import asyncio
import typing as T
import uuid

# 3rd party
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, model_validator

# Type aliasing
Query = T.Union[
    T.Dict[str, T.Any],
    T.List[T.Dict[str, T.Any]]
]

# TODO : 나중에 redis 등으로
operation_status_cache = {}

app = FastAPI()


class QueryRequest(BaseModel):
    collection_name: str
    query: Query
    use_agg: bool = False

    @model_validator(mode='after')
    def validate_query_type(cls, values):
        query = values.get('query')
        use_agg = values.get('use_agg')

        if use_agg:
            if not isinstance(query, list):
                raise ValueError("When 'use_agg' is True, 'query' must be a list of aggregation stages.")
        else:
            if not isinstance(query, dict):
                raise ValueError("When 'use_agg' is False, 'query' must be a single query document (dict).")
        return values

async def perform_mongo_query(
    mongo_uri: str,
    db_name: str,
    collection_name: str,
    query: Query,
    operation_id: str,
    use_agg: bool = False,
):
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    try:
        if use_agg:
            cursor = collection.aggregate(query)
        else:
            cursor = collection.find(query)
        results = await cursor.to_list(length=None)
        operation_status_cache[operation_id] = {"status": "SUCCESS", "results": results}
    except Exception as e:
        operation_status_cache[operation_id] = {"status": "FAILED", "error": str(e)}
    finally:
        client.close()

@app.post("/initiate-query")
async def initiate_query(request: QueryRequest):
    mongo_uri = "mongodb://user:password@your_mongo_host:27017/your_auth_db"
    db_name = "mydatabase"

    operation_id = str(uuid.uuid4())
    operation_status_cache[operation_id] = {"status": "PENDING"}

    asyncio.create_task(
        perform_mongo_query(
            mongo_uri,
            db_name,
            request.collection_name,
            request.query,
            operation_id,
            request.use_agg
        )
    )

    return {"status": "INIITATED", "operation_id": operation_id}


@app.get("/operation-status/{operation_id}")
async def get_status(operation_id: str):
    status = operation_status_cache.get(operation_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Invalid operation ID")

    else:
        del operation_status_cache[operation_id]

    return JSONResponse(content=status)