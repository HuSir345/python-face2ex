import requests
import random
from PIL import Image
import io
import base64
from app import app
import logging
import json

logger = logging.getLogger(__name__)

def compress_image(image_data, quality):
    """压缩图片"""
    img = Image.open(io.BytesIO(base64.b64decode(image_data)))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=int(quality * 100))
    return base64.b64encode(buffer.getvalue()).decode()

def upload_to_imagehub(image_data):
    """上传图片到 ImageHub"""
    url = 'https://www.imagehub.cc/api/1/upload'
    headers = {
        'X-API-Key': app.config['IMAGEHUB_API_KEY']
    }
    
    try:
        # 将base64转换为二进制图片数据
        image_binary = base64.b64decode(image_data)
        
        # 构建 multipart/form-data 请求
        files = {
            'source': ('image.jpg', image_binary, 'image/jpeg')
        }
        
        # 可选参数
        data = {
            'format': 'json',
            'nsfw': '0'
        }
        
        # 记录请求信息
        logger.info("=== ImageHub API Request ===")
        logger.info(f"URL: {url}")
        logger.info(f"Method: POST")
        logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        logger.info("FormData 内容:")
        logger.info(f"- source: {{ type: 'image/jpeg', name: 'image.jpg', size: '{len(image_binary)/1024/1024:.2f}MB' }}")
        
        # 发送请求
        response = requests.post(
            url=url,
            headers=headers,
            files=files,
            data=data
        )
        
        # 记录响应信息
        logger.info("=== ImageHub API Response ===")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        response_json = response.json()
        logger.info(f"Response Body: {json.dumps(response_json, indent=2)}")
        
        if response.status_code == 200:
            # 从响应中获取图片URL
            image_url = response_json.get('image', {}).get('url')
            if image_url:
                logger.info(f"Image uploaded successfully: {image_url}")
                return image_url
            else:
                raise Exception("No image URL in response")
        else:
            raise Exception(f"Upload failed with status {response.status_code}")
            
    except Exception as e:
        logger.error(f"Upload to ImageHub failed: {str(e)}")
        raise

def process_face_swap(face_image_data, base_image_data):
    """调用 Coze API 进行人脸替换"""
    url = 'https://api.coze.cn/v1/workflow/run'
    headers = {
        'Authorization': f'Bearer {app.config["COZE_API_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    
    try:
        # 先上传两张图片到 ImageHub
        logger.info("开始上传人脸图片到 ImageHub...")
        face_image_url = upload_to_imagehub(face_image_data)
        logger.info(f"人脸图片上传成功，URL: {face_image_url}")
        
        logger.info("开始上传被替换人脸图片到 ImageHub...")
        base_image_url = upload_to_imagehub(base_image_data)
        logger.info(f"被替换人脸图片上传成功，URL: {base_image_url}")
        
        # 构建 Coze API 请求数据
        data = {
            'workflow_id': app.config['COZE_WORKFLOW_ID'],
            'parameters': {
                'face_image': face_image_url,    # 使用 ImageHub 返回的 URL
                'base_image': base_image_url     # 使用 ImageHub 返回的 URL
            }
        }
        
        # 记录请求信息
        logger.info("=== Coze API Request ===")
        logger.info(f"URL: {url}")
        logger.info(f"Method: POST")
        logger.info(f"Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'}, indent=2)}")
        logger.info(f"Request Body: {json.dumps(data, indent=2)}")
        
        # 发送请求
        response = requests.post(
            url=url,
            headers=headers,
            json=data
        )
        
        # 记录响应信息
        logger.info("=== Coze API Response ===")
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        try:
            response_json = response.json()
            logger.info(f"Response Body: {json.dumps(response_json, indent=2)}")
            
            if response.status_code == 200 and response_json.get('code') == 0:
                # 解析返回的 data 字段（它是一个 JSON 字符串）
                result_data = json.loads(response_json['data'])
                return result_data['output']
            else:
                error_msg = response_json.get('msg', 'Unknown error')
                raise Exception(f"Face swap failed: {error_msg}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Raw response content: {response.text[:200]}...")
            raise Exception("Invalid JSON response from server")
            
    except Exception as e:
        logger.error(f"Process face swap failed: {str(e)}")
        raise 