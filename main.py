import os
import time
import requests
import scratchattach as scratch3
from threading import Thread
from flask import Flask

# --- Flask（サーバー機能：Renderスリープ防止用） ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive_loop():
    my_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not my_url:
        print("警告: RENDER_EXTERNAL_URL が設定されていないため、自動スリープ防止が働きません。")
        return
        
    while True:
        time.sleep(600)
        try:
            requests.get(my_url)
            print("セルフウェイクアップ成功！サーバーの生存を確認しました。")
        except Exception as e:
            print(f"セルフウェイクアップ失敗: {e}")

# --- 47都道府県の緯度経度・気象庁地域コードのリスト ---
# 気象庁のデータ（1次細分区域コードなど）を基準にマッピングしています
prefectures = [
    {"name": "北海道", "lat": 43.0642, "lon": 141.3469, "jma_code": "016000"}, # 石狩（札幌）
    {"name": "青森県", "lat": 40.8244, "lon": 140.7400, "jma_code": "020000"}, # 青森
    {"name": "岩手県", "lat": 39.7036, "lon": 141.1525, "jma_code": "030000"}, # 盛岡
    {"name": "宮城県", "lat": 38.2682, "lon": 140.8694, "jma_code": "040000"}, # 仙台
    {"name": "秋田県", "lat": 39.7186, "lon": 140.1025, "jma_code": "050000"}, # 秋田
    {"name": "山形県", "lat": 38.2404, "lon": 140.3633, "jma_code": "060000"}, # 山形
    {"name": "福島県", "lat": 37.7503, "lon": 140.4676, "jma_code": "070000"}, # 福島
    {"name": "茨城県", "lat": 36.3418, "lon": 140.4468, "jma_code": "080000"}, # 水戸
    {"name": "栃木県", "lat": 36.5658, "lon": 139.8836, "jma_code": "090000"}, # 宇都宮
    {"name": "群馬県", "lat": 36.3911, "lon": 139.0608, "jma_code": "100000"}, # 前橋
    {"name": "埼玉県", "lat": 35.8574, "lon": 139.6489, "jma_code": "110000"}, # さいたま
    {"name": "千葉県", "lat": 35.6051, "lon": 140.1233, "jma_code": "120000"}, # 千葉
    {"name": "東京都", "lat": 35.6895, "lon": 139.6917, "jma_code": "130000"}, # 東京
    {"name": "神奈川県", "lat": 35.4478, "lon": 139.6425, "jma_code": "140000"}, # 横浜
    {"name": "新潟県", "lat": 37.9022, "lon": 139.0236, "jma_code": "150000"}, # 新潟
    {"name": "富山県", "lat": 36.6953, "lon": 137.2113, "jma_code": "160000"}, # 富山
    {"name": "石川県", "lat": 36.5947, "lon": 136.6256, "jma_code": "170000"}, # 金沢
    {"name": "福井県", "lat": 36.0652, "lon": 136.2216, "jma_code": "180000"}, # 福井
    {"name": "山梨県", "lat": 35.6639, "lon": 138.5684, "jma_code": "190000"}, # 甲府
    {"name": "長野県", "lat": 36.6513, "lon": 138.1810, "jma_code": "200000"}, # 長野
    {"name": "岐阜県", "lat": 35.3912, "lon": 136.7223, "jma_code": "210000"}, # 岐阜
    {"name": "静岡県", "lat": 34.9771, "lon": 138.3831, "jma_code": "220000"}, # 静岡
    {"name": "愛知県", "lat": 35.1802, "lon": 136.9066, "jma_code": "230000"}, # 名古屋
    {"name": "三重県", "lat": 34.7303, "lon": 136.5086, "jma_code": "240000"}, # 津
    {"name": "滋賀県", "lat": 35.0045, "lon": 135.8686, "jma_code": "250000"}, # 大津
    {"name": "京都府", "lat": 35.0212, "lon": 135.7556, "jma_code": "260000"}, # 京都
    {"name": "大阪府", "lat": 34.6863, "lon": 135.5200, "jma_code": "270000"}, # 大阪
    {"name": "兵庫県", "lat": 34.6913, "lon": 135.1830, "jma_code": "280000"}, # 神戸
    {"name": "奈良県", "lat": 34.6853, "lon": 135.8327, "jma_code": "290000"}, # 奈良
    {"name": "和歌山県", "lat": 34.2260, "lon": 135.1675, "jma_code": "300000"}, # 和歌山
    {"name": "鳥取県", "lat": 35.5036, "lon": 134.2383, "jma_code": "310000"}, # 鳥取
    {"name": "島根県", "lat": 35.4722, "lon": 133.0505, "jma_code": "320000"}, # 松江
    {"name": "岡山県", "lat": 34.6618, "lon": 133.9344, "jma_code": "330000"}, # 岡山
    {"name": "広島県", "lat": 34.3966, "lon": 132.4596, "jma_code": "340000"}, # 広島
    {"name": "山口県", "lat": 34.1861, "lon": 131.4705, "jma_code": "350000"}, # 山口
    {"name": "徳島県", "lat": 34.0657, "lon": 134.5593, "jma_code": "360000"}, # 徳島
    {"name": "香川県", "lat": 34.3401, "lon": 134.0434, "jma_code": "370000"}, # 高松
    {"name": "愛媛県", "lat": 33.8417, "lon": 132.7657, "jma_code": "380000"}, # 松山
    {"name": "高知県", "lat": 33.5597, "lon": 133.5311, "jma_code": "390000"}, # 高知
    {"name": "福岡県", "lat": 33.6064, "lon": 130.4182, "jma_code": "400000"}, # 福岡
    {"name": "佐賀県", "lat": 33.2494, "lon": 130.2988, "jma_code": "410000"}, # 佐賀
    {"name": "長崎県", "lat": 32.7448, "lon": 129.8737, "jma_code": "420000"}, # 長崎
    {"name": "熊本県", "lat": 32.7905, "lon": 130.7416, "jma_code": "430000"}, # 熊本
    {"name": "大分県", "lat": 33.2382, "lon": 131.6126, "jma_code": "440000"}, # 大分
    {"name": "宮崎県", "lat": 31.9111, "lon": 131.4239, "jma_code": "450000"}, # 宮崎
    {"name": "鹿児島県", "lat": 31.5602, "lon": 130.5580, "jma_code": "460100"}, # 鹿児島
    {"name": "沖縄県", "lat": 26.2124, "lon": 127.6809, "jma_code": "471000"}  # 那覇
]

