from dotenv import load_dotenv
import os

load_dotenv()

dev = True


if dev:
    ACCOUNT_SERVER_URL=os.getenv("ACCOUNT_SERVER_URL")
    HOSPITAL_SERVER_URL=os.getenv("HOSPITAL_SERVER_URL")
    TIME_TABLE_SERVER_URL=os.getenv("TIME_TABLE_SERVER_URL")

    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    ACCOUNT_SERVER_URL=os.getenv("ACCOUNT_SERVER_URL_TEST")
    HOSPITAL_SERVER_URL=os.getenv("HOSPITAL_SERVER_URL_TEST")
    TIME_TABLE_SERVER_URL=os.getenv("TIME_TABLE_SERVER_URL_TEST")
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")

ES_HOST = os.getenv("ES_HOST")

ACCOUNT_SERVICE_TOKEN=os.getenv("ACCOUNT_SERVICE_TOKEN")
HOSPITAL_SERVICE_TOKEN=os.getenv("HOSPITAL_SERVICE_TOKEN")
DOCUMENT_SERVICE_TOKEN=os.getenv("DOCUMENT_SERVICE_TOKEN")
TIME_TABLE_SERVICE_TOKEN=os.getenv("TIME_TABLE_SERVICE_TOKEN")

list_available_tokens = []
list_available_tokens.append(ACCOUNT_SERVICE_TOKEN)
list_available_tokens.append(HOSPITAL_SERVICE_TOKEN)
list_available_tokens.append(DOCUMENT_SERVICE_TOKEN)
list_available_tokens.append(TIME_TABLE_SERVICE_TOKEN)
print(f"Database URL: {DATABASE_URL}")

