import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import time


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

chat=model.start_chat(history=[])
with open('chat.txt','r') as file:
    response=chat.send_message('''I will give a conversation of two persons person1 and person2, analyse it and respond like person2 ,and
                                continue the given conversation as person2 with an appropriate answer,here is the conversation,don't write person2 just give reply'''+file.read())
def reply(message):
        response=chat.send_message(message)
        return response.text



