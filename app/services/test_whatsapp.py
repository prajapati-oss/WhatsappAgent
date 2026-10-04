from app.services.whatsapp_service import WhatsAppService


response = WhatsAppService.send_text_message(
    to_phone_number="919518241685",
    message="""Congratulations Ankit Maurya on your selection as a Data Analyst at Infosys! 🎉

Your hard work, dedication, and skills have truly paid off. This is a great achievement and the beginning of an exciting professional journey. Wishing you continued success, growth, and many more accomplishments in your career ahead.
your offer letter will come soon 
 best regard 
 Infosis.com"""
)

print(response)