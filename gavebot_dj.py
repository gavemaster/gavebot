import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from moviepy.editor import *
import discord
import asyncio
from gm_logger import create_logger
import subprocess
from googleapiclient.discovery import build
import os
logger = create_logger("gavebot_dj")
class GavebotDJ:
    def __init__(self):
        self.queue = []
        self.current_index = 0

    def search_youtube(self, query):
        # Use your API key here
        api_key = "AIzaSyBWdy6bIJWoW5OLbCelqHB7oiQ90oePJdg"

        # Build a YouTube client
        youtube = build("youtube", "v3", developerKey=api_key)

        # Search request
        request = youtube.search().list(part="snippet", q=query, type="video", maxResults=1)

        response = request.execute()

        if response["items"]:
            # Get the first video's URL
            video_id = response["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"

        return None

    def download_video_as_mp3(self, youtube_url, output_path):
        yt = YouTube(youtube_url,
			use_oauth=False,
			allow_oauth_cache=True)
        if yt.age_restricted:
            yt.bypass_age_gate()

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()

        try:
            command = [
                'ffmpeg', 
                '-i', out_file,
                '-vn', 
                '-ar', '44100', 
                '-ac', '2', 
                '-b:a', '192k', 
                output_path
            ]
            subprocess.run(command, check=True)
            os.remove(out_file)  # Optionally remove the downloaded file after conversion
            print(f"Audio extracted and saved to {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion: {e}")


    def add_to_queue(self, query):
        logger.debug("adding to queue")
        folder_path = Path(__file__).parent        

        file_path = os.path.join(folder_path, query)
        file_path += ".mp3"

        if os.path.exists(file_path):
            self.queue.append(file_path)
            return file_path 
        else:
            logger.debug("url not in lib searching youtube.....")
            youtube_url = self.search_youtube(query)
            if youtube_url:
                
                mp3_file = self.download_video_as_mp3(youtube_url, file_path)

                self.queue.append(mp3_file)
                logger.debug("File added to queue")
                return mp3_file
            else:
                return "No video found for the query."

    def play_next(self):
        if self.current_index < len(self.queue):
            # Play the mp3 file at self.queue[self.current_index]
            # Implement the actual playback logic here
            self.current_index += 1
        else:
            print("End of queue reached.")

    
    
    async def play_queue(self, voice_client, channel):
        while len(self.queue) > 0 and voice_client.is_connected():
            mp3_path = self.queue.pop(0)
            if len(self.queue) > 0:
                next_song = self.queue[0]
                await channel.send(f"Now playing : {mp3_path}...... on Deck: {next_song}")
            else:
                await channel.send(f"Now playing : {mp3_path}....")
            
            voice_client.play(discord.FFmpegPCMAudio(mp3_path), after=lambda e: self.check_queue(voice_client, channel))

            while voice_client.is_playing():
                await asyncio.sleep(1)  # Wait for the song to finish

            # Optional: Add delay between songs
            await asyncio.sleep(1)

        await channel.send("goodbye!")
        await voice_client.disconnect()


    def skip_song(self, voice_client):
        if voice_client.is_playing():
            voice_client.stop()
            return True
        return False
            


    def check_queue(self, voice_client, channel):
        if len(self.queue) > 0:
            asyncio.run_coroutine_threadsafe(self.play_queue(voice_client, channel), asyncio.get_event_loop())


