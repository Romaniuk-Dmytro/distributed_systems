import requests
import random
import uuid
from fastapi import FastAPI, Header, Response, Request
from fastapi.responses import JSONResponse
import hazelcast
import consul

app = FastAPI()
con = consul.Consul(host='localhost', port=8500)
con.agent.service.register('facade', port=8080)
queue_name = con.kv.get("queue_name")


client = hazelcast.HazelcastClient()
queue = client.get_queue(str(queue_name[1]['Value']))


def get_instances(n_array):
    instances = []
    for name in n_array:
        _, service = con.health.service(name, passing=True)
        instances.append(service[0]['Service']['Port'])
    return instances


async def get_messages():
    messages_instances = get_instances(['messages_1', 'messages_2'])
    node_port = messages_instances[random.randint(0, 1)]
    request = requests.get(f"http://127.0.0.1:{node_port}/messages/")
    return request.json()


async def get_log():
    logging_instances = get_instances(['logging_1', 'logging_2', 'logging_3'])
    node_port = logging_instances[random.randint(0, 2)]
    request = requests.get(f"http://127.0.0.1:{node_port}/logging/")
    return request.json()


async def post_to_log(data=None):
    logging_instances = get_instances(['logging_1', 'logging_2', 'logging_3'])
    node_port = logging_instances[random.randint(0, 2)]
    data['port'] = node_port
    request = requests.post(f"http://127.0.0.1:{node_port}/logging/", json=data)
    status = request.json()
    if status["status"] == "OK":
        return 200
    else:
        return "ERROR"


async def post_to_messages():
    messages_instances = get_instances(['messages_1', 'messages_2'])
    node_port = messages_instances[random.randint(0, 1)]
    requests.post(f"http://127.0.0.1:{node_port}/messages/", json={"port": node_port})


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
    queue.add(request_data["msg"])
    await post_to_messages()
    if post_log == 200:
        return "DONE"
    else:
        return "ERROR"
