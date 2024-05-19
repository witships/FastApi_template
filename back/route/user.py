from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from sqlalchemy import desc
from pydantic import BaseModel
from model import User


# db接続
def get_db(request: Request):
    return request.state.db


# モデル
Item = User

# 共通メタデータ
router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "なし"}},
)


# スキーマ
class ItemModel(BaseModel):
    name: str
    able: bool


# router
@router.get("/", description="全件取得", summary="全件取得")
def read_all(db: Session = Depends(get_db)):
    item = db.query(Item).all()
    return item


@router.get("/{user_id}/", description="IDから1件取得", summary="IDから1件取得")
def read_one(user_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == user_id).first()
    if item:
        return item
    else:
        return f"ID{user_id}は存在しません"


@router.post("/", description="新規作成", summary="新規作成")
def create_item(req: ItemModel, db: Session = Depends(get_db)):
    new_item = Item(name=req.name, able=req.able)
    db.add(new_item)
    db.commit()
    new_item = db.query(Item).order_by(desc(Item.id)).first()
    return new_item


@router.put("/{user_id}", description="更新・上書き", summary="更新・上書き")
def update_item(user_id: int, req: ItemModel, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == user_id).first()
    if item:
        item.name = req.name
        item.able = req.able
        db.commit()
        update_item = db.query(Item).filter(Item.id == user_id).first()
        return update_item
    else:
        return f"ID{user_id}は存在しません"


@router.delete("/{user_id}", description="削除", summary="削除")
def delete_item(user_id: int, req: ItemModel, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == user_id).first()
    if item:
        db.delete(item)
        db.commit()
        return f"ID{user_id}を削除しました"
    else:
        return f"ID{user_id}は存在しません"
