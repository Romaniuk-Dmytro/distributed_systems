import requests
import random
import uuid
from fastapi import FastAPI, Header, Response, Request
from fastapi.responses import JSONResponse

app = FastAPI()
logging_instances = ['8082', '8083', '8084']


async def get_messages():
    request = requests.get("http://127.0.0.1:8081/messages/")
    return request.json()


async def get_log():
    node_port = logging_instances[random.randint(1, 3)]
    print(node_port)
    request = requests.get(f"http://127.0.0.1:{node_port}/logging/")
    return request.json()


async def post_to_log(data=None):
    node_port = logging_instances[random.randint(0, 2)]
    data['port'] = node_port
    request = requests.post(f"http://127.0.0.1:{node_port}/logging/", json=data)
    status = request.json()
    if status["status"] == "OK":
        return 200
    else:
        return "ERROR"


@app.get("/facade/")
async def get_facade() -> JSONResponse:
    messages_service = await get_messages()
    logging_service = await get_log()
    return JSONResponse(content={"messages_service": messages_service, "logging_service": logging_service})


@app.post("/facade/")
async def post_facade(request: Request):
    request_data = await request.json()
    id = uuid.uuid4()
    request_data["UUID"] = str(id)
    post_log = await post_to_log(request_data)
    if post_log == 200:
        return "DONE"
    else:
        return "ERROR"
