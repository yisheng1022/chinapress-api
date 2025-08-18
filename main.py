# from operator import le
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
from typing import Optional
from db import db
from datetime import datetime
import math
from typing import Optional

app = FastAPI()

# 所有 Collection 名稱（可擴充）
VALID_COLLECTIONS = {
    "JFJB": db["JFJB_daily_articles"],
    "GMB": db["GMB_daily_articles"]
}

@app.get("/search")
def search_articles(
    paper: str = Query(..., description="報紙代號[JFJB(解放軍報)、GMB(光明日報)]"),
    start_date: Optional[str] = Query(..., description="開始日期，格式 yyyy-mm-dd"),
    end_date: Optional[str] = Query(..., description="結束日期，格式 yyyy-mm-dd"),
    content_keyword: Optional[str] = Query(None, description="搜尋內文關鍵字"),
    skip: int = Query(0, ge=0,le=50),
    limit: int = Query(100,ge=1,le=100, description="最多回傳幾筆（預設 100 筆）")
):
    # 驗證報紙名稱
    if paper not in VALID_COLLECTIONS:
        return {"error": "Invalid paper name."}

    search_query = {}
    # 轉換日期
    if start_date & end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            search_query["Date"] = {"$gte": start_date, "$lte": end_date}
        except ValueError:
            return {"error": "日期格式錯誤，請使用 yyyy-mm-dd"}
    if content_keyword:
        search_query["Content"] = {"$regex": content_keyword, "$options": "i"}
    
    # 查詢資料
    collection = VALID_COLLECTIONS[paper] ##指定collection
    total_count = collection.count_documents(search_query) ##計算total result
    results = collection.find(search_query,{"_id": 0}).skip(skip).limit(limit)

    # 回傳 JSON
    encoded = jsonable_encoder(
        list(results),
        custom_encoder={float: lambda x: None if math.isnan(x) else x}
    )
    return {
        'total_result':total_count,
        'sk_page':skip,
        'data':encoded
    }
