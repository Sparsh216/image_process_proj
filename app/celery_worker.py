from celery import Celery
from PIL import Image
import requests
from io import BytesIO
from database import SessionLocal
import crud
import models
import uuid
import csv
from tempfile import NamedTemporaryFile
import cloudinary.uploader
import logging
import os
import tempfile


# Configure logging
logger = logging.getLogger(__name__)
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def process_images(request_id: str, file):
    db = SessionLocal()

    # Read and validate CSV file
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(file.file.read())
    temp_file.seek(0)

    with open(temp_file.name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            serial_number = row['Serial Number']
            product_name = row['Product Name']
            input_image_urls = row['Input Image Urls']
            product = crud.create_product(db, request_id, serial_number, product_name, input_image_urls)
            
            # Process each image
            input_urls = input_image_urls.split(',')
            output_urls = []
            for url in input_urls:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                output = BytesIO()
                img.save(output, format='JPEG', quality=50)
                output.seek(0)

                # Upload to Cloudinary
                try:
                    upload_result = cloudinary.uploader.upload(output, folder="processed_images/")
                    output_url = upload_result['url']
                    output_urls.append(output_url)
                except cloudinary.exceptions.Error as e:
                    logger.error(f"Cloudinary upload error: {e}")
                    # Handle the error as needed (e.g., mark product as failed, retry, etc.)

            crud.update_product_output_urls(db, product.id, ','.join(output_urls))

    # Update request status and output CSV URL
    output_csv_url = generate_output_csv(request_id, db)
    crud.update_request_status(db, request_id, "completed", output_csv_url)

    # Commit all changes
    db.commit()

    # Close the database session
    db.close()

def generate_output_csv(request_id, db):
    # Generate output CSV locally
    products = db.query(models.Product).filter(models.Product.request_id == request_id).all()
    
    # Create a temporary folder if it doesn't exist
    temp_folder = os.path.join(os.getcwd(), 'temp_output_csv')
    os.makedirs(temp_folder, exist_ok=True)
    
    # Create a temporary CSV file
    output_file_path = os.path.join(temp_folder, 'output.csv')
    with open(output_file_path, 'w', newline='') as output_file:
        fieldnames = ['S. No.', 'Product Name', 'Input Image Urls', 'Output Image Urls']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            writer.writerow({
                'S. No.': product.serial_number,
                'Product Name': product.product_name,
                'Input Image Urls': product.input_image_urls,
                'Output Image Urls': product.output_image_urls
            })

    return output_file_path