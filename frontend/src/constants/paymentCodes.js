export const VNPAY_RESPONSE_CODES = {
    '00': {
        code: '00',
        message: 'Giao dịch thành công',
        severity: 'success',
        icon: 'check-circle',
        color: '#10b981'
    },
    '07': {
        code: '07',
        message: 'Trừ tiền thành công. Giao dịch bị nghi ngờ',
        severity: 'warning',
        icon: 'alert-triangle',
        color: '#f59e0b',
        additionalInfo: 'Giao dịch của bạn đang được xác minh. Vui lòng liên hệ hotline nếu cần hỗ trợ.'
    },
    '09': {
        code: '09',
        message: 'Thẻ/Tài khoản chưa đăng ký Internet Banking',
        severity: 'error',
        icon: 'credit-card-off',
        color: '#ef4444',
        action: 'Vui lòng đăng ký Internet Banking trước khi thực hiện giao dịch.'
    },
    '10': {
        code: '10',
        message: 'Xác thực thông tin sai quá 3 lần',
        severity: 'error',
        icon: 'lock',
        color: '#ef4444',
        action: 'Tài khoản của bạn có thể bị tạm khóa. Vui lòng liên hệ ngân hàng.'
    },
    '11': {
        code: '11',
        message: 'Hết hạn chờ thanh toán',
        severity: 'error',
        icon: 'clock',
        color: '#ef4444',
        action: 'Vui lòng thực hiện lại giao dịch.'
    },
    '12': {
        code: '12',
        message: 'Thẻ/Tài khoản bị khóa',
        severity: 'error',
        icon: 'lock',
        color: '#ef4444',
        action: 'Vui lòng liên hệ ngân hàng để được hỗ trợ.'
    },
    '13': {
        code: '13',
        message: 'Nhập sai mã OTP',
        severity: 'error',
        icon: 'shield-off',
        color: '#ef4444',
        action: 'Vui lòng kiểm tra lại mã OTP và thử lại.'
    },
    '24': {
        code: '24',
        message: 'Khách hàng hủy giao dịch',
        severity: 'info',
        icon: 'x-circle',
        color: '#6b7280',
        action: 'Bạn đã hủy giao dịch. Vui lòng thử lại nếu muốn tiếp tục.'
    },
    '51': {
        code: '51',
        message: 'Tài khoản không đủ số dư',
        severity: 'error',
        icon: 'wallet',
        color: '#ef4444',
        action: 'Vui lòng kiểm tra số dư và thử lại.'
    },
    '65': {
        code: '65',
        message: 'Vượt quá hạn mức giao dịch trong ngày',
        severity: 'error',
        icon: 'trending-up',
        color: '#ef4444',
        action: 'Bạn đã vượt quá hạn mức giao dịch. Vui lòng thử lại vào ngày mai.'
    },
    '75': {
        code: '75',
        message: 'Ngân hàng đang bảo trì',
        severity: 'warning',
        icon: 'tool',
        color: '#f59e0b',
        action: 'Ngân hàng đang bảo trì hệ thống. Vui lòng thử lại sau.'
    },
    '79': {
        code: '79',
        message: 'Nhập sai mật khẩu thanh toán quá nhiều lần',
        severity: 'error',
        icon: 'alert-octagon',
        color: '#ef4444',
        action: 'Bạn đã nhập sai mật khẩu quá nhiều lần. Vui lòng liên hệ ngân hàng.'
    },
    '99': {
        code: '99',
        message: 'Lỗi không xác định',
        severity: 'error',
        icon: 'alert-circle',
        color: '#ef4444',
        action: 'Đã xảy ra lỗi trong quá trình xử lý. Vui lòng thử lại sau.'
    }
};

export const getResponseInfo = (code) => {
    return VNPAY_RESPONSE_CODES[code] || VNPAY_RESPONSE_CODES['99'];
};

export const isSuccessCode = (code) => {
    return code === '00';
};

export const isWarningCode = (code) => {
    return code === '07' || code === '75';
};

export const isErrorCode = (code) => {
    return !isSuccessCode(code) && !isWarningCode(code) && code !== '24';
};

export const isCancelCode = (code) => {
    return code === '24';
};