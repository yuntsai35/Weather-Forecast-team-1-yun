from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from controller import router as weather_router

app=FastAPI()

app.mount("/page", StaticFiles(directory="page"), name="page")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./page/index.html", media_type="text/html")

app.include_router(weather_router)