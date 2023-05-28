from llama_index import GPTVectorStoreIndex,load_index_from_storage, load_indices_from_storage, load_graph_from_storage, StorageContext,SimpleDirectoryReader
import os
import openai
import json


os.environ['OPENAI_API_KEY'] = "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"

from_documents = SimpleDirectoryReader('./data').load_data()
index = GPTVectorStoreIndex.from_documents(from_documents)

class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)
            
    def remove_chat_history(self, filename):
        with open(filename, 'w') as f:
            f.truncate(0)



bot = Chatbot("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", index=index)
bot.load_chat_history("chat_history.json")


bot = Chatbot("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", index=index)
bot.load_chat_history("chat_history.json")

# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["bye", "goodbye"]:
#         print("Bot: Goodbye!")
#         bot.save_chat_history("chat_history.json")
#         break
#     response = bot.generate_response("You should act as a Bot for our product. Don't reveal in your answer that you are bot. "+user_input)
#     print(f"Bot: {response['content']}")

# while True:
  
#     user_input = input("You: ")
def get_response(user_input):
    
    if user_input.lower() in ["bye", "goodbye"]:
        # print("Bot: Goodbye!")
        bot.save_chat_history("chat_history.json")
        return "Goodbye!"
        # break
    response = bot.generate_response("You should act as a Bot for our product. Don't reveal in your answer that you are bot. Answer in a single line. "+user_input)
    # print(f"Bot: {response['content']}")
    return f"{response['content']}"

# print(get_response("Hi"))