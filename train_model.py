import json
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from features import extract_features

# 讀取 config.json
with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

blacklist = data["blacklist"]

# 特徵擷取
X = [extract_features(domain) for domain in blacklist]

# 建立模型
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)

# 儲存模型
joblib.dump(model, "blacklist_model.joblib")
print("✅ 模型訓練完成，使用特徵數量：", len(X[0]))
