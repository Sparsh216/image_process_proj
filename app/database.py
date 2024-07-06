from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from urllib.parse import quote_plus

# Assuming your original SQLALCHEMY_DATABASE_URL
password = "P@ssword"
encoded_password = quote_plus(password)

# Construct the URL with the encoded password
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost/image_processing"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)