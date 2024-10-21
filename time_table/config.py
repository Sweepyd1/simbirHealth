from dotenv import load_dotenv
import os

load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")

ACCOUNT_SERVER_URL=os.getenv("ACCOUNT_SERVER_URL")
HOSPITAL_SERVER_URL=os.getenv("HOSPITAL_SERVER_URL")
DOCUMENT_SERVER_URL=os.getenv("DOCUMENT_SERVER_URL")


print(f"Database URL: {DATABASE_URL}")

