import discord
import os
import random

import sys

# setting path
sys.path.append("../common")

from db import Database
from sqlite3 import IntegrityError

database = Database()


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

        if message.content == "$link-account":
            await message.reply("I have sent you a dm to link up your account!")

            await message.author.send(
                "To link up your account send the following message to the user 'Beardedhippo' in the osu! ingame chat:"
            )

            verification_code = self.generate_verification_code()
            await message.author.send(f"$verify {verification_code}")

            database.store_verification_code(message.author.id, verification_code)

    def generate_verification_code(self):
        verification_code_lenght = 32
        verification_code = ""

        for _ in range(verification_code_lenght):
            random_integer = random.randint(97, 122)
            verification_code += chr(random_integer)

        return verification_code


client = MyClient()
client.run(os.getenv("DISCORD_BOT_TOKEN"))
