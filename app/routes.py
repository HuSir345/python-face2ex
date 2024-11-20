from flask import render_template, jsonify, request
from app import app
from app.utils import process_face_swap
import base64
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/swap-face', methods=['POST'])
def swap_face():
    try:
        # 记录接收到的请求信息
        logger.info("=== Received Swap Face Request ===")
        logger.info(f"Headers: {json.dumps(dict(request.headers), indent=2)}")
        logger.info("Request contains two base64 encoded images (not logged for brevity)")
        
        # 获取上传的图片
        face_image = request.json.get('pic1')
        base_image = request.json.get('pic2')
        
        # 准备调用 Coze API
        logger.info("=== 准备调用 Coze API ===")
        logger.info("开始处理人脸替换...")
        
        # 调用 Coze API 进行人脸替换
        result_url = process_face_swap(face_image, base_image)
        logger.info(f"人脸替换完成，结果URL: {result_url}")
        
        response_data = {
            'success': True,
            'result_url': result_url
        }
        logger.info(f"发送响应: {json.dumps(response_data, indent=2)}")
        
        return jsonify(response_data)
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e)
        }
        logger.error(f"处理过程中出现错误: {str(e)}")
        logger.error(f"发送错误响应: {json.dumps(error_response, indent=2)}")
        return jsonify(error_response), 500