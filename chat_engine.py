from groq import Groq
from groq.types.chat import chat_completion
import get_key

def completion(key, model, conversation_history):
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model=model
    )
    return chat_completion

def stream_completion(key, model, conversation_history):
    client = Groq(api_key=key)
    stream = client.chat.completions.create(
        messages=conversation_history,
        model=model,
        stream=True
    )

    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")

# old
def new_chat():
    key = get_key.get_api_key()
    client = Groq(
    api_key=key,
    )
    conversation_history = []
    while True:
        print("user: ")
        user_message = input()
        conversation_history.append({"role": "user", "content": user_message})
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="llama3-8b-8192",
        )
        print(chat_completion.choices[0].message.content)
