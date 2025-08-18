# import_data.py
import pandas as pd
from pymongo.errors import BulkWriteError
from db import db  # 來自 db.py

# 定義資料來源：CSV 檔案路徑 ➜ Collection 名稱
data_sources = {
    "JFJB_daily_articles": "data/JFJB_combine.csv",
    "GMB_daily_articles": "data/xinhua_news.csv"
}

# 開始處理每一份報紙資料
for collection_name, filepath in data_sources.items():
    print(f"\n📥 正在匯入：{filepath} 到 collection：{collection_name}")

    # 讀取 CSV
    df = pd.read_csv(filepath,dtype='str')
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d")
    # 轉換為 list of dicts
    docs = df.to_dict(orient="records")

    collection = db[collection_name]

    try:
        # 批次匯入資料（unordered：遇到錯誤也會繼續匯入其他筆）
        collection.insert_many(docs, ordered=False)
        print(f"✅ {collection_name} 匯入完成：成功 {len(docs)} 筆，無重複")
    except BulkWriteError as e:
        inserted = len(docs) - len(e.details["writeErrors"])
        skipped = len(e.details["writeErrors"])
        print(f"⚠️ {collection_name} 匯入完成：成功 {inserted} 筆，跳過重複 {skipped} 筆")
