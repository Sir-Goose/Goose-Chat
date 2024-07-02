import os
import datetime
import pickle
import json

class Conversation:
    def __init__(self, position, name="Chat"):
        self.conversation_history = []
        self.name = name
        if self.name == "Chat":
            self.name = f"Chat #{position}"
        self.creation_timestamp = datetime.datetime.now().timestamp()
        self.edit_timestamp = datetime.datetime.now().timestamp()
        self.position = position

    def update_timestamp(self):
        self.edit_timestamp = datetime.datetime.now().timestamp()

    def to_json(self):
        return json.dumps({
            'conversation_history': self.conversation_history,
            'name': self.name,
            'creation_timestamp': self.creation_timestamp,
            'edit_timestamp': self.edit_timestamp,
            'position': self.position
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        conversation = cls(data['position'], data['name'])
        conversation.conversation_history = data['conversation_history']
        conversation.creation_timestamp = data['creation_timestamp']
        conversation.edit_timestamp = data['edit_timestamp']
        return conversation

class Conversation_List:
    def __init__(self):
        self.chat_list = retrieve_chats()

    def add_chat(self, name="Chat"):
        length = len(self.chat_list)
        self.chat_list.append(Conversation(length, name))

def store_chats(chat_list):
    # Open a file in binary write mode
    with open('chats.pickle', 'wb') as f:
        # Serialize the object and write it to the file
        pickle.dump([chat.to_json() for chat in chat_list], f)

def retrieve_chats():
    loaded_data = []
    if os.path.isfile('chats.pickle'):
        # Open the file in binary read mode
        with open('chats.pickle', 'rb') as f:
            # Deserialize the object from the file
            json_list = pickle.load(f)
            loaded_data = [Conversation.from_json(json_str) for json_str in json_list]
    return loaded_data
