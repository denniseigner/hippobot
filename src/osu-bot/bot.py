import os
import random
import sys

# setting path
sys.path.append("../common")

from db import Database

from irc.bot import SingleServerIRCBot
from irc.client import ip_numstr_to_quad

database = Database()


class HippobotOsu(SingleServerIRCBot):
    def __init__(self, server, port, nickname, password, channel):
        SingleServerIRCBot.__init__(
            self, [(server, port, password)], nickname, nickname
        )
        self.channel = channel

    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_privmsg(self, connection, event):
        self.do_command(connection, event)

    def on_pubmsg(self, connection, event):
        print(event)

    def on_dccmsg(self, connection, event):
        text = event.arguments[0].decode("utf-8")
        connection.privmsg("You said: " + text)

    def on_dccchat(self, connection, event):
        if len(event.arguments) != 2:
            return
        args = event.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, connection, event):
        print(event)
        print(connection)
        command = event.arguments[0]
        username = event.source.split("!")[0]

        if command.startswith("$roll"):
            max_number = command.split()[1]
            random_number = random.randint(1, int(max_number))
            connection.privmsg(
                event.source.split("!")[0], f"You rolled {random_number}"
            )
            print(event.source.split("!")[0])
            print(f"You rolled {random_number}")

        if command.startswith("$verify"):
            verification_code = command.split()[1]
            verifcation_result = database.verify(verification_code, username)
            connection.privmsg(username, verifcation_result)


if __name__ == "__main__":
    server = "irc.ppy.sh"
    port = 6667
    channel = "#osu"
    nickname = f'{os.getenv("IRC_USERNAME")}'
    password = f'{os.getenv("IRC_PASSWORD")}'

    bot = HippobotOsu(server, port, nickname, password, channel)
    bot.start()
