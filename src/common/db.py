import sqlite3

import os

current_file_path = os.path.dirname(os.path.realpath(__file__))


class Database:
    def __init__(self):
        self.con = sqlite3.connect(f"{current_file_path}/hippobot.sqlite")

        # create tables as needed
        self.con.execute(
            """create table if not exists players (
            discord_id text primary key,
            osu_id text unique,
            verification_code text
        )"""
        )
        self.con.commit()

    def store_verification_code(self, user_id, verification_code):
        self.con.execute(
            "insert into players(discord_id, verification_code) values (?, ?)",
            (user_id, verification_code),
        )
        self.con.commit()

    def verify(self, verification_code, osu_username):
        discord_id = ""
        for row in self.con.execute(
            "select discord_id from players where verification_code = (?)",
            (verification_code,),
        ):
            discord_id = row[0]

        if discord_id == "":
            return "Verification not successful"

        self.con.execute(
            "update players set osu_id = (?) where verification_code = (?)",
            (osu_username, verification_code),
        )
        self.con.commit()
        return "Verification succesful"
