from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from model import engine  # db作成

# DB用
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(request: Request):
    return request.state.db


app = FastAPI()

# アクセス許可
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ↑のorginsで指定するか[*]で全許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routeを外部化
from route import item, user

# import item
app.include_router(user.router)
app.include_router(item.router)


# リクエストの度に呼ばれるミドルウェア DB接続用のセッションインスタンスを作成
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


if __name__ == "__main__":
    import webbrowser, uvicorn

    url = "http://0.0.0.0:8000/docs"
    webbrowser.open(url, new=0, autoraise=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
