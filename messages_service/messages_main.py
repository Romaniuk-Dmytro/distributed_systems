from fastapi import FastAPI, Header, Response, Request
from fastapi.responses import JSONResponse
import hazelcast

app = FastAPI()
client = hazelcast.HazelcastClient()
queue = client.get_queue("default")

node_memory_dict = {'messages_list': []}


def write_massages_to_memory(data):
    try:
        message_from_queue = queue.take().result()
        node_memory_dict['messages_list'] += [message_from_queue]
        print("\n", f"Message delivered to node: 127.0.0.1:{data['port']}",
              "\n", f'MESSAGE: {message_from_queue}', "\n")
        return "DONE"
    except:
        return "ERR"


@app.get("/messages/")
async def get_information() -> JSONResponse:
    return JSONResponse(node_memory_dict)


@app.post("/messages/")
async def get_messages_from_queue(request: Request):
    data = await request.json()
    write_massages_to_memory(data)
