from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import re

# ============ ADMIN MODELS ============

class AdminRole(BaseModel):
    """Admin role definition"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # admin, super_admin, moderator
    permissions: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdminUser(BaseModel):
    """Admin user model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    password_hash: str
    full_name: str
    role: str  # admin, super_admin, moderator
    is_active: bool = True
    is_2fa_enabled: bool = False
    totp_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AdminUserCreate(BaseModel):
    """Schema for creating admin user"""
    email: EmailStr
    username: str
    password: str
    full_name: str
    role: str = "admin"
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        allowed_roles = ['admin', 'super_admin', 'moderator']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of {allowed_roles}')
        return v

class AdminLogin(BaseModel):
    """Admin login schema"""
    email: EmailStr
    password: str
    totp_code: Optional[str] = None

class AdminUpdateProfile(BaseModel):
    """Update admin profile"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class AdminChangePassword(BaseModel):
    """Change admin password"""
    old_password: str
    new_password: str
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        return v

# ============ USER MODELS ============

class User(BaseModel):
    """User model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    password_hash: str
    full_name: Optional[str] = None
    role: str = "user"
    kyc_status: str = "pending"  # pending, verified, rejected
    is_active: bool = True
    is_2fa_enabled: bool = False
    totp_secret: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    """Schema for creating user"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
    totp_code: Optional[str] = None

# ============ DOCUMENT MODELS ============

class Document(BaseModel):
    """Document model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    price: float
    category: str
    tags: List[str] = Field(default_factory=list)
    seller_id: str
    file_id: str  # GridFS file ID
    status: str = "pending"  # pending, approved, rejected
    downloads: int = 0
    revenue: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DocumentCreate(BaseModel):
    """Schema for creating document"""
    title: str
    description: str
    price: float
    category: str
    tags: List[str] = Field(default_factory=list)

# ============ WALLET MODELS ============

class Wallet(BaseModel):
    """Internal coin wallet"""
    model_config = ConfigDict(extra="ignore")
    
    user_id: str
    balance: float = 0.0
    locked_balance: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Transaction(BaseModel):
    """Transaction model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: str  # deposit, withdrawal, purchase, staking, investment, etc.
    amount: float
    status: str  # pending, completed, failed
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ============ DEPOSIT/WITHDRAWAL MODELS ============

class DepositRequest(BaseModel):
    """Deposit request model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    amount: float
    payment_method: str
    status: str = "pending"  # pending, approved, rejected
    admin_note: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None

class WithdrawalRequest(BaseModel):
    """Withdrawal request model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    amount: float
    withdrawal_method: str
    withdrawal_address: str
    status: str = "pending"  # pending, approved, rejected
    admin_note: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: Optional[datetime] = None

# ============ STAKING MODELS ============

class StakingPosition(BaseModel):
    """Staking position model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    plan: str  # basic, premium, vip
    amount: float
    apy: float
    locked_until: datetime
    rewards_earned: float = 0.0
    status: str = "active"  # active, unstaked
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    unstaked_at: Optional[datetime] = None

# ============ INVESTMENT MODELS ============

class InvestmentPosition(BaseModel):
    """Investment position model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    package: str  # starter, growth, premium
    amount: float
    expected_return: float
    actual_return: float = 0.0
    status: str = "active"  # active, completed
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime
    completed_at: Optional[datetime] = None

# ============ KYC MODELS ============

class KYCSubmission(BaseModel):
    """KYC submission model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    id_type: str
    file_ids: List[str] = Field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected
    admin_note: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    reviewed_at: Optional[datetime] = None

# ============ AUDIT LOG MODELS ============

class AuditLog(BaseModel):
    """Audit log model"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ============ RESPONSE MODELS ============

class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True

class DashboardStats(BaseModel):
    """Admin dashboard statistics"""
    total_users: int
    total_documents: int
    total_transactions: int
    pending_deposits: int
    pending_withdrawals: int
    pending_kyc: int
    total_revenue: float
    active_stakings: int
    active_investments: int