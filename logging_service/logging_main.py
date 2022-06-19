from fastapi import FastAPI, Header, Response, Request
from fastapi.responses import JSONResponse
import hazelcast
import consul

app = FastAPI()
logging_info = {}

con = consul.Consul(host='localhost', port=8500)
con.agent.service.register('logging_3', port=8084)
map_name = con.kv.get("map_name")

client = hazelcast.HazelcastClient()
my_map = client.get_map(str(map_name[1]['Value'])).blocking()


@app.post("/logging/")
async def post_logging(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        logging_info[data['UUID']] = data['msg']
        print("\n", f"Message delivered to node: 127.0.0.1:{data['port']}",
              "\n", f'MESSAGES: {logging_info}', "\n")
        my_map.put(data['UUID'], data['msg'])
        return JSONResponse({"status": "OK"})
    except:
        return JSONResponse({"status": "ERR"})


@app.get("/logging/")
async def get_logging() -> JSONResponse:
    return JSONResponse({"all_messages": [x for x in my_map.values()]})
