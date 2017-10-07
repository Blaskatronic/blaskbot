import psycopg2
from tinydb import TinyDB, Query


#def createTables():
#    connection = psycopg2.connect(database='blaskytest', user='blaskbot')
#    cursor = connection.cursor()
#    cursor.execute("CREATE TABLE Clips (ID SMALLINT PRIMARY KEY, URL VARCHAR(70), Author VARCHAR(25));")
#    cursor.execute("CREATE TABLE Viewers (ID SMALLINT PRIMARY KEY, Name VARCHAR(25), Points SMALLINT, Rank VARCHAR(25), Multiplier FLOAT, Lurker BIT, TotalPoints SMALLINT, DrinkExpiry TIME, Drinks SMALLINT);")
#    connection.close()
#
#
#def testTables():
#    connection = psycopg2.connect(database='blaskytest', user='blaskbot')
#    cursor = connection.cursor()
#    cursor.execute("SELECT * FROM Viewers;")
#    cursor.fetchall()
#    cursor.execute("SELECT * FROM Clips;")
#    cursor.fetchall()
#    connection.close()


if __name__ == "__main__":
    viewersDB = TinyDB('./blaskytestViewers.db')
    clipsDB = TinyDB('./blaskytestClips.db')
    discordDB = TinyDB('./discordNames.db')

    viewerDict = viewersDB.search(Query().name.exists())
    clipDict = clipsDB.search(Query().url.exists())
    discordDict = discordDB.search(Query().twitchName.exists())

    connection = psycopg2.connect(database='blaskytest', user='blaskbot')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE Clips (ID SMALLINT PRIMARY KEY, URL VARCHAR(70), Author VARCHAR(25));")
    cursor.execute("CREATE TABLE Viewers (ID SMALLINT PRIMARY KEY, Name VARCHAR(25), Points SMALLINT, Rank VARCHAR(25), Multiplier FLOAT, Lurker BIT, TotalPoints SMALLINT, DrinkExpiry TIME, Drinks SMALLINT);")

    for index, clip in enumerate(clipDict):
        cursor.execute("INSERT INTO Clips (ID, " + ', '.join(clip.keys()) + ") VALUES (%s, %s, %s);", tuple([index] + list(clip.values())))

    for index, viewer in enumerate(viewerDict):
        viewer['lurker'] = 'B' + str(int(eval(viewer['lurker'].capitalize())))
        cursor.execute("INSERT INTO Viewers (ID, " + ', '.join(viewer.keys()) + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", tuple([index] + list(viewer.values())))

    ### Sorting the Discord name mappings out
    # First, create the discord column
    cursor.execute("ALTER TABLE Viewers ADD Discord VARCHAR(25);")
    # Then, update the discord column to be == the name column
    cursor.execute("UPDATE Viewers SET Discord = Name;")

    # Now, iterate through the TinyDB and re-update the ones we know there are discord names for
    for _, user in enumerate(discordDict):
        cursor.execute("UPDATE Viewers SET Discord = %s WHERE Name = %s;", (user['discordName'], user['twitchName']))


    cursor.execute("SELECT * FROM Viewers;")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM Clips;")
    print(cursor.fetchall())

    connection.commit()

    connection.close()
