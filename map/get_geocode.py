import requests
import json
import time

API_KEY = "e2af5ac6f39edf4b77e65f0774e0181d"

def geocode(address):
    url = f"https://restapi.amap.com/v3/geocode/geo?address={address}&key={API_KEY}"
    try:
        resp = requests.get(url, proxies={"http": None, "https": None})
        data = resp.json()
        if data["status"] == "1" and data["geocodes"]:
            location = data["geocodes"][0]["location"]  # 'lng,lat'
            lng, lat = map(float, location.split(','))
            return lng, lat
    except Exception as e:
        print(f"Error for address: {address} → {e}")
    return None, None

output = []

with open("error.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for i in range(0, 6, 2):
    name = lines[i]
    address = lines[i+1]
    lng, lat = geocode(address)
    if lng and lat:
        print(f"成功获取：{name} → ({lng}, {lat})")
        output.append({
            "name": name,
            "address": address,
            "lng": lng,
            "lat": lat
        })
    else:
        print(f"⚠️ 获取失败：{name}，地址：{address}")
    time.sleep(0.3)  # 避免触发限流

# 保存为 JSON
with open("home_code.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)