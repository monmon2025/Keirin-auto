from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# --- 将来ここに「KEIRIN.JP からの自動取得」処理を実装 ---
# 今は疎通確認のためダミー（モック）応答を返します。

def fetch_race_data_mock(date_str: str, place: str, race: str):
    # 例: date_str="2025-09-20", place="matsudo", race="9R"
    race_id = f"{date_str}_{place}{race}"
    # ここはテスト用の固定データ（あとで実データに差し替え）
    return {
        "race_id": race_id,
        "date": date_str,
        "place": place,
        "race": race,
        "start_time": "12:34",
        "odds": {
            "2f_1-3": 3.2,    # 2車複(1-3)
            "2t_1>3": 7.0,    # 2車単(1→3)
            "3t_1>3>2": 20.0  # 3連単(1→3→2)
        },
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "note": "mock data (later will be replaced with auto-fetch)"
    }

@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "service": "keirin-auto",
        "time": datetime.utcnow().isoformat() + "Z"
    })

@app.get("/race/<date_str>/<place>/<race>")
def get_race(date_str, place, race):
    # 形式チェックだけ簡単に
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "date must be YYYY-MM-DD"}), 400

    data = fetch_race_data_mock(date_str, place.lower(), race.upper())
    return jsonify(data)

# ルートの簡易案内
@app.get("/")
def root():
    return jsonify({
        "endpoints": [
            "/health",
            "/race/YYYY-MM-DD/<place>/<race>",
        ],
        "example": "/race/2025-09-20/matsudo/9R"
    })

if __name__ == "__main__":
    # ローカル実行用（Render では gunicorn を使います）
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
