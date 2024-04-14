from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from os import environ
from socket import gethostbyname

#### IMPORTS: DB ####
import app.config.db as db_config
import databases
import sqlalchemy


# Initialize API
api = FastAPI()


class Item(BaseModel):
    text: str


# DATABASE #
database = databases.Database(db_config.DB_URL)
db_engine = sqlalchemy.create_engine(db_config.DB_URL)
metadata = sqlalchemy.MetaData()
# DATABASE #


# TEMPLATING #
templates = Jinja2Templates(directory="app/html")
# TEMPLATING #


## VARS ##
USE_DATABASE = environ.get("USE_DATABASE", True)
ENV_HOSTNAME = environ.get("HOSTNAME", "default-hostname-value")
ENV_IP = gethostbyname(ENV_HOSTNAME)
SECURE_PASSWORD_1 = environ.get("SECURE_PASSWORD_1", "default-secure-password-1-value")
SECURE_PASSWORD_2 = environ.get("SECURE_PASSWORD_2", "default-secure-password-2-value")
CUSTOM_HEADERS = {
    "X-App-Header": "k8s-app-demo",
    "Content-Language": "en-US",
    "Content-Type": "application/json",
}
## VARS ##


@api.on_event("startup")
async def startup():
    if USE_DATABASE is True:
        if not database.is_connected:
            print("INFO:\t   Connecting to Database")
            await database.connect()
            print("INFO:\t   Connected to Database")


@api.on_event("shutdown")
async def shutdown():
    if USE_DATABASE is True:
        if database.is_connected:
            await database.disconnect()
            print("INFO:\t   Disconnected from Database")


@api.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api.api_route("/private/hostname", methods=["GET", "HEAD"])
def hostname():
    content = {"hostname": ENV_HOSTNAME}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.api_route("/private/ip", methods=["GET", "HEAD"])
def ip():
    content = {"ip": ENV_IP}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/private/db")
def liveness():
    content = {"is-db-used": USE_DATABASE}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/health/liveness")
def liveness():
    content = {"state": "ALIVE"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/health/readiness")
def readiness():
    content = {"state": "READY"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.get("/secrets")
def readiness():
    content = {
        "secure-password-1": SECURE_PASSWORD_1,
        "secure-password-2": SECURE_PASSWORD_2,
    }
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)


@api.post("/publisher")
async def publisher(data: Item):
    content = {"message": f"{data.text}"}
    return JSONResponse(content=content, headers=CUSTOM_HEADERS)
