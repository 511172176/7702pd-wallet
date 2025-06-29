import requests

domain = "blast-pools.pages.dev"
res = requests.post("http://localhost:3000/check", json={"address": domain})

print("✅ 狀態碼：", res.status_code)
print("✅ 回傳內容：", res.text)  # 不用 .json()，直接看純文字
