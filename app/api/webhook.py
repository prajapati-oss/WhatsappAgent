from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
import json
from app.handlers.message_handler import (
    message_handler
)

router = APIRouter()

# =========================================================
# CONFIG
# =========================================================

VERIFY_TOKEN = "my_verify_token"


# =========================================================
# WEBHOOK VERIFICATION
# =========================================================

@router.get("/")
async def verify_webhook(request: Request):
    """
    Meta webhook verification endpoint.
    """

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully")
        return PlainTextResponse(content=challenge, status_code=200)

    raise HTTPException(
        status_code=403,
        detail="Webhook verification failed")


# =========================================================
# RECEIVE WHATSAPP MESSAGES
# =========================================================

@router.post("/")
async def receive_message(request: Request):
    """
    Receives incoming WhatsApp messages from Meta webhook.
    """

    try:
        try:
            body = await request.json()
        except Exception: 
            return {"status": "invalid_json"}

        print("\n📩 Incoming Webhook Data:")
        print("\n================ WEBHOOK DATA ================\n")
        print(json.dumps(body, indent=2))
        print("\n=============================================\n")

        # =================================================
        # SAFETY CHECKS
        # =================================================

        entry = body.get("entry", [])

        if not entry:
            return {"status": "no_entry_found"}

        changes = entry[0].get("changes", [])

        if not changes:
            return {"status": "no_changes_found"}

        value = changes[0].get("value", {})
        if "messages" not in value:
            print("ℹ️ Non-message webhook event received")
            return {"status": "ignored"}


        messages = value.get("messages")

        if not messages:
            return {"status": "no_message_found"}

        # =================================================
        # EXTRACT USER DATA
        # =================================================

        message = messages[0]

        user_number = message.get("from")
        message_id = message.get("id")
        message_type = message.get("type")

        print(f"\n👤 User: {user_number}")
        print(f"🆔 Message ID: {message_id}")
        print(f"📦 Message Type: {message_type}")

        # =================================================
        # HANDLE TEXT MESSAGE
        # =================================================

        if message_type == "text":

            user_text = message["text"]["body"]

            print(f"💬 User Message: {user_text}")

            # =============================================
            # TODO:
            # 1. Save message in DB
            # 2. Fetch user memory
            # 3. Call AI model
            # 4. Generate response
            # 5. Send WhatsApp reply
            # =============================================

            result = await message_handler.process_message(
    body
)

            print("\n🤖 MESSAGE HANDLER RESULT:")
            print(json.dumps(result, indent=2))

        # =================================================
        # HANDLE AUDIO MESSAGE
        # =================================================

        elif message_type == "audio":

            audio_id = message["audio"]["id"]

            print(f"🎤 Audio Message ID: {audio_id}")

            # TODO:
            # Download audio
            # Transcribe audio
            # Send to AI

        # =================================================
        # HANDLE IMAGE MESSAGE
        # =================================================

        elif message_type == "image":

            image_id = message["image"]["id"]

            print(f"🖼️ Image Message ID: {image_id}")

        # =================================================
        # UNKNOWN MESSAGE TYPE
        # =================================================

        else:
            print(f"⚠️ Unsupported message type: {message_type}")

        return {
            "status": "success"
        }

    except Exception as e:
      print("ERROR:", str(e))
      raise HTTPException(
        status_code=500,
        detail=str(e)
    )