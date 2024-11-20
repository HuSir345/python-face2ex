from flask import Flask, send_from_directory
import os
from app import app

# 添加静态文件支持
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('app/static', path)

# Vercel 需要这个
handler = app 