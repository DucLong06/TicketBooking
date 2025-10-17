#!/bin/bash
# test_9pay_curl.sh

# ============================================================================
# CONFIG - THAY ĐỔI THEO THÔNG TIN CỦA BẠN
# ============================================================================

MERCHANT_KEY=""  # ← Thay bằng merchant key thật
SECRET_KEY=""  # ← Thay bằng secret key thật
INVOICE_NO="DCAEFF352B05C"  # ← Thay bằng invoice_no thật
API_DOMAIN="https://sand-payment.9pay.vn"
TIMESTAMP=$(date +%s)

echo "=========================================="
echo "9PAY CURL TEST VARIANTS"
echo "=========================================="
echo "Merchant Key: $MERCHANT_KEY"
echo "Invoice No: $INVOICE_NO"
echo "Timestamp: $TIMESTAMP"
echo ""

# ============================================================================
# HELPER FUNCTION - Generate HMAC-SHA256 signature
# ============================================================================

generate_signature() {
    local message="$1"
    local secret="$2"
    echo -n "$message" | openssl dgst -sha256 -hmac "$secret" -binary | base64
}

# ============================================================================
# VARIANT 1: Authorization format như docs
# ============================================================================

echo "============================================"
echo "TEST 1: Authorization = Signature Algorithm=HS256,..."
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo "Authorization: $AUTH_HEADER"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 2: Không có trailing newline
# ============================================================================

echo "============================================"
echo "TEST 2: No trailing newline"
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 3: Chỉ path, không có domain
# ============================================================================

echo "============================================"
echo "TEST 3: Path only (no domain)"
echo "============================================"

MESSAGE="GET
/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 4: Có merchantKey trong canonicalized resources
# ============================================================================

echo "============================================"
echo "TEST 4: With merchantKey in canonicalized resources"
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
merchantKey=${MERCHANT_KEY}"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 5: Signature header thay vì Authorization
# ============================================================================

echo "============================================"
echo "TEST 5: 'Signature' header instead of 'Authorization'"
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
SIG_HEADER="Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Signature: $SIG_HEADER" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 6: Chỉ signature thuần, không có format đặc biệt
# ============================================================================

echo "============================================"
echo "TEST 6: Pure signature in Authorization"
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $SIGNATURE" \
  -H "Date: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 7: Timestamp header thay vì Date
# ============================================================================

echo "============================================"
echo "TEST 7: 'Timestamp' header instead of 'Date'"
echo "============================================"

MESSAGE="GET
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Timestamp: $TIMESTAMP" \
  -H "Content-Type: application/json"

echo ""
echo ""

# ============================================================================
# VARIANT 8: Lowercase 'get' và không có Content-Type
# ============================================================================

echo "============================================"
echo "TEST 8: Lowercase 'get' and no Content-Type"
echo "============================================"

MESSAGE="get
${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire
${TIMESTAMP}
"

SIGNATURE=$(generate_signature "$MESSAGE" "$SECRET_KEY")
AUTH_HEADER="Signature Algorithm=HS256,Credential=${MERCHANT_KEY},SignedHeaders=,Signature=${SIGNATURE}"

echo "Message to sign:"
echo "$MESSAGE" | cat -A
echo ""
echo "Signature: $SIGNATURE"
echo ""

curl -v -X GET \
  "${API_DOMAIN}/v2/payments/${INVOICE_NO}/inquire" \
  -H "Authorization: $AUTH_HEADER" \
  -H "Date: $TIMESTAMP"

echo ""
echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo "=========================================="
echo "TEST COMPLETED"
echo "=========================================="
echo "Check responses above for HTTP 200 status"
echo ""