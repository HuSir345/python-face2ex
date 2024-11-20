from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    try:
        logger.info("Attempting to render index.html")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        logger.error(f"Python version: {sys.version}")
        logger.error(f"Current working directory: {os.getcwd()}")
        logger.error(f"Directory contents: {os.listdir('.')}")
        return jsonify({
            "error": str(e),
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "files": os.listdir('.')
        }), 500

@app.errorhandler(404)
def not_found(e):
    logger.error(f"404 error: {str(e)}")
    return jsonify({"error": "Not found", "path": request.path}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 error: {str(e)}")
    return jsonify({"error": str(e)}), 500

# 添加健康检查路由
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 