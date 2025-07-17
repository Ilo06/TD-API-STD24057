import json
from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from typing import List

app = FastAPI()


class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str


events_store: List[EventModel] = []

def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted


@app.get("/")
def root(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != "12345678":
        return Response(content="Unauthorized", status_code=401)
    else:
        with open("welcome.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return Response(content=html_content, status_code=200, media_type="text/html")

@app.get("/hello")
def hello(request:Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers not in ["text/plain", "text/html"]:
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    return JSONResponse(content="Hello world", status_code=200)


@app.get("/events")
def events(request:Request):
    return {"events": serialized_stored_events()}

@app.post("/events")
def post_event(event: list[EventModel]):
    events_store.extend(event)
    return {"message": serialized_stored_events()}

@app.put("/events")
def update_events(events: List[EventModel]) :
    for event in events:
        for stored_event in events_store:
            if event.name == stored_event.name:
                stored_event.name = event.name
                stored_event.description = event.description
                stored_event.start_date = event.start_date
                stored_event.end_date = event.end_date

    return {"events": serialized_stored_events()}



@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("notFound.html", "r", encoding="utf-8") as file:
        html_content = file.read()
        return Response(status_code=404, media_type="text/html", content=html_content)