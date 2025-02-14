# Kypton Lantz
# February 14, 2025
# Module 8-Assignment 2: Movies: Update & Deletes
# Display selected contents of the film table with a python function that can be called with a cursor and an output

""" Import Statements """
import mysql.connector  # to connect
from mysql.connector import errorcode
from dotenv import load_dotenv  # to use .env file
import os 

# Load environment variables from .env file
load_dotenv()

# Using our .env file
secrets = {
    "USER": os.getenv("USER"),
    "PASSWORD": os.getenv("PASSWORD"),
    "HOST": os.getenv("HOST"),
    "DATABASE": os.getenv("DATABASE")
}

""" Database Config Object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True  # not in .env file
}

def display_films(cursor, title):
    """ Display selected contents of the film table """
    query = """
        SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS Studio
        FROM film f
        INNER JOIN genre g ON f.genre_id = g.genre_id
        INNER JOIN studio s ON f.studio_id = s.studio_id
    """
    
    cursor.execute(query)
    films = cursor.fetchall()

    print(f"\n--- {title} ---")
    for film in films:
        print(f"Name: {film[0]}\nDirector: {film[1]}\nGenre: {film[2]}\nStudio: {film[3]}\n")

try:
    """ Try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # Connect to the movies database

    # Output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()  # Create a cursor object to execute queries

    #Display the films
    display_films(cursor, "DISPLAYING FILMS")

    # Insert a new film record
    insert_query = """
        INSERT INTO film (film_name, film_releaseDate, film_director, genre_id, studio_id, film_runtime)
        VALUES ('The Invisible Man', '2020', 'Leigh Whannell', 
          (SELECT genre_id FROM genre WHERE genre_name = 'Horror'), 
          (SELECT studio_id FROM studio WHERE studio_name = 'Blumhouse Productions'), 124);
    """
    cursor.execute(insert_query)
    db.commit()

    # Display the updated films
    display_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    #Update Alien to being a horror film
    update_query = """
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien';
    """
    cursor.execute(update_query)
    db.commit()

    #Display the films to show the update
    display_films(cursor, "DISPLAYING FILMS AFTER UPDATE (Changed Alien to Horror)")

    #Delete Gladiator from the film table
    delete_query = """
        DELETE FROM film
        WHERE film_name = 'Gladiator';
    """
    cursor.execute(delete_query)
    db.commit()

    #Display the films to show the delete
    display_films(cursor, "DISPLAYING FILMS AFTER DELETE (Removed Gladiator)")

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ Handle MySQL errors """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    """ Close the cursor and connection to MySQL """
    if 'cursor' in locals():
        cursor.close()
    if 'db' in locals() and db.is_connected():
        db.close()
        print("\n  Database connection closed.")
