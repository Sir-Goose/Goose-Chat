from groq import Groq
from groq.types.chat import chat_completion

def completion(key, model, conversation_history):
    client = Groq(api_key=key)
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model=model
    )
    return chat_completion


# old
def new_chat():
    key = "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"
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
