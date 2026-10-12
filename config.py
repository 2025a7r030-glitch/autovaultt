import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Application configuration for AutoVault."""
    # Secret key for session management and CSRF security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'autovault-dev-secret-key-3rd-sem-cybersec-2026'
    
    # Check if running in serverless environment (e.g. Vercel)
    IS_VERCEL = bool(os.environ.get('VERCEL'))
    
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    if db_url:
        SQLALCHEMY_DATABASE_URI = db_url
    elif IS_VERCEL:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/autovault.db'
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'autovault.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configurations (reserved for Document Vault)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    if IS_VERCEL:
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'instance', 'uploads')
