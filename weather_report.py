import os
import requests
import json
from bs4 import BeautifulSoup
import sys
import io
import locale

# 设置系统默认编码
if sys.platform.startswith('win'):
    # Windows 系统
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Chinese_China.UTF8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
else:
    # 类Unix系统
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

# 设置标准输出编码为 utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 直接定义变量
APP_ID = "wxee3337b1f84a8bd9"
APP_SECRET = "653c58f4f8f83d067c7364bd51835e9a"
OPEN_ID = "o90ob6QvNAc4xyOC0V1pj_Tnh54k,o90ob6VB3Cg0LZJyLTn7-oziGY7w"
TEMPLATE_ID = "tsqTLBMJT_b_3igmh07DWkf-i_vhskWyhwNlZYxYmHc"
API_KEY = "9dbb5a4f2e1e0536bc4f7de6e362ca61"

# 使用直接定义的变量
appID = APP_ID
appSecret = APP_SECRET
openId = OPEN_ID
weather_template_id = TEMPLATE_ID
api_key = API_KEY  # 高德 API 密钥

# 在文件开头添加用户城市映射
USER_CITY_MAPPING = {
    # 'o90ob6RMZnjpa26EfcIHQvrqBlh4': ('上海', '上海'),
    'o90ob6VB3Cg0LZJyLTn7-oziGY7w': ('中山市', '广东省'),
    # 'o90ob6cksje4isH_zyNVlviV-bvo': ('广州市', '广东省'),
    # 'o90ob6ZqOt8YTYZfrdH3tS0DxZv8': ('广州市', '广东省'),
    'o90ob6QvNAc4xyOC0V1pj_Tnh54k': ('珠海市', '广东省'),
}

# 从环境变量获取 API 密钥
# appID = os.environ.get("APP_ID")
# appSecret = os.environ.get("APP_SECRET")
# openId = os.environ.get("OPEN_ID")
# weather_template_id = os.environ.get("TEMPLATE_ID")
# api_key = os.environ.get("API_KEY")  # 高德 API 密钥

def get_current_city(user_id):
    """根据用户ID获取当前城市"""
    try:
        # 首先检查用户是否在映射表中
        if user_id in USER_CITY_MAPPING:
            city, province = USER_CITY_MAPPING[user_id]
            print(f"用户 {user_id} 使用映射城市: {province} {city}")
            return city, province
            
        # 检查是否在 GitHub Actions 环境中
        if os.environ.get('GITHUB_ACTIONS'):
            # 从环境变量获取城市信息
            default_city = os.environ.get('DEFAULT_CITY', '珠海市')
            default_province = os.environ.get('DEFAULT_PROVINCE', '广东省')
            print(f"GitHub Actions 环境，使用默认城市: {default_province} {default_city}")
            return default_city, default_province
            
        # 本地环境使用高德地图 API
        url = f"https://restapi.amap.com/v3/ip?key={api_key}"
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == '1' and data.get('city') and data.get('province'):
            province = data['province']
            city = data['city']
            print(f"用户 {user_id} 的城市信息: {province} {city}")
            return city, province
        else:
            print(f"无法获取位置信息，使用默认城市")
            return "珠海市", "广东省"
            
    except Exception as e:
        print(f"获取城市信息时出错: {str(e)}，使用默认城市")
        return "珠海市", "广东省"

