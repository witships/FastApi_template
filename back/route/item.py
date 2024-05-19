from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from sqlalchemy import desc
from pydantic import BaseModel
from model import Todo


# db接続
def get_db(request: Request):
    return request.state.db


# モデル
Item = Todo

# 共通メタデータ
router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "なし"}},
)


# スキーマ
class ItemModel(BaseModel):
    title: str
    done: bool


# router
@router.get("/", description="全件取得", summary="全件取得")
def read_all(db: Session = Depends(get_db)):
    item = db.query(Item).all()
    return item


@router.get("/{item_id}/", description="IDから1件取得", summary="IDから1件取得")
def read_one(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        return item
    else:
        return f"ID{item_id}は存在しません"


@router.post("/", description="新規作成", summary="新規作成")
def create_item(req: ItemModel, db: Session = Depends(get_db)):
    new_item = Todo(title=req.title, done=req.done)
    db.add(new_item)
    db.commit()
    new_item = db.query(Item).order_by(desc(Item.id)).first()
    return new_item


@router.put("/{item_id}", description="更新・上書き", summary="更新・上書き")
def update_item(item_id: int, req: ItemModel, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        item.title = req.title
        item.done = req.done
        db.commit()
        update_item = db.query(Item).filter(Item.id == item_id).first()
        return update_item
    else:
        return f"ID{item_id}は存在しません"


@router.delete("/{item_id}", description="削除", summary="削除")
def delete_item(item_id: int, req: ItemModel, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return f"ID{item_id}を削除しました"
    else:
        return f"ID{item_id}は存在しません"
