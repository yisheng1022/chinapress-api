from db import db

collections = {
    "JFJB_daily_articles": db["JFJB_daily_articles"],
    "GMB_news_articles": db["GMB_daily_articles"]
}

for name, col in collections.items():
    col.create_index([("url", 1)], unique=True)
    print(f"✅ 建立索引成功：{name}（url）")