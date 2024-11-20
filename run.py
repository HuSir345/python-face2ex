from app import app
from flask import send_from_directory
import os

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('app/static', path)

if __name__ == '__main__':
    app.run(debug=True)
else:
    # 这是为 Vercel 准备的
    application = app 