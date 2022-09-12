import sqlite3 as sql3
from pathlib import Path
import os


def create_category(user_id: int, guild_id: int, name: str):
    db = sql3.connect("database.db")
    db.execute("INSERT INTO Categorys (UserID, GuildID, Name) VALUES (?, ?, ?)", (user_id, guild_id, name))
    db.commit()
    db.close()


def category_exists(category_id: int) -> bool:
    db = sql3.connect("database.db")
    result = db.execute("SELECT * FROM Categorys WHERE ID=?", (category_id,)).fetchall()
    db.close()
    return len(result) != 0


def delete_category(category_id: int):
    db = sql3.connect("database.db")
    db.execute("DELETE FROM Categorys WHERE ID=?", (category_id,))
    db.commit()
    db.close()


def get_categorys(guild_id: int) -> list:
    db = sql3.connect("database.db")
    result = db.execute("SELECT ID, UserID, GuildID, Name FROM Categorys WHERE GuildID=?", (guild_id,)).fetchall()
    db.close()
    return result


def get_owned_category(user_id: int):
    db = sql3.connect("database.db")
    result = db.execute("SELECT CategoryID FROM CategoryUsers WHERE UserID=?", (user_id,)).fetchall()
    db.close()
    return [x[0] for x in result]


def set_user_categorys(categorys: list, user_id: int):
    db = sql3.connect("database.db")
    db.execute("DELETE FROM CategoryUsers WHERE UserID=?", (user_id,))
    for category_id in categorys:
        db.execute("INSERT INTO CategoryUsers (UserID, CategoryID) VALUES (?, ?)", (user_id, category_id))
    db.commit()
    db.close()


if __name__ == "__main__":
    if Path("database.db").exists():
        os.remove("database.db")

    db = sql3.connect("database.db")
    db.executescript("""
    CREATE TABLE Reminders (
        ID INTEGER NOT NULL UNIQUE,
        UserID INTEGER NOT NULL,
        GuildID INTEGER NOT NULL,
        TimeStamp INTEGER NOT NULL,
        Message TEXT NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
    )
    """)

    db.executescript("""
    CREATE TABLE Categorys (
        ID INTEGER NOT NULL UNIQUE,
        UserID INTEGER NOT NULL,
        GuildID INTEGER NOT NULL,
        Name TEXT NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
    )
    """)

    db.executescript("""
    CREATE TABLE CategoryUsers (
        ID INTEGER NOT NULL UNIQUE,
        UserID INTEGER NOT NULL,
        CategoryID INTEGER NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
    )
    """)
