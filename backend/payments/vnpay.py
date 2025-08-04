import hashlib
import hmac
import urllib.parse
from datetime import datetime, timedelta
import random
from django.conf import settings


class VNPay:
    def __init__(self):
        self.vnp_TmnCode = settings.VNP_TMNCODE
        self.vnp_HashSecret = settings.VNP_HASTSECRET
        self.vnp_Url = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
        self.vnp_ReturnUrl = "http://localhost:8000/api/payment/vnpay/return/"

        # Debug: Check credentials
        if not self.vnp_TmnCode or not self.vnp_HashSecret:
            print(f"⚠️  VNPay Credentials Missing:")
            print(f"   TmnCode: {'✓' if self.vnp_TmnCode else '✗ MISSING'}")
            print(f"   HashSecret: {'✓' if self.vnp_HashSecret else '✗ MISSING'}")
            print(f"   Please check your .env file and settings.py")

    def get_payment_url(self, request, order_id, amount, order_desc, bank_code=""):
        """
            Generate VNPay payment URL
            ref: https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html
        """

        # Calculate expiry time (15 minutes from now)
        expire_time = datetime.now() + timedelta(minutes=15)

        vnp_params = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': self.vnp_TmnCode,
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': order_id,
            'vnp_Amount': int(amount * 100),
            'vnp_OrderInfo': order_desc,
            'vnp_OrderType': 'other',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': self.vnp_ReturnUrl,
            'vnp_IpAddr': self.get_client_ip(request),
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_ExpireDate': expire_time.strftime('%Y%m%d%H%M%S'),
        }

        if bank_code:
            vnp_params['vnp_BankCode'] = bank_code
        # Sort params
        vnp_params = dict(sorted(vnp_params.items()))

        # Create hash data
        hash_data = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in vnp_params.items()])

        # Create secure hash
        vnp_secure_hash = self._hmacsha512(self.vnp_HashSecret, hash_data)

        # Add hash to params
        vnp_params['vnp_SecureHash'] = vnp_secure_hash

        # Create payment URL
        payment_url = f"{self.vnp_Url}?{urllib.parse.urlencode(vnp_params)}"

        # Debug logging
        print(f"=== VNPay Debug ===")
        print(f"TmnCode: {self.vnp_TmnCode}")
        print(f"Amount: {amount} -> {int(amount * 100)}")
        print(f"OrderId: {order_id}")
        print(f"CreateDate: {datetime.now().strftime('%Y%m%d%H%M%S')}")
        print(f"ExpireDate: {expire_time.strftime('%Y%m%d%H%M%S')}")
        print(f"ReturnUrl: {self.vnp_ReturnUrl}")
        print(f"Payment URL: {payment_url}")
        print(f"=================")

        return payment_url

    def verify_return_url(self, request_params):
        """Verify VNPay return data"""
        vnp_params = {}
        for key, value in request_params.items():
            if key.startswith('vnp_'):
                vnp_params[key] = value

        # Remove hash param
        vnp_secure_hash = vnp_params.pop('vnp_SecureHash', None)
        vnp_params.pop('vnp_SecureHashType', None)

        # Sort params
        vnp_params = dict(sorted(vnp_params.items()))

        # Create hash data
        hash_data = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in vnp_params.items()])

        # Verify hash
        signature = self._hmacsha512(self.vnp_HashSecret, hash_data)

        return signature == vnp_secure_hash

    def _hmacsha512(self, key, data):
        byte_key = key.encode('utf-8')
        byte_data = data.encode('utf-8')
        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()

    def validate_response(self, request_data):
        """Validate VNPay response"""
        vnp_SecureHash = request_data.get('vnp_SecureHash')

        # Remove hash from params
        params = dict(request_data)
        if 'vnp_SecureHash' in params:
            del params['vnp_SecureHash']

        # Sort and create query string
        sorted_params = sorted(params.items())
        query_string = urllib.parse.urlencode(sorted_params)

        # Create signature
        hash_value = hmac.new(
            self.vnp_HashSecret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        return hash_value == vnp_SecureHash

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
