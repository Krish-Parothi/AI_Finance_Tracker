import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["finance_db"]
collection = db["expenses"]

async def get_recent_expenses(user_id: str):
    cursor = collection.find({"user_id": user_id}).sort("date", -1).limit(50)
    return [exp async for exp in cursor]

async def get_category_totals(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
    ]
    cursor = collection.aggregate(pipeline)
    return {doc["_id"]: doc["total"] async for doc in cursor}

async def get_hourly_distribution(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": {"$hour": "$date"}, "count": {"$sum": 1}}},
    ]
    cursor = collection.aggregate(pipeline)
    return {doc["_id"]: doc["count"] async for doc in cursor}

async def get_weekly_distribution(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": {"$dayOfWeek": "$date"}, "count": {"$sum": 1}}},
    ]
    cursor = collection.aggregate(pipeline)
    return {doc["_id"]: doc["count"] async for doc in cursor}
