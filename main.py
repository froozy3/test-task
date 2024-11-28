from fastapi import FastAPI
from routes.missions import missions_router
from routes.cats import cats_router

app = FastAPI()
app.include_router(missions_router,prefix="/mission",tags=["mission"])
app.include_router(cats_router, prefix="/spy-cat", tags=['spy_cats'])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
