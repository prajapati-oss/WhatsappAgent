import os
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
print(ACCESS_TOKEN,PHONE_NUMBER_ID)