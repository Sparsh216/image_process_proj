Upload API

Endpoint: POST /upload
Description: Uploads images and related data.
Parameters:
file: Image file (multipart/form-data)
product_name: String
serial_number: Integer

curl -X 'POST' \
  'http://localhost:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.csv;type=text/csv'

	
Response body

{
  "request_id": "041fc7ab-88db-4ebd-8f06-5468be422cdc"
}

Retrieve Product Data API

Endpoint: GET /products/{product_id}
Description: Retrieves product details by ID.
Parameters:
product_id: Integer (path parameter)

curl -X 'GET' \
  'http://localhost:8000/status/041fc7ab-88db-4ebd-8f06-5468be422cdc' \
  -H 'accept: application/json'

	
Response body

{
  "request_id": "041fc7ab-88db-4ebd-8f06-5468be422cdc",
  "status": "completed",
  "output_csv_url": "D:\\projects\\image_processing_application\\app\\temp_output_csv\\output.csv"
}
