from fastapi import FastAPI, Header, Response, Request
from fastapi.responses import JSONResponse

app = FastAPI()
logging_info = {}


@app.post("/logging/")
async def post_logging(request: Request) -> JSONResponse:
    try:
        data = await request.json()
        logging_info[data['UUID']] = data['msg']
        print("\n", f'MESSAGES: {logging_info}', "\n")
        return JSONResponse({"status": "OK"})
    except:
        return JSONResponse({"status": "ERR"})


@app.get("/logging/")
async def get_logging() -> JSONResponse:
    return JSONResponse({"all_messages": [x for x in logging_info.values()]})
