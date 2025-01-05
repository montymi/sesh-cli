from pymongo import MongoClient
from datetime import datetime

class DBLibrarian:
    def __init__(self, client):
        self.client = client
        self.db = self.client['sesh_testing']  # Use your database name
        self.collection = self.db['conversationlogs']  # Use your collection name

    def date(self):
        return datetime.now().strftime("%Y%m%d-%H:%M:%S")


    def save(self, conversation, title, user):
        # Check if title is provided, otherwise generate one based on the current date
        if not title:
            title = self.date()
        
        # Prepare the document to be inserted or replaced with the given title
        document = {
            "title": title,
            "user": user,
            "conversation": []
        }
        
        # Iterate over the conversation list to add message_id and keep the existing information
        for message_id, message in enumerate(conversation):
            # Format message_id as required and add to the message dict
            formatted_message = {
                "message_id": {"$numberInt": str(message_id)},
                "role": message["role"],
                "content": message["content"]
            }
            document["conversation"].append(formatted_message)
        
        # Replace the document with the matching title, or insert it if it doesn't exist
        self.collection.replace_one({"title": title}, document, upsert=True)

    def load(self, title: str):
        # Check if title is not provided or is an empty string
        if not title:
            # Return default values: an empty dict with a conversation key set to an empty list
            return []
    
        conversation = self.collection.find_one({"title": title})
        if conversation:
            parsed_conversation = self.parse(conversation)
            return parsed_conversation
        else:
            # Return default values if no conversation is found
            return []

    def parse(self, log: dict):
        # Initialize an empty list with None to ensure the list has the correct size
        # and can handle message_id as index directly
        parsed_conversation = [None] * len(log['conversation'])
        
        for message in log['conversation']:
            # Extract the integer value of message_id
            message_id = int(message['message_id']['$numberInt'])
            # Use message_id as index and create a dict with 'role' and 'content'
            parsed_conversation[message_id] = {
                "role": message['role'],
                "content": message['content']
            }
        
        return parsed_conversation

    def list(self, user):
        conversations = self.collection.find({"user": user})
        # Extract the title (or another identifier) from each conversation
        titles = [conversation['title'] for conversation in conversations]
        return titles