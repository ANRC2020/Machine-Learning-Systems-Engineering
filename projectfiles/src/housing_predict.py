# housing_predict.py

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
import numpy as np
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from joblib import load
from redis import asyncio
import os
from redis.exceptions import ConnectionError, ResponseError
from dataclasses import astuple, dataclass

logger = logging.getLogger(__name__)

# Local Redis URL
LOCAL_REDIS_URL = "redis://localhost:6379/0"

global model

@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):

    logging.info("Starting up Lab3 API")

    # Load the Model on Startup
    global model
    model = load("model_pipeline.pkl")

    # Load the Redis Cache
    HOST_URL = os.getenv("REDIS_URL", LOCAL_REDIS_URL) # replace this according to the Lab Requirements
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)

    # We initialize the connection to Redis and declare that all keys in the
    # database will be prefixed with w255-cache-predict. Do not change this
    # prefix for the submission.
    FastAPICache.init(RedisBackend(redis), prefix="w255-cache-prediction")

    yield
    # We don't need a shutdown event for our system, but we could put something
    # here after the yield to deal with things during shutdown
    logging.info("Shutting down Lab3 API")

sub_application_housing_predict = FastAPI(lifespan=lifespan_mechanism)

@dataclass
class InputModel(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @field_validator('Longitude')
    @classmethod
    def check_longitude(cls, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError('Invalid value for Longitude')
        return longitude

    @field_validator('Latitude')
    @classmethod
    def valid_latitude(cls, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError('Invalid value for Latitude')
        return latitude

    model_config = ConfigDict(extra="forbid")

@dataclass
class ListInputModel(BaseModel):
    houses: list[InputModel]
    model_config = ConfigDict(extra="forbid")

@dataclass
class OutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: float

@dataclass
class ListOutputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predictions: list[float]

@sub_application_housing_predict.get("/health")
async def get_health():
    return {"time": str(datetime.now().isoformat())}

@sub_application_housing_predict.get("/hello") 
async def get_greeting(name: str):
    return {"message": f"Hello {name}"}

@sub_application_housing_predict.post("/predict", response_model=OutputModel)
@cache(expire=60)
async def get_prediction(input: InputModel) -> OutputModel:
    global model

    input_data = np.array([[input.MedInc, input.HouseAge, input.AveRooms, 
                             input.AveBedrms, input.Population, 
                             input.AveOccup, input.Latitude, 
                             input.Longitude]])
    
    predictions = model.predict(input_data)

    return {"prediction": predictions[0]}

@sub_application_housing_predict.post("/bulk-predict", response_model=ListOutputModel)
@cache(expire=60)
async def multi_predict(houses: ListInputModel) -> ListOutputModel:
    global model

    input_data = np.array(list(map(astuple, houses.houses)))

    predictions = model.predict(input_data)

    return {"predictions": predictions.tolist()}

