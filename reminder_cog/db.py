import sqlite3 as sql3
from pathlib import Path
import os


# !Category

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


def delete_category(category_id: int):  # TODO: delete connected reminders as well
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


def get_users(category_id: int):
    """ID, UserID, CategoryID"""
    db = sql3.connect("database.db")
    users = db.execute("SELECT ID, UserID, CategoryID FROM CategoryUsers WHERE CategoryID=?", (category_id,)).fetchall()
    db.close()
    return users

# !Reminder

def create_reminder(timestamp: int, user_id: int, category_id: int, message: str):
    db = sql3.connect("database.db")
    db.execute("INSERT INTO Reminders (CategoryID, UserID, TimeStamp, Message) VALUES (?, ?, ?, ?)", (category_id, user_id, timestamp, message))
    db.commit()
    db.close()

def get_reminders(category_id: int) -> list:  # TODO: sort by TimeStamp
    """ID, UserID, TimeStamp, Message, category_id"""
    db = sql3.connect("database.db")
    result = db.execute("SELECT ID, UserID, TimeStamp, Message FROM Reminders WHERE CategoryID=?", (category_id,)).fetchall()
    db.close()
    return [r + (category_id,) for r in result]

def get_reminders_for_reminding(timestamp: int):
    """ID, UserID, TimeStamp, CategoryID, Message"""
    db = sql3.connect("database.db")
    result = db.execute("SELECT ID, UserID, TimeStamp, CategoryID, Message FROM Reminders WHERE TimeStamp<=?", (timestamp,)).fetchall()
    db.close()
    return result

def get_reminder(id: int):
    """ID, UserID, TimeStamp, CategoryID, Message"""
    db = sql3.connect("database.db")
    result = db.execute("SELECT ID, UserID, TimeStamp, CategoryID, Message FROM Reminders WHERE ID=?", (id,)).fetchone()
    db.close()
    return result

def reminder_exist(id: int) -> bool:
    db = sql3.connect("database.db")
    result = db.execute("SELECT * FROM Reminders WHERE ID=?", (id,)).fetchall()
    db.close()
    return len(result) != 0

def delete_reminder(id):
    db = sql3.connect("database.db")
    db.execute("DELETE FROM Reminders WHERE ID=?", (id,))
    db.commit()
    db.close()

def get_guild(reminder_id):
    db = sql3.connect("database.db")
    result = db.execute("SELECT GuildID FROM Categorys WHERE ID=?", (reminder_id,)).fetchone()
    db.close()
    return result[0]

# !Main Stuff

if __name__ == "__main__":
    if Path("database.db").exists():
        os.remove("database.db")

    db = sql3.connect("database.db")
    db.executescript("""
    CREATE TABLE Reminders (
        ID INTEGER NOT NULL UNIQUE,
        UserID INTEGER NOT NULL,
        TimeStamp INTEGER NOT NULL,
        CategoryID INTEGER NOT NULL,
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
