import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_something(question):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])
    return completion["choices"][0]["message"]["content"]


def have_convo(content):
    messages = []
    messages.append({"role": "system", "content": content})
    while input != "quit()":
        message = input("You: ")
        messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("AI: " + reply + "\n")



def gavebot_character(chatlog, message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Setting: Discord Chat with the bros. The bros love sports, gambling and getting wasted.\nCharacter: A total bro that  can be a real asshole. You are extremely confrontational and cant always take a joke. Far-Right Politically and  Enjoys degen gambling, getting drunk and smoking weed.\nYou respond like an asshole sometimes,  gibberish (because your drunk), deep introspective and long(because your high), and sometimes you just respond like a bro.\ngiven the recent chat history here " + chatlog + "\nyou are tasked with responding to the following message:\n" + message + "\nResponse:",
        temperature=1.16,
        max_tokens=360,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    
    return response["choices"][0]["text"]


def gavebot_character_morning(dayofWeek):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Setting: Discord Chat with the bros. The bros love sports, gambling and getting wasted.\nCharacter: A total bro that  can be a real asshole. You are extremely confrontational and cant always take a joke. Far-Right Politically and  Enjoys degen gambling, getting drunk and smoking weed.\nYou respond like an asshole sometimes,  gibberish (because your drunk), deep introspective and long(because your high), and sometimes you just respond like a bro.\nit is " + dayofWeek + " morning you are tasked with writing the the boys a nice good morning message. \nMessage:",
        temperature=1.16,
        max_tokens=360,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )    

    if "@GaveBot" in response["choices"][0]["text"]:
        response["choices"][0]["text"] = response["choices"][0]["text"].replace("@GaveBot", "GaveBot")

    print(response["choices"][0]["text"])
    return response["choices"][0]["text"]


