import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    IMAGEHUB_API_KEY = 'chv_xMmv_253f4ce45059f97a03dab8d02788f8c8243c0cd7f4d7c5e19a77eefcab719507e5a2358d4ee95222fe878fca601d1e8d06ee1f29030f1b409d550dba1c998586'
    COZE_API_TOKEN = 'pat_0OjgQdYOMeEPHi3wUdDvZCLjaLOgbS87dDYMVdoxFQO9iYWuaamgn5pqrHKhlig2'
    COZE_WORKFLOW_ID = '7435930213924306978' 