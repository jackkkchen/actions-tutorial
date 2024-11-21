import os
import requests
import json
from bs4 import BeautifulSoup



# APP_ID = "wxee3337b1f84a8bd9"
# APP_SECRET = "653c58f4f8f83d067c7364bd51835e9a"
# OPEN_ID = "o90ob6QvNAc4xyOC0V1pj_Tnh54k"
# TEMPLATE_ID = "tsqTLBMJT_b_3igmh07DWkf-i_vhskWyhwNlZYxYmHc"
# API_KEY = "9dbb5a4f2e1e0536bc4f7de6e362ca61"

# # 使用直接定义的变量
# appID = APP_ID
# appSecret = APP_SECRET
# openId = OPEN_ID
# weather_template_id = TEMPLATE_ID
# api_key = API_KEY  # 高德 API 密钥


# 从环境变量获取 API 密钥
appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
openId = os.environ.get("OPEN_ID")
weather_template_id = os.environ.get("TEMPLATE_ID")
api_key = os.environ.get("API_KEY")  # 高德 API 密钥

def get_current_city():
    # 使用高德地图 API 获取当前城市
    url = f"https://restapi.amap.com/v3/ip?key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    print(f"API Response: {data}")  # 输出 API 返回的数据
    
    if data['status'] == '1':
        # 直接从返回的数据中获取省份和城市
        province = data['province']
        city = data['city']
        return city, province
    else:
        print(f"获取当前城市失败: {data['info']}")
        return None, None

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

    # 获取省份的拼音
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
                    # 获取这一行的所有单元格
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

if __name__ == '__main__':
    current_city, current_province = get_current_city()
    if current_city:
        print(f"当前城市: {current_city}, 当前省份: {current_province}")
        weather_info = get_weather(current_city, current_province)
        if weather_info:
            print(f"天气信息：{weather_info}")
        else:
            print("未能获取天气信息")
    else:
        print("未能获取当前城市")

# def get_daily_love():
#     url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
#     r = requests.get(url)
#     all_dict = json.loads(r.text)
#     sentence = all_dict['returnObj'][0]
#     return sentence

def send_weather(access_token, weather):
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
        "touser": openId.strip(),
        "template_id": weather_template_id.strip(),
        "url": "https://weather.cma.cn/",  # 添加中国气象网链接
        "data": template_data
    }
    
    # 打印完整的请求数据
    print("\n完整的请求数据：")
    print(json.dumps(body, ensure_ascii=False, indent=2))
    
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    
    try:
        response = requests.post(url, json.dumps(body))
        result = response.json()
        
        print("\n请求URL:", url)
        print("HTTP状态码:", response.status_code)
        print("响应头:", dict(response.headers))
        print("响应内容:", json.dumps(result, ensure_ascii=False, indent=2))
        
        if result.get('errcode') == 0:
            print("发送成功！")
        else:
            print(f"发送失败！错误码：{result.get('errcode')}, 错误信息：{result.get('errmsg')}")
            
            # 检查模板ID
            print(f"\n当前使用的模板ID: {weather_template_id}")
            print("请确认该ID与微信公众平台的模板ID是否一致")
            
            # 检查数据字段
            print("\n模板数据字段检查:")
            for key in template_data:
                print(f"- {key}: {template_data[key]['value']}")
            
    except Exception as e:
        print(f"发送请求时出错: {str(e)}")

def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token

def weather_report():
    access_token = get_access_token()
    current_city, current_province = get_current_city()
    
    if current_city:
        weather = get_weather(current_city, current_province)
        if weather:
            print(f"天气信息：{weather}")
            send_weather(access_token, weather)
        else:
            print("未能获取天气信息")
    else:
        print("未能获取当前城市")

if __name__ == '__main__':
    weather_report()