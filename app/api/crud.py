from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse

def create_order(db: Session, order: schemas.Order):
    db_order = models.Order(status=order.status, items=order.items, amount=order.amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order 

def get_order(db: Session, order_id: id):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if db_order:
        return db_order
    else: 
        msg = {"message": f'Order id {order_id} not found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=msg)        

def delete_order(db: Session, order_id: id):
    order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if order:
        db.query(models.Order).filter(models.Order.order_id == order_id).delete()
        db.commit()
        return {"message": f'Order {order_id} is deleted'}
    else:
        msg = {"message": f'Order id {order_id} not found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=msg)
    
def update_order(db: Session, order_id: id, order_data: schemas.Order):
    find_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if find_order:
        if order_data.status:
            find_order.status = order_data.status
        if order_data.amount:
            find_order.amount = order_data.amount
        db.commit()
        db.refresh(find_order)
        return find_order
    else:
        msg = {"message": f'Order id {order_id} not found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=msg)        


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    data = db.query(models.Order).all()
    return data