USERNAME = os.environ.get("SCRATCH_USERNAME")
PASSWORD = os.environ.get("SCRATCH_PASSWORD")
PROJECT_ID = os.environ.get("SCRATCH_PROJECT_ID")

# --- ① Open-Meteoのデータ取得ロジック (通常通り) ---
def get_open_meteo_data():
    lats = ",".join(str(p["lat"]) for p in prefectures)
    lons = ",".join(str(p["lon"]) for p in prefectures)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lats}&longitude={lons}&current_weather=true"
    
    weather_str = ""
    temp_str = ""
    try:
        response = requests.get(url).json()
        results = response if isinstance(response, list) else [response]
        for i, pref in enumerate(prefectures):
            try:
                data = results[i] if i < len(results) else {}
                current = data.get("current_weather", {})
                wmo_code = current.get("weathercode", 0)
                temp = round(current.get("temperature", 0))

                if wmo_code <= 1: weather_str += "1"
                elif wmo_code <= 3: weather_str += "2"
                elif (71 <= wmo_code <= 77) or (85 <= wmo_code <= 86): weather_str += "4"
                else: weather_str += "3"

                if temp < 0: temp = 0
                elif temp > 99: temp = 99
                temp_str += f"{temp:02d}"
            except Exception:
                weather_str += "2"
                temp_str += "15"
    except Exception:
        weather_str = "2" * 47
        temp_str = "15" * 47
    return weather_str + temp_str

# --- ② 気象庁(JMA)のデータ取得ロジック ---
def get_jma_data():
    weather_str = ""
    temp_str = ""
    
    # 負荷軽減のためセッションを使い回す
    session = requests.Session()
    
    for pref in prefectures:
        code = pref["jma_code"]
        # 気象庁の地域ごとの予報JSON
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{code}.json"
        try:
            res = session.get(url, timeout=5).json()
            
            # --- 天気コードの解析 ---
            # 直近の天気情報コードを取得
            jma_weather_code = res[0]["timeSeries"][0]["areas"][0]["weatherCodes"][0]
            w = int(jma_weather_code)
            
            # 気象庁コードを 1:晴れ, 2:曇り, 3:雨, 4:雪 にマッピング
            if w <= 101: weather_str += "1"     # 晴れ
            elif w <= 214: weather_str += "2"   # 曇り
            elif w <= 317: weather_str += "3"   # 雨
            else: weather_str += "4"            # 雪系統

            # --- 気温の解析 ---
            # 予報データの最初の気温、またはダミー
            temp_list = res[0]["timeSeries"][2]["areas"][0].get("temps", ["15"])
            temp = round(float(temp_list[0]))
            
            if temp < 0: temp = 0
            elif temp > 99: temp = 99
            temp_str += f"{temp:02d}"
            
        except Exception:
            # エラー時のフォールバック (曇り、15度)
            weather_str += "2"
            temp_str += "15"
            
        # 気象庁サーバーに優しくするためにわずかにウェイトを入れる
        time.sleep(0.05)
        
    return weather_str + temp_str

# --- メインループ ---
def weather_loop():
    while True:
        # 両方のデータを取得
        om_data = get_open_meteo_data()
        jma_data = get_jma_data()
        
        # 141文字の長さに調整
        if len(om_data) != 141: om_data = om_data[:141].ljust(141, "0")
        if len(jma_data) != 141: jma_data = jma_data[:141].ljust(141, "0")
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] OM データ: {om_data}")
        print(f"[{timestamp}] JMAデータ: {jma_data}")
        
        # Scratchへ送信
        try:
            session = scratch3.login(USERNAME, PASSWORD)
            conn = session.connect_cloud(PROJECT_ID)
            
            # 通常通り Open-Meteo を送信
            conn.set_var("weather_and_temp", om_data)
            time.sleep(1) # Scratchのサーバーに配慮して少し間を空ける
            
            # 気象庁データを新変数に送信
            conn.set_var("jma_weather_and_temp", jma_data)
            
            print("Both datasets successfully sent to Scratch!")
        except Exception as e:
            print(f"Scratchへの送信でエラーが発生しました: {e}")
            
        # 1時間（3600秒）待機
        time.sleep(3600)

if __name__ == "__main__":
    # スレッドを起動してWebキープアライブと並列処理
    t1 = Thread(target=run_server)
    t1.start()
    
    t2 = Thread(target=keep_alive_loop)
    t2.start()
    
    weather_loop()
