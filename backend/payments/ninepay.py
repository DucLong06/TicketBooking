import hashlib
import hmac
import time
import json
import base64
from urllib.parse import urlencode, quote
from collections import OrderedDict
from django.conf import settings
from logzero import logger


class NinePay:
    def __init__(self):
        self.merchant_key = settings.NINEPAY_MERCHANT_KEY
        self.secret_key = settings.NINEPAY_SECRET_KEY
        self.checksum_key = settings.NINEPAY_CHECKSUM_KEY
        self.api_domain = settings.NINEPAY_URL
        self.portal_url = f"{self.api_domain}/portal"

    def _generate_request_signature(self, data_string, key):
        key_bytes = key.encode('utf-8')
        data_bytes = data_string.encode('utf-8')
        hmac_obj = hmac.new(key_bytes, data_bytes, hashlib.sha256)
        signature_bytes = hmac_obj.digest()
        return base64.b64encode(signature_bytes).decode('utf-8')

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
