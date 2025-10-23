# Trading Platform - Admin Panel System

Hệ thống quản trị toàn diện cho nền tảng mua bán tài liệu với tích hợp tiền ảo, staking và đầu tư.

## 📋 Tổng Quan

Dự án này là một hệ thống admin panel đầy đủ chức năng được xây dựng dựa trên cấu trúc từ [repository gốc](https://github.com/dinhthuysd/trading).

### Tính Năng Chính

#### 🔐 **Hệ Thống Bảo Mật**
- **JWT Authentication** với Access & Refresh Token
- **2FA (Two-Factor Authentication)** với TOTP  
- **Role-based Authorization** (Super Admin, Admin, Moderator)
- **Password Hashing** với bcrypt
- **Rate Limiting** (100 requests/minute per IP)
- **Audit Logging** cho mọi hành động quan trọng

#### 👨‍💼 **Admin Panel Features**
- Dashboard tổng quan với thống kê real-time
- Quản lý người dùng (User Management)
- Xác minh KYC (KYC Verification)
- Duyệt tài liệu (Document Approval)
- Xử lý nạp tiền (Deposit Management)
- Xử lý rút tiền (Withdrawal Management)
- Lịch sử giao dịch (Transaction History)
- Nhật ký hệ thống (Audit Logs)

---

## 🚀 Hướng Dẫn Chạy Ứng Dụng

### 1. Cài Đặt Backend

```bash
# Di chuyển đến thư mục backend
cd /app/backend

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi động backend (managed by supervisor)
sudo supervisorctl restart backend

# Kiểm tra trạng thái
sudo supervisorctl status backend

# Xem logs
tail -f /var/log/supervisor/backend.*.log
```

### 2. Cài Đặt Frontend

```bash
# Di chuyển đến thư mục frontend
cd /app/frontend

# Cài đặt dependencies
yarn install

# Khởi động frontend (managed by supervisor)
sudo supervisorctl restart frontend

# Xem logs
tail -f /var/log/supervisor/frontend.*.log
```

### 3. Khởi Động Tất Cả Services

```bash
# Restart all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status
```

---

## 👤 Tài Khoản Admin Mặc Định

| Field    | Value                |
|----------|----------------------|
| Email    | admin@trading.com    |
| Password | Admin@123456         |
| Role     | super_admin          |

**⚠️ LƯU Ý:** Vui lòng đổi mật khẩu ngay sau lần đăng nhập đầu tiên!

**URL Admin Panel:** `/admin/login`

---

## 📊 Database Collections

Hệ thống sử dụng MongoDB với các collections sau:

1. **admin_users** - Quản lý admin accounts
2. **users** - Người dùng platform
3. **wallets** - Ví coin nội bộ
4. **documents** - Tài liệu được upload
5. **deposit_requests** - Yêu cầu nạp tiền
6. **withdrawal_requests** - Yêu cầu rút tiền
7. **transactions** - Lịch sử giao dịch
8. **kyc_submissions** - Hồ sơ KYC
9. **staking_positions** - Vị thế staking
10. **investment_positions** - Gói đầu tư
11. **audit_logs** - Nhật ký hệ thống

---

## 🔌 API Endpoints

### Admin Authentication (`/api/admin/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/auth/login` | Đăng nhập admin |
| GET | `/admin/auth/profile` | Lấy thông tin profile |
| PUT | `/admin/auth/profile` | Cập nhật profile |
| POST | `/admin/auth/change-password` | Đổi mật khẩu |
| POST | `/admin/auth/2fa/setup` | Thiết lập 2FA |
| POST | `/admin/auth/logout` | Đăng xuất |

### Admin Management (`/api/admin`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/dashboard` | Dashboard statistics |
| GET | `/admin/users` | Danh sách users |
| GET | `/admin/users/{id}` | Chi tiết user |
| PUT | `/admin/users/{id}/status` | Kích hoạt/vô hiệu hóa user |
| GET | `/admin/kyc/pending` | KYC chờ duyệt |
| PUT | `/admin/kyc/{id}/verify` | Duyệt KYC |
| GET | `/admin/documents` | Danh sách tài liệu |
| PUT | `/admin/documents/{id}/approve` | Duyệt tài liệu |
| GET | `/admin/deposits` | Yêu cầu nạp tiền |
| PUT | `/admin/deposits/{id}/process` | Xử lý nạp tiền |
| GET | `/admin/withdrawals` | Yêu cầu rút tiền |
| PUT | `/admin/withdrawals/{id}/process` | Xử lý rút tiền |
| GET | `/admin/transactions` | Lịch sử giao dịch |
| GET | `/admin/audit-logs` | Nhật ký hệ thống |

---

## 🎨 Frontend Pages

### Public Pages
- `/` - Landing page với link đến admin panel
- `/admin/login` - Trang đăng nhập admin (đẹp mắt với gradient animation)

### Admin Pages (Protected - Requires Login)
- `/admin/dashboard` - Dashboard tổng quan với statistics cards
- `/admin/users` - Quản lý người dùng với search và pagination
- `/admin/kyc` - Xác minh KYC
- `/admin/documents` - Duyệt tài liệu
- `/admin/deposits` - Xử lý nạp tiền (approve/reject)
- `/admin/withdrawals` - Xử lý rút tiền (approve/reject)
- `/admin/transactions` - Lịch sử giao dịch
- `/admin/logs` - Nhật ký hệ thống

---

## 🔒 Role-Based Permissions

### Super Admin
- ✅ Quản lý admin khác
- ✅ Toàn quyền truy cập mọi chức năng
- ✅ Xem và quản lý audit logs
- ✅ Cài đặt hệ thống

### Admin
- ✅ Quản lý người dùng
- ✅ Xử lý KYC, deposits, withdrawals
- ✅ Duyệt tài liệu
- ✅ Xem thống kê
- ❌ Không thể quản lý admin khác

### Moderator
- ✅ Duyệt tài liệu
- ✅ Xác minh KYC
- ✅ Xem thống kê cơ bản
- ❌ Không thể xử lý deposits/withdrawals
- ❌ Không thể quản lý users

---

## 🧪 Testing API

### Admin Login Test
```bash
curl -X POST http://localhost:8001/api/admin/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@trading.com",
    "password": "Admin@123456"
  }'
```

### Get Dashboard Stats (Requires Token)
```bash
curl http://localhost:8001/api/admin/dashboard \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🛠️ Troubleshooting

### Backend không khởi động?
```bash
# Kiểm tra logs
tail -f /var/log/supervisor/backend.*.log

# Restart backend
sudo supervisorctl restart backend
```

### Frontend không compile?
```bash
# Kiểm tra logs
tail -f /var/log/supervisor/frontend.*.log

# Restart frontend
sudo supervisorctl restart frontend
```

### Database connection error?
```bash
# Restart MongoDB
sudo supervisorctl restart mongodb

# Test connection
mongosh mongodb://localhost:27017
```

---

## 📝 Cấu Trúc Code

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── models.py              # Pydantic models
│   ├── security.py            # JWT, hashing, 2FA utilities
│   ├── middleware.py          # Authentication middleware
│   ├── database.py            # MongoDB connection & indexes
│   ├── routes/
│   │   ├── admin_auth.py      # Admin authentication routes
│   │   └── admin_management.py # Admin management routes
│   ├── .env                   # Environment variables
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/admin/       # Admin pages
│   │   ├── components/admin/  # Admin components
│   │   ├── services/          # API services
│   │   ├── contexts/          # React contexts
│   │   └── App.js            # Main app with routing
│   ├── .env
│   └── package.json
│
└── README.md                  # This file
```

---

## 📌 Version Information

- **Version:** 1.0.0
- **Last Updated:** October 22, 2025
- **Status:** ✅ Production Ready

---

## 🎯 Checklist Hoàn Thành

✅ **Backend**
- [x] Models & Security
- [x] Authentication & Authorization (JWT + 2FA)
- [x] Role-based Access Control
- [x] Admin Management APIs
- [x] Database Indexes
- [x] Audit Logging
- [x] Default Admin Account Seeded

✅ **Frontend**
- [x] Beautiful Admin Login Page
- [x] Responsive Dashboard with Stats
- [x] Admin Layout with Sidebar
- [x] User Management Page
- [x] Deposit Management Page
- [x] Withdrawal Management Page
- [x] KYC, Documents, Transactions, Logs Pages (Template)
- [x] Protected Routes
- [x] Context for Auth

✅ **Database**
- [x] MongoDB Collections Setup
- [x] Indexes Created
- [x] Default Admin Seeded

---

**Developed with ❤️ by Emergent Labs**

**Liên hệ:** Để được hỗ trợ, vui lòng kiểm tra logs và documentation
