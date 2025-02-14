# Kypton Lantz
# February 12, 2025
# Module 7-Assignment 2: Movies: Table Queries
# Write the code to connect to your MySQL movies database and run four queries.

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

try:
    """ Try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # Connect to the movies database

    # Output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    cursor = db.cursor()  # Create a cursor object to execute queries

    """ QUERY 1: Select all fields from the studio table """
    cursor.execute("SELECT * FROM studio;")
    print("-- DISPLAYING Studio RECORDS --")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0],studio[1]))

    """ QUERY 2: Select all fields from the genre table """
    cursor.execute("SELECT * FROM genre;")
    print("-- DISPLAYING Genre RECORDS --")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0],genre[1]))

    """ QUERY 3: Select movie names for movies with a runtime of less than two hours """
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;")
    print("\n-- DISPLAYING Short Film RECORDS --")
    short_films = cursor.fetchall()
    for film in short_films:
        print("Film Name: {}\nRuntime: {}".format(film[0], film[1]))

    """ QUERY 4: Get a list of film names and directors, grouped by director """
    cursor.execute("SELECT film_director, GROUP_CONCAT(film_name ORDER BY film_name SEPARATOR ', ') AS Movies FROM film GROUP BY film_director;")
    print("\n-- DISPLAYING Director RECORDS in Order --")
    directors = cursor.fetchall()
    for director in directors:
        print("Director: {}\nFilm Name(s): {}\n".format(director[0], director[1]))

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
