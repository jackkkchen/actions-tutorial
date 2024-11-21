from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import hashlib
import time
import requests
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# 你的微信公众号配置
TOKEN = "你的Token"  # 在公众号后台设置的Token
API_KEY = "你的高德地图API密钥"

def check_signature(signature, timestamp, nonce):
    """验证微信签名"""
    token = TOKEN
    temp = [token, timestamp, nonce]
    temp.sort()
    temp_str = ''.join(temp)
    hash_obj = hashlib.sha1(temp_str.encode('utf-8'))
    return hash_obj.hexdigest() == signature

@app.route('/wx', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 处理服务器配置验证
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        
        if check_signature(signature, timestamp, nonce):
            return echostr
        return 'Invalid signature'
        
    elif request.method == 'POST':
        try:
            xml_data = request.data
            logger.info(f"收到XML数据: {xml_data}")
            
            root = ET.fromstring(xml_data)
            msg_type = root.find('MsgType').text
            
            if msg_type == 'event':
                event = root.find('Event').text
                if event == 'LOCATION':
                    openid = root.find('FromUserName').text
                    latitude = float(root.find('Latitude').text)
                    longitude = float(root.find('Longitude').text)
                    
                    logger.info(f"收到位置信息 - OpenID: {openid}, 经度: {longitude}, 纬度: {latitude}")
                    
                    # 使用高德地图 API 反向地理编码
                    url = f"https://restapi.amap.com/v3/geocode/regeo?key={API_KEY}&location={longitude},{latitude}"
                    response = requests.get(url).json()
                    
                    if response['status'] == '1':
                        province = response['regeocode']['addressComponent']['province']
                        city = response['regeocode']['addressComponent']['city']
                        
                        logger.info(f"解析到地址 - 省份: {province}, 城市: {city}")
                        
                        # 更新数据库
                        update_user_location(openid, latitude, longitude, province, city)
                        logger.info(f"已更新用户 {openid} 的位置信息")
                    else:
                        logger.error(f"地理编码失败: {response}")
                        
            # 返回成功响应
            reply = "<xml><Return>success</Return><Message>OK</Message></xml>"
            response = make_response(reply)
            response.content_type = 'application/xml'
            return response
            
        except Exception as e:
            logger.error(f"处理消息时出错: {str(e)}", exc_info=True)
            return 'error'

if __name__ == '__main__':
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('wx_location.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    init_db()
    app.run(host='0.0.0.0', port=80) 