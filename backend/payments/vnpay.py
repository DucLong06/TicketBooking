import hashlib
import hmac
import urllib.parse
from datetime import datetime, timedelta
import random
from django.conf import settings
from logzero import logger


class VNPay:
    def __init__(self):
        self.vnp_TmnCode = settings.VNP_TMNCODE
        self.vnp_HashSecret = settings.VNP_HASTSECRET
        self.vnp_Url = settings.VNP_URL
        self.vnp_ReturnUrl = settings.VNP_RETURNURL

    def get_payment_url(self, request, order_id, amount, order_desc, bank_code=""):
        """
            Generate VNPay payment URL
            ref: https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html
        """

        # Calculate expiry time (15 minutes from now)
        expire_time = datetime.now() + timedelta(minutes=settings.PAYMENT_TIMEOUT_MINUTES)

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
        """Validate VNPay response - FIXED VERSION"""
        vnp_params = {}
        for key, value in request_data.items():
            if key.startswith('vnp_'):
                vnp_params[key] = value

        vnp_secure_hash = vnp_params.pop('vnp_SecureHash', None)

        vnp_params.pop('vnp_SecureHashType', None)

        vnp_params = dict(sorted(vnp_params.items()))

        hash_data = '&'.join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in vnp_params.items()])

        signature = self._hmacsha512(self.vnp_HashSecret, hash_data)

        return signature == vnp_secure_hash

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
