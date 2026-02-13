import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Telegram bot settings
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8429912645:AAG95x5WDgqF8r42zFwnF8oLTPSGdQmMcUM")  # Default to the provided token
    ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # Chat ID for admin notifications
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/dbname")
    
    # File storage settings
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "20971520"))  # 20MB in bytes
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()