from sqlalchemy.orm import Session
import models

def create_request(db: Session, request_id: str):
    db_request = models.Request(request_id=request_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_request_by_id(db: Session, request_id: str):
    return db.query(models.Request).filter(models.Request.request_id == request_id).first()

def update_request_status(db: Session, request_id: str, status: str, output_csv_url: str = None):
    db_request = get_request_by_id(db, request_id)
    db_request.status = status
    if output_csv_url:
        db_request.output_csv_url = output_csv_url
    db.commit()
    db.refresh(db_request)
    return db_request

def create_product(db: Session, request_id: str, serial_number: int, product_name: str, input_image_urls: str):
    db_product = models.Product(request_id=request_id, serial_number=serial_number, product_name=product_name, input_image_urls=input_image_urls)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_output_urls(db: Session, product_id: int, output_image_urls: str):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db_product.output_image_urls = output_image_urls
    db.commit()
    db.refresh(db_product)
    return db_product
