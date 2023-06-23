import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")


def ask_something(question):
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": question}])

    print(completion.choices[0].text)

    return completion


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