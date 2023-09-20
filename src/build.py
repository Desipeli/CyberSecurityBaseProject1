from sqlalchemy import text
import sqlite3
from werkzeug.security import generate_password_hash


def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE {table[0]}")
    conn.commit()

    # Users
    cursor.execute(
        "CREATE TABLE Users(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    cursor.execute(
        "INSERT INTO Users(username, password) VALUES ('alice', :password)",
        {"password": generate_password_hash("password12345", method="md5")}
    )
    cursor.execute(
        "INSERT INTO Users(username, password) VALUES ('bob', :password)",
        {"password": generate_password_hash("password12345", method="md5")}
    )

    # Mooovies
    cursor.execute(
        "CREATE TABLE Moovies(id INTEGER PRIMARY KEY, title TEXT, description TEXT, image TEXT)"
    )
    cursor.execute(
        """INSERT INTO Moovies(title, description, image) VALUES(
            ' Dairy of the Rings: The Hoofed Heroes',
            'Moofrodo Bovins, a humble Holstein, finds himself chosen to bear the responsibility of the One Ring, a powerful artifact coveted by the nefarious dairy farmer, Cowron. Assisted by a loyal band of bovine companions, Moofrodo embarks on an epic journey to save their pastures.

Guided by the wise and mystical Gandairy the Moozard, Moofrodo is joined by ArCOWmie, the steadfast warrior, Merry-Moos and Pippenchew, the mischievous bovine duo, and Legolamb, the skilled archer with hooves of precision. Their quest leads them through the idyllic pastures of Middle-Moo, where they encounter the enigmatic Tom Bullbadil, a carefree singing bull among other charming characters.

As the Hoofed Heroes inch closer to the volcanic Mount Mordairy, they must overcome the eerie Udderwraiths, spectral cattle rustlers, and navigate treacherous terrain like the dreaded Marsh of Moozark. The climax of their journey involves the perilous task of destroying the One Ring by tossing it into the fiery udder of Mount Doomoo.',
            'de2_lotr.png')
        """
    )
    cursor.execute(
        """INSERT INTO Moovies(title, description, image) VALUES(
        'Dairy Potter and the Moo-losopher''s Stone',
        'In the whimsical world of Dairy Potter, a young calf named Dairy Potter lives an ordinary life with his neglectful aunt and uncle, the Bovineleys, and their calf, Dudley. On his eleventh birthday, Dairy receives an invitation to attend Cowwarts School of Witchcraft and Herdery, where he discovers his magical abilities and learns about his famous parents, Lily and James Moo-ter.

Upon arrival at Cowwarts, Dairy befriends Ron Weasbull and Hermione Granger and embarks on a journey filled with spell-casting, potion-making, and mystical adventures. The trio becomes suspicious when they suspect someone is trying to steal the Moo-losopher''s Stone, a powerful relic said to grant immortality.

With courage and teamwork, Dairy and his friends uncover a plot involving their Defense Against the Dark Herds teacher, Professor Quirrell, and his connection to the dark cow-wizard, Lord Volde-moo. Together, they must protect the Moo-losopher''s Stone from falling into the wrong hooves.

\"Dairy Potter and the Moo-losopher''s Stone\" is a heartwarming tale of friendship, bravery, and the magic of the bovine world, as Dairy begins his extraordinary journey in the enchanting realm of Dairy Potter.',
        'de2_potter.png')
        """
    )
    cursor.execute(
        """INSERT INTO Moovies(title, description, image) VALUES(
        'Star Herds: Episode IV - A New Bull',
        'In a galaxy far, far away, the moo-rebellion against the evil Galactic Herdmaster and his Imperial Cattle Empire rages on. The Rebel Herds, fighting for freedom and justice, have obtained the plans to the Empire''s ultimate weapon, the Bovine Star, a space station with the power to destroy entire planets.

The story follows the journey of a young farmhand named Luke Sky-grazer, who, like many, dreams of a life beyond the confines of his moisture farm on the desert planet Tatoo-ween. Luke''s life takes an unexpected turn when he discovers a message hidden within a pair of droids, R2-MOO2 and C-3PO, that contain vital information about the Bovine Star.

Teaming up with the wise and mysterious Obi-Wan Ken-bull, a hermit with a hidden past, and the roguish cattle smuggler Han Cow-lo, Luke sets out on a daring adventure to rescue Princess Leia Organa, a prominent member of the Rebel Herds who''s been captured by the Empire.

Their journey leads them to the heart of the Empire, where they encounter iconic characters like the dreaded Darth Moo-der and the imposing Grand Moolk Tarkin. The Rebel Herds, including Princess Leia and the wookiee co-pilot, Chewbacca, join forces to devise a plan to destroy the Bovine Star.

In an epic space battle, the Rebel Herds launch a desperate assault on the Bovine Star, with Luke using his newfound skills in the ways of the Bull-der to target the station''s vulnerable exhaust port. With precise aim, he delivers a decisive blow, causing the Bovine Star to implode, and the Rebel Herds emerge victorious.

\"Star Herds: Episode IV - A New Bull\" is a timeless tale of heroism, hope, and the fight against tyranny in a galaxy where the Force binds all beings, whether they walk on two legs or four. It marks the beginning of Luke Skywalker''s journey and the Rebel Herds'' struggle to restore freedom to the galaxy.',
        'de2_sw.png')"""
    )

    # Comments
    cursor.execute(
        "CREATE TABLE Comments(id INTEGER PRIMARY KEY, comment TEXT, user INTEGER, moovie, FOREIGN KEY(user) REFERENCES Users(id), FOREIGN KEY(moovie) REFERENCES Moovies(id))"
    )
    cursor.execute(
        "INSERT INTO Comments(comment, user, moovie) VALUES('""Moo-tastic! ''Moofrodo and the Quest for the One Ring'' is an utterly captivating bovine adventure that left me chewing my cud in awe. From the wise Gandairy the Moozard to the mischievous Pippenchew, this movie''s cast is udderly charming. The journey through Middle-Moo is a hoof-stomping thrill, and the climax at Mount Doomoo had me on the edge of my pasture. A must-see for all my fellow cud-chewing movie enthusiasts!"" #MooovieMagic', 1, 1)"
    )

    conn.commit()