def get_weather(my_city, my_province):
    # 省份名称到拼音的映射
    province_mapping = {
        "广东省": "guangdong",
        "北京市": "beijing",
        "上海市": "shanghai",
        "江苏省": "jiangsu",
        "浙江省": "zhejiang",
        "湖北省": "hubei",
        "湖南省": "hunan",
        "四川省": "sichuan",
        "陕西省": "shanxi",
        "福建省": "fujian",
        "海南省": "hainan",
        "新疆": "xinjiang",
        "内蒙古自治区": "neimenggu",
        "甘肃省": "gansu",
        "青海省": "qinghai",
        "宁夏回族自治区": "ningxia",
        "吉林省": "jilin",
        "黑龙江省": "heilongjiang",
        "安徽省": "anhui",
        "江西省": "jiangxi",
        "河南省": "henan",
        "山西省": "shanxi",
        "河北省": "hebei",
        "辽宁省": "liaoning",
        "天津市": "tianjin",
        "重庆市": "chongqing",
        "澳门特别行政区": "aomen",
        "香港特别行政区": "xianggang",
        "台湾省": "taiwan"
    }

    # 处理直辖市的特殊情况
    direct_cities = {
        '上海': 'shanghai',
        '北京': 'beijing',
        '天津': 'tianjin',
        '重庆': 'chongqing'
    }
    
    if my_city.replace('市', '') in direct_cities:
        province_pinyin = direct_cities[my_city.replace('市', '')]
    else:
        # 原有的省份映射逻辑
        province_pinyin = province_mapping.get(my_province)
        
    if not province_pinyin:
        print(f"未找到省份 {my_province} 的拼音映射")
        return None

    # 直接使用省份的 URL
    province_url = f"http://www.weather.com.cn/textFC/{province_pinyin}.shtml"
    
    # 打印 URL 和城市信息
    # print(f"正在查询: 省份={my_province}, 城市={my_city}")
    print(f"访问的URL: {province_url}")
    
    # 发送请求获取省份天气信息
    resp = requests.get(province_url)
    text = resp.content.decode("utf-8")
    soup = BeautifulSoup(text, 'html.parser')
    
    # 查找所有城市天气信息的表格
    div_conMidtab = soup.find("div", class_="conMidtab")
    
    if div_conMidtab is None:
        print("未找到天气数据")
        return None
        
    tables = div_conMidtab.find_all("table")
    
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all('td')
            if not cells:
                continue
                
            for cell in cells:
                cell_text = list(cell.stripped_strings)
                if cell_text and my_city.replace("市", "") in cell_text[0]:
                    # 获取这一的所有单元格
                    all_cells = row.find_all("td")
                    
                    try:
                        high_temp = list(all_cells[-5].stripped_strings)[0]
                        low_temp = list(all_cells[-2].stripped_strings)[0]
                        weather_typ_day = list(all_cells[-7].stripped_strings)[0]
                        weather_type_night = list(all_cells[-4].stripped_strings)[0]
                        wind_day = "".join(list(all_cells[-6].stripped_strings))
                        wind_night = "".join(list(all_cells[-3].stripped_strings))

                        temp = f"{low_temp}——{high_temp}摄氏度" if high_temp != "-" else f"{low_temp}摄氏度"
                        weather_typ = weather_typ_day if weather_typ_day != "-" else weather_type_night
                        wind = f"{wind_day}" if wind_day != "--" else f"{wind_night}"
                        
                        return cell_text[0], temp, weather_typ, wind
                    except Exception as e:
                        print(f"处理天气数据时出错: {str(e)}")
                        continue

    print(f"未找到 {my_city} 的天气信息")
    return None

def send_weather(access_token, weather_data=None):
    import datetime
    
    now = datetime.datetime.now()
    today = now.date()
    current_time = now.strftime("%H:%M")
    today_str = today.strftime("%Y年%m月%d日")
    
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "早上好"
    elif 12 <= hour < 18:
        greeting = "下午好"
    else:
        greeting = "晚上好"

    # 获取所有用户的 OPEN_ID
    open_id_list = openId.strip().split(',')
    
    for user_id in open_id_list:
        user_id = user_id.strip()
        # 获取用户所在城市
        city, province = get_current_city(user_id)
        
        if not city or not province:
            print(f"未能获取用户 {user_id} 的位置信息，跳过推送")
            continue
            
        # 获取该城市的天气信息
        weather = get_weather(city, province)
        
        if not weather:
            print(f"未能获取用户 {user_id} 所在城市 {city} 的天气信息")
            continue

        template_data = {
            "first": {
                "value": greeting,
                "color": "#1e90ff"
            },
            "date": {
                "value": f"现在是{today_str} {current_time}",
                "color": "#173177"
            },
            "region": {
                "value": weather[0],
                "color": "#173177"
            },
            "weather": {
                "value": weather[2],
                "color": "#173177"
            },
            "temp": {
                "value": weather[1],
                "color": "#ff0000"
            },
            "wind_dir": {
                "value": weather[3],
                "color": "#173177"
            },
            "remark": {
                "value": "愿你拥有美好的一天！",
                "color": "#1e90ff"
            }
        }

        body = {
            "touser": user_id,
            "template_id": weather_template_id.strip(),
            "url": "https://weather.cma.cn/",
            "data": template_data
        }
        
        url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
        
        try:
            response = requests.post(url, json.dumps(body))
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"发送成功！用户ID: {user_id}, 城市: {city}")
            else:
                print(f"发送失败！用户ID: {user_id}, 城市: {city}, 错误码：{result.get('errcode')}, 错误信息：{result.get('errmsg')}")
                
        except Exception as e:
            print(f"发送请求时出错，用户ID: {user_id}, 城市: {city}, 错误: {str(e)}")

def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token

def weather_report():
    print("开始执行天气预报程序...")
    
    access_token = get_access_token()
    if not access_token:
        print("获取 access_token 失败，终止执行")
        return
    print(f"成功获取 access_token")
    
    # 直接调用 send_weather，它会处理所有用户
    send_weather(access_token)
    
    print("天气预报程序执行完成")

if __name__ == '__main__':
    try:
        weather_report()
    except Exception as e:
        print(f"程序执行出错: {str(e)}")