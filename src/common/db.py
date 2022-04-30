import sqlite3

import os

current_file_path = os.path.dirname(os.path.realpath(__file__))


class Database:
    def __init__(self):
        self.con = sqlite3.connect(f"{current_file_path}/hippobot.sqlite")

        tablelist = []

        # create tables as needed
        for row in self.con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ):
            tablelist.append(row[0])

        if not "players" in tablelist:
            self.con.execute(
                """create table players (
                discord_id text,
                osu_id text,
                verification_code text
            )"""
            )

    def store_verification_code(self, user_id, verification_code):
        pass
