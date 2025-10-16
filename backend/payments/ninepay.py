# ref: https: // developers.9pay.vn/danh-sach-api/quy-tac-tich-hop
import hashlib
import hmac
import time
import json
import base64
import requests
from urllib.parse import urlencode, quote
from django.conf import settings
from logzero import logger


class NinePay:
    def __init__(self):
        self.merchant_key = settings.NINEPAY_MERCHANT_KEY
        self.secret_key = settings.NINEPAY_SECRET_KEY
        self.checksum_key = settings.NINEPAY_CHECKSUM_KEY
        self.api_domain = settings.NINEPAY_URL
        self.portal_url = f"{self.api_domain}/portal"

    def get_payment_url(self, invoice_no, amount, description, return_url, back_url=None):
        logger.info("=== Creating 9Pay Payment URL ===")

        current_time = str(int(time.time()))

        payload = {
            "merchantKey": self.merchant_key,
            "time": current_time,
            "invoice_no": invoice_no,
            "amount": str(int(amount)),
            "description": description,
            "return_url": return_url
        }
        if back_url:
            payload["back_url"] = back_url

        query_http = urlencode(sorted(payload.items()))

        endpoint_path_for_signing = "/payments/create"
        message_to_sign = "\n".join([
            "POST",
            self.api_domain + endpoint_path_for_signing,
            current_time,
            query_http
        ])

        signature = self._generate_request_signature(message_to_sign, self.secret_key)

        json_string = json.dumps(payload, separators=(',', ':'))
        base_encode = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

        final_params = {
            "baseEncode": base_encode,
            "signature": signature
        }
        payment_url = f"{self.portal_url}?{urlencode(final_params, quote_via=quote)}"

        logger.info(f"✓ 9Pay Payment URL created successfully")
        return payment_url

    def _generate_request_signature(self, data_string, key):
        """
        Generate HMAC-SHA256 signature
        Returns: Base64 encoded signature
        """
        key_bytes = key.encode('utf-8')
        data_bytes = data_string.encode('utf-8')
        hmac_obj = hmac.new(key_bytes, data_bytes, hashlib.sha256)
        signature_bytes = hmac_obj.digest()
        return base64.b64encode(signature_bytes).decode('utf-8')

    def query_payment_status(self, invoice_no):
        logger.info(f"=== [9Pay Query] Checking invoice_no: {invoice_no} ===")

        try:
            # 1. Prepare parameters
            current_time = str(int(time.time()))
            endpoint_path = f"/v2/payments/{invoice_no}/inquire"
            full_url = f"{self.api_domain}{endpoint_path}"

            # 2. Build message to sign
            #  docs: <Http request method> +"\n"+<URI>+"\n"+<timestamp>+"\n"+<canonicalized resources>
            message_to_sign = "\n".join([
                "GET",
                full_url,
                current_time,
            ])

            # 3. Generate signature
            signature = self._generate_request_signature(message_to_sign, self.secret_key)

            authorization_value = (
                f"Signature Algorithm=HS256,"
                f"Credential={self.merchant_key},"
                f"SignedHeaders=,"
                f"Signature={signature}"
            )

            # 5. Build headers
            headers = {
                'Authorization': authorization_value,
                'Date': current_time,
                'Content-Type': 'application/json'
            }

            logger.debug(
                f"[9Pay Query] Headers:\n"
                f"  Authorization: {authorization_value[:80]}...\n"
                f"  Date: {current_time}"
            )

            # 6. Call API
            logger.info(f"[9Pay Query] GET {full_url}")

            response = requests.get(
                full_url,
                headers=headers,
                timeout=15
            )

            logger.info(f"[9Pay Query] Response status: {response.status_code}")

            # 7. Handle response
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    logger.error(
                        f"[9Pay Query] API Error {response.status_code}:\n"
                        f"  Error code: {error_data.get('error_code')}\n"
                        f"  Message: {error_data.get('message')}\n"
                        f"  Failure reason: {error_data.get('failure_reason')}"
                    )

                    return {
                        'success': False,
                        'status': error_data.get('status'),
                        'error_code': str(error_data.get('error_code', '')),
                        'data': None,
                        'message': error_data.get('message', f'HTTP {response.status_code}'),
                        'failure_reason': error_data.get('failure_reason')
                    }
                except:
                    logger.error(f"[9Pay Query] Non-JSON error: {response.text}")
                    return {
                        'success': False,
                        'status': None,
                        'error_code': None,
                        'data': None,
                        'message': f'HTTP {response.status_code}',
                        'raw_response': response.text
                    }

            # 8. Parse success response
            data = response.json()

            status = data.get('status')
            error_code = str(data.get('error_code', '000'))
            payment_no = data.get('payment_no')
            amount = data.get('amount')
            method = data.get('method')

            logger.info(
                f"[9Pay Query] ✓ Success:\n"
                f"  Invoice: {invoice_no}\n"
                f"  Payment No: {payment_no}\n"
                f"  Status: {status} ({self.get_status_description(status)})\n"
                f"  Error Code: {error_code}\n"
                f"  Amount: {amount}\n"
                f"  Method: {method}"
            )

            return {
                'success': True,
                'status': status,
                'error_code': error_code,
                'data': data,
                'message': 'Query successful'
            }

        except requests.exceptions.Timeout:
            logger.error(f"[9Pay Query] ✗ Timeout for {invoice_no}")
            return {
                'success': False,
                'status': None,
                'error_code': None,
                'data': None,
                'message': 'Request timeout'
            }

        except requests.exceptions.ConnectionError as e:
            logger.error(f"[9Pay Query] ✗ Connection error: {e}")
            return {
                'success': False,
                'status': None,
                'error_code': None,
                'data': None,
                'message': f'Connection error: {str(e)}'
            }

        except Exception as e:
            logger.error(f"[9Pay Query] ✗ Unexpected error: {e}", exc_info=True)
            return {
                'success': False,
                'status': None,
                'error_code': None,
                'data': None,
                'message': f'Unexpected error: {str(e)}'
            }

    def get_status_description(self, status_code):
        """Map status code to description"""
        status_map = {
            2: 'Đang xử lý',
            3: 'Chờ kiểm tra',
            4: 'Liên kết thẻ thành công',
            5: 'Thành công',
            6: 'Thất bại',
            8: 'Bị hủy',
            9: 'Bị từ chối',
            16: 'Đã nhận tiền (Chuyển khoản)',
        }
        return status_map.get(status_code, f'Unknown status ({status_code})')

    def verify_return(self, params):
        """Verify return callback from 9Pay"""
        logger.info("=== Verifying 9Pay Return Callback ===")

        encoded_result = params.get('result')
        received_checksum = params.get('checksum')

        if not encoded_result or not received_checksum:
            logger.error("Missing 'result' or 'checksum' in params")
            return False

        # Calculate expected checksum
        string_to_hash = encoded_result + self.checksum_key
        expected_checksum = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest().upper()

        # Compare checksums
        if hmac.compare_digest(expected_checksum, received_checksum.upper()):
            logger.info("✓ Checksum is valid")
            return True
        else:
            logger.error("✗ Checksum is invalid!")
            return False

    def parse_return_data(self, params):
        """Parse return data from 9Pay callback"""
        logger.info("=== Parsing 9Pay Return Data ===")

        encoded_result = params.get('result')
        if not encoded_result:
            logger.error("Missing 'result' in params")
            return None

        try:
            # Fix base64 padding if needed
            # Add padding to make length multiple of 4
            missing_padding = len(encoded_result) % 4
            if missing_padding:
                encoded_result += '=' * (4 - missing_padding)

            logger.debug(f"Encoded result (with padding): {encoded_result}")

            # Decode base64
            decoded_json = base64.b64decode(encoded_result).decode('utf-8')
            logger.debug(f"Decoded JSON: {decoded_json}")

            payment_data = json.loads(decoded_json)

            logger.info(f"✓ Successfully parsed payment data")
            logger.debug(f"Payment data: {payment_data}")

            return payment_data
        except Exception as e:
            logger.error(f"✗ Failed to decode/parse result: {e}")
            logger.error(f"Encoded result length: {len(params.get('result', ''))}")
            return None

    def verify_callback(self, callback_data):
        """Legacy method for backward compatibility"""
        logger.info("=== Verifying 9Pay Callback (legacy method) ===")

        if not self.verify_return(callback_data):
            return False, None

        payment_data = self.parse_return_data(callback_data)
        if not payment_data:
            return False, None

        return True, payment_data
