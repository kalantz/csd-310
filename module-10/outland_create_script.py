# CHANGE THE ROOT CONFIG TO YOUR USERNAME AND PASSWORD BEFORE RUNNING THE SCRIPT
#
#
#Description: This script connects to and creates a new database/user with the necessary permissions to access the Outland Adventures database. It also creates the tables for it.

import mysql.connector
from mysql.connector import errorcode

#Connection configuration for the root user
root_config = {
    'user': 'root', #Change to your username
    'password': '031494Kl.', #Change to your password
    'host': 'localhost',
    'port': '3306',
    'raise_on_warnings': True
}

#Connection configuration for the outland_user
config = {
    'user': 'outland_user',
    'password': 'outland_adven',
    'host': 'localhost',
    'port': '3306',
    'database': 'outland_adventures',
    'raise_on_warnings': True
}

db = None #Initialize db to None

#SQL commands to set up the Outland Adventures database and user
sql_create_db_user_commands= [
    "DROP DATABASE IF EXISTS {database};".format(database=config["database"]),
    "CREATE DATABASE IF NOT EXISTS {database};".format(database=config["database"]),
    "DROP USER IF EXISTS '{user}'@'{host}';".format(user=config["user"], host=config["host"]),
    "CREATE USER IF NOT EXISTS '{user}'@'{host}' IDENTIFIED BY '{password}';".format(user=config["user"], host=config["host"], password=config["password"]),
    "GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'{host}';".format(database=config["database"], user=config["user"], host=config["host"]),
    "FLUSH PRIVILEGES;"
]

#SQL commands to create the tables in the Outland Adventures database
sql_create_tables_commands = [
    """
    CREATE TABLE IF NOT EXISTS departments (
        department_id INT AUTO_INCREMENT PRIMARY KEY,
        department_name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS roles (
        role_id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS owners (
        owner_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        job_title VARCHAR(100) NOT NULL DEFAULT 'Co-Owner',
        department_id INT,
        role_id INT,
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        hire_date DATE NOT NULL,
        job_title VARCHAR(100) NOT NULL,
        department_id INT,
        salary DECIMAL(10,2),
        employment_status ENUM('Active', 'On Leave', 'Terminated') DEFAULT 'Active',
        FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS staff_roles (
        staff_id INT NOT NULL,
        role_id INT NOT NULL,
        PRIMARY KEY (staff_id, role_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS trips (
        trip_id INT AUTO_INCREMENT PRIMARY KEY,
        trip_name VARCHAR(100) NOT NULL,
        region ENUM('Africa', 'Asia', 'Southern Europe') NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        min_bookings INT NOT NULL,
        visa_required BOOLEAN DEFAULT FALSE,
        vaccination_required BOOLEAN DEFAULT FALSE,
        airfare_included BOOLEAN DEFAULT FALSE,
        status ENUM('Upcoming', 'Ongoing', 'Completed', 'Canceled') DEFAULT 'Upcoming'
    );
    """,
        """
        CREATE TABLE IF NOT EXISTS trip_guides (
        trip_id INT NOT NULL,
        staff_id INT NOT NULL,
        PRIMARY KEY (trip_id, staff_id),
        FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE,
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """, 
    """
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        trip_id INT NOT NULL,
        status ENUM('Pending', 'Confirmed', 'Canceled') DEFAULT 'Pending',
        deposit_paid DECIMAL(10,2) DEFAULT 0.00,
        total_price DECIMAL(10,2) NOT NULL,
        full_payment_due DATE NOT NULL,
        cancellation_fee DECIMAL(10, 2),
        booking_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
        FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS customer_reviews (
        review_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        trip_id INT NOT NULL,
        rating INT CHECK (rating BETWEEN 1 AND 5),
        review_text TEXT,
        review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
        FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS equipment (
        equipment_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        type VARCHAR(50) NOT NULL,
        status ENUM('available', 'rented', 'sold-out') NOT NULL,
        inventory_quantity INT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        rental_return_date DATE,
        purchase_date DATE NOT NULL,
        equipment_condition ENUM('New', 'Good', 'Worn', 'Needs Repair') DEFAULT 'New',
        review_flag BOOLEAN DEFAULT FALSE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS equipment_transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        equipment_id INT NOT NULL,
        transaction_type ENUM('Purchase', 'Rental') NOT NULL,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_price DECIMAL(10,2) NOT NULL,
        payment_method VARCHAR(50) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
        FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS marketing_campaigns (
        campaign_id INT AUTO_INCREMENT PRIMARY KEY,
        campaign_name VARCHAR(100) NOT NULL,
        strategy VARCHAR(255) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        budget DECIMAL(10,2) NOT NULL,
        effectiveness_score DECIMAL(5, 2)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS revenue (
        revenue_id INT AUTO_INCREMENT PRIMARY KEY,
        booking_id INT NULL,
        transaction_id INT NULL,
        trip_region ENUM('Africa', 'Asia', 'Southern Europe') NOT NULL,
        source ENUM('Trip Booking', 'Equipment Sale', 'Equipment Rental') NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        revenue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE SET NULL,
        FOREIGN KEY (transaction_id) REFERENCES equipment_transactions(transaction_id) ON DELETE SET NULL
    );
    """
]

try:
    #Connect as root to create the database
    root_db = mysql.connector.connect(**root_config)
    cursor = root_db.cursor()
    print("Database user {} connected to MySQL on host {}".format(root_config["user"], root_config["host"]))

    #Execute the SQL commands to create the database and user
    for command in sql_create_db_user_commands:
        try:
            cursor.execute(command)
            #print(f"\nCommand executed: {command.strip()}")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print("\nDatabase {} already exists: {}".format(config["database"], err))
            elif err.errno == errorcode.ER_CANNOT_USER:
                print("\nUser {} already exists: {}".format(config["user"], err))
            else:
                print(err)
    print("Database user {} and database {} successfully created!".format(config["user"], config["database"]))

    cursor.close()
    root_db.close()
    print("Root connection closed.")

    #Connect as the new user
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("\nDatabase user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    #Execute the SQL commands to create the tables
    for command in sql_create_tables_commands:
        try:
            cursor.execute(command)
            #print(f"Command executed: {command.strip()}")
        except mysql.connector.Error as err:
            print(err)
    print("Tables successfully created in database {}!".format(config["database"]))

    #print the tables in the database
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()  #Fetch all the tables
    print("\nTables in database {}:".format(config["database"]))
    for table in tables:
        print("    {}".format(table[0]))

    cursor.close()
    db.close()
    print("\n{} connection closed.".format(config["database"]))

    input("\n\n Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)

finally:
    if db:  #Check if db is not None before closing
        db.close()