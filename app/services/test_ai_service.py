from app.services.ai_service import AIService


memory = [
    {
        "role": "user",
        "content": "My name is Rakesh"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you Rakesh!"
    }
]


response = AIService.generate_response(
    user_message="What is my name?",
    memory=memory
)

print(response)