from dotenv import load_dotenv
import os
from openai import OpenAI
import discord
import subprocess
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import traceback
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
PREACH_PROMPT = "You are world class Hellfire and Brimstone preacher. You should preach to the user based on there input."

class GavebotPreacher:
    def __init__(self):
        self.client = OpenAI()
        self.llm = ChatOpenAI(openai_api_key=OPENAI_KEY)
        self.preach_prompt = ChatPromptTemplate.from_messages([("system", PREACH_PROMPT), 
        ("user", "{input}")])
    
    
    def preach_to_user(self, input):
        output_parser = StrOutputParser()
        chain = self.preach_prompt | self.llm | output_parser
        return chain.invoke({"input": input})
        
    def get_text_to_speech(self, input):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = self.client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input
        )
    
        # Save the audio stream to a file
        response.stream_to_file(speech_file_path)
        
                
        print(f"Audio extracted and saved to {speech_file_path}")
        
        print(speech_file_path)
        
        return speech_file_path
        
    async def playPreach(self, voice_client, channel, filename):
        audio_source = discord.FFmpegPCMAudio(filename)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=lambda e: print('Player error: %s' % e) if e else None)
            while voice_client.is_playing():
                await asyncio.sleep(1)  # Waitfor the song to finish
            await voice_client.disconnect()