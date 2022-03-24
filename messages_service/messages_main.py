from fastapi import FastAPI, Header, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/messages/")
async def get_information() -> JSONResponse:
    return JSONResponse(content={"info": "messages service not implemented"})
