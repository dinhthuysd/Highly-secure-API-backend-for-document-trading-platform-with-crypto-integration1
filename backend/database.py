from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

async def create_indexes():
    """Create database indexes for performance"""
    
    # Admin users indexes
    await db.admin_users.create_index("email", unique=True)
    await db.admin_users.create_index("username", unique=True)
    await db.admin_users.create_index("role")
    
    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.users.create_index("kyc_status")
    await db.users.create_index("role")
    
    # Documents indexes
    await db.documents.create_index("seller_id")
    await db.documents.create_index("status")
    await db.documents.create_index("category")
    await db.documents.create_index("created_at")
    
    # Transactions indexes
    await db.transactions.create_index("user_id")
    await db.transactions.create_index("type")
    await db.transactions.create_index("status")
    await db.transactions.create_index("created_at")
    
    # Wallets indexes
    await db.wallets.create_index("user_id", unique=True)
    
    # Deposit requests indexes
    await db.deposit_requests.create_index("user_id")
    await db.deposit_requests.create_index("status")
    await db.deposit_requests.create_index("created_at")
    
    # Withdrawal requests indexes
    await db.withdrawal_requests.create_index("user_id")
    await db.withdrawal_requests.create_index("status")
    await db.withdrawal_requests.create_index("created_at")
    
    # Staking positions indexes
    await db.staking_positions.create_index("user_id")
    await db.staking_positions.create_index("status")
    
    # Investment positions indexes
    await db.investment_positions.create_index("user_id")
    await db.investment_positions.create_index("status")
    
    # KYC submissions indexes
    await db.kyc_submissions.create_index("user_id")
    await db.kyc_submissions.create_index("status")
    
    # Audit logs indexes
    await db.audit_logs.create_index("user_id")
    await db.audit_logs.create_index("action")
    await db.audit_logs.create_index("timestamp")
    
    print("Database indexes created successfully")

async def seed_default_admin():
    """Create default admin user if not exists"""
    from security import hash_password
    from datetime import datetime, timezone
    
    # Check if admin already exists
    existing_admin = await db.admin_users.find_one({"email": "admin@trading.com"})
    
    if not existing_admin:
        admin_user = {
            "id": "admin-default-001",
            "email": "admin@trading.com",
            "username": "superadmin",
            "password_hash": hash_password("Admin@123456"),
            "full_name": "Super Administrator",
            "role": "super_admin",
            "is_active": True,
            "is_2fa_enabled": False,
            "totp_secret": None,
            "last_login": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        await db.admin_users.insert_one(admin_user)
        print("✅ Default admin user created:")
        print("   Email: admin@trading.com")
        print("   Password: Admin@123456")
        print("   Role: super_admin")
        print("   ⚠️  PLEASE CHANGE PASSWORD AFTER FIRST LOGIN!")
    else:
        print("Admin user already exists")

async def get_db():
    """Dependency to get database instance"""
    return db