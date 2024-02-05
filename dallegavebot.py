from openai import OpenAI
import os
import base64
import time
import requests
import discord
from io import BytesIO



class DalleGavebot:
    def __init__(self):
        self.client = OpenAI()

    def get_image_from_variation_dalle(self, image_stream):
        byte_stream = image_stream
        byte_array = byte_stream.getvalue()
        response = self.client.images.create_variation(
                    image=byte_array,
                    n=1,
                    model="dall-e-2",
                    size="1024x1024"
                )
        return response.data[0].url



    def get_image(self, prompt):
        response = self.client.images.generate(
    		model = "dall-e-3",
    		prompt=prompt,
    		size="1024x1024",
    		quality="standard",
    		n=1,
    	)
        image_url = response.data[0].url
        return image_url




    def extract_text_and_image_from_message(self, message: discord.Message):
        """
        Extracts text and the first image from a Discord message.
    
        :param message: A discord.Message object.
        :return: A tuple containing the message text and a BytesIO stream of the first image,
                 or None if no image is found.
        """
        image_stream = None
        for attachment in message.attachments:
            
            url_without_query = attachment.url.split('?')[0]  # This removes the query parameters
            if url_without_query.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                response = requests.get(attachment.url)
                if response.status_code == 200:
                    image_stream = BytesIO(response.content)
                    break  # Only process the first image
                    
        return image_stream