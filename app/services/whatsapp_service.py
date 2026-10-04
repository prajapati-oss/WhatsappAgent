import os
import logging
import requests

from dotenv import load_dotenv


# =========================================================
# LOAD ENV VARIABLES
# =========================================================

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
print("\n===== WHATSAPP CONFIG =====")
print("PHONE_NUMBER_ID:", PHONE_NUMBER_ID)
print("TOKEN PREFIX:", ACCESS_TOKEN[:25] if ACCESS_TOKEN else None)
print("==========================\n")

# =========================================================
# LOGGING CONFIG
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# ENV VARIABLES
# =========================================================

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")


if not ACCESS_TOKEN:
    raise ValueError(
        "❌ WHATSAPP_ACCESS_TOKEN not found in .env"
    )

if not PHONE_NUMBER_ID:
    raise ValueError(
        "❌ WHATSAPP_PHONE_NUMBER_ID not found in .env"
    )


# =========================================================
# WHATSAPP API URL
# =========================================================

WHATSAPP_API_URL = (
    f"https://graph.facebook.com/v22.0/"
    f"{PHONE_NUMBER_ID}/messages"
)


# =========================================================
# WHATSAPP SERVICE
# =========================================================

class WhatsAppService:

    @staticmethod
    def send_text_message(
        to_phone_number: str,
        message: str
    ):
        """
        Send WhatsApp text message.
        """

        try:

            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            response = requests.post(
                WHATSAPP_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )

            response_data = response.json()

            # =================================================
            # SUCCESS
            # =================================================

            if response.status_code == 200:

                logger.info(
                    f"✅ Message sent successfully "
                    f"to {to_phone_number}"
                )

                return {
                    "success": True,
                    "data": response_data
                }

            # =================================================
            # FAILURE
            # =================================================

            logger.error(
                f"❌ WhatsApp API Error: {response_data}"
            )

            return {
                "success": False,
                "error": response_data
            }

        except requests.exceptions.Timeout:

            logger.error("❌ WhatsApp API timeout")

            return {
                "success": False,
                "error": "Request timeout"
            }

        except requests.exceptions.RequestException as e:

            logger.error(
                f"❌ Request failed: {str(e)}"
            )

            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:

            logger.error(
                f"❌ Unexpected error: {str(e)}"
            )

            return {
                "success": False,
                "error": str(e)
            }
whatsapp_service = WhatsAppService()