# This example requires the 'message_content' privileged intent to function.

import discord

from predict import predict_data

import os

from dotenv import load_dotenv

load_dotenv()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$predict'):
            await message.reply(str(predict_data(str(message.content)[9:])))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))