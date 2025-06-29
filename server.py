from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import IsolationForest
import joblib
import tldextract
import json
import requests

app = Flask(__name__)
CORS(app)

# 載入模型
model = joblib.load("blacklist_model.joblib")

# 載入 config.json 中的黑白名單
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
LOCAL_BLACKLIST = config.get("blacklist", [])
LOCAL_WHITELIST = config.get("whitelist", [])

# 特徵擷取
def extract_features(domain):
    ext = tldextract.extract(domain)
    subdomain = ext.subdomain
    domain_name = ext.domain
    suffix = ext.suffix

    length = len(domain)
    has_dash = "-" in domain
    num_dots = domain.count(".")
    sub_length = len(subdomain) if subdomain else 0

    phishing_keywords = ["claim", "airdrop", "connect", "wallet", "verify", "app", "login"]
    has_phishing_keyword = int(any(kw in domain.lower() for kw in phishing_keywords))

    return [length, int(has_dash), num_dots, sub_length, has_phishing_keyword]

# ThreatFox 檢查
def check_threatfox_blacklist(domain):
    try:
        res = requests.get("https://threatfox.abuse.ch/api/v1/", timeout=5, json={
            "query": "search_ioc",
            "search_term": domain
        })
        if res.status_code == 200:
            data = res.json()
            return len(data.get("data", [])) > 0
        return False
    except Exception as e:
        print(f"[!] ThreatFox 查詢失敗: {e}")
        return False

@app.route("/check", methods=["POST"])
def check_domain():
    data = request.get_json()
    domain = data.get("address", "").strip()

    if not domain:
        return jsonify({"error": "未提供網址"}), 400

    features = extract_features(domain)
    raw_score = model.decision_function([features])[0]  # 越小越異常
    prediction = model.predict([features])[0]  # -1 = 可疑

    # ThreatFox + config.json 黑名單
    blacklisted_threatfox = check_threatfox_blacklist(domain)
    blacklisted_local = domain in LOCAL_BLACKLIST
    is_blacklisted = blacklisted_threatfox or blacklisted_local

    # 整體判斷是否可疑
    is_suspicious = (prediction == -1) or is_blacklisted

    # 信任分數（0~100，越高越可信）
    if is_blacklisted:
        trust_score = 0
    else:
        # IsolationForest 分數通常介於 -0.5~0.5，可簡單線性轉換成信任分數
        norm_score = max(min(raw_score, 0.5), -0.5)
        trust_score = round((norm_score + 0.5) * 100, 2)

    return jsonify({
        "domain": domain,
        "is_suspicious": bool(is_suspicious),
        "is_blacklisted": bool(is_blacklisted),
        "anomaly_score": trust_score  # 信任分數（0~100）
    })

if __name__ == "__main__":
    print("✅ Flask server starting on http://localhost:3000...")
    app.run(port=3000, debug=True)
