import os
import requests

def get_user_location(api_key):
    url = f"https://restapi.amap.com/v3/ip?key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':
        latitude = data['latt']
        longitude = data['longt']
        return latitude, longitude
    else:
        print("获取位置失败")
        return None, None

def get_city_name(latitude, longitude, api_key):
    url = f"https://restapi.amap.com/v3/geocode/regeo?key={api_key}&location={longitude},{latitude}&poitype=&radius=1000&extensions=all"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':
        city = data['regeocode']['addressComponent']['city']
        return city
    else:
        print("获取城市名称失败")
        return None

# 定义获取天气的函数
def get_weather(city):
    # 这里添加获取天气的逻辑
    pass  # 替换为实际的天气获取代码

def weather_report():
    api_key = os.environ.get("API_KEY")  # 从环境变量获取 API_KEY
    latitude, longitude = get_user_location(api_key)
    
    if latitude and longitude:
        city = get_city_name(latitude, longitude, api_key)
        
        if city:
            weather = get_weather(city)  # 你的天气获取函数
            print(f"{city} 天气信息： {weather}")
            # 发送消息的逻辑可以在这里添加

# 使用你的高德 API 密钥
weather_report()