#Description: This script connects to the Outland Adventures database and populates it with sample data.

import mysql.connector
from mysql.connector import errorcode

# Connection configuration for the outland_user
config = {
    'user': 'outland_user',
    'password': 'outland_adven',
    'host': 'localhost',
    'port': '3306',
    'database': 'outland_adventures',
    'raise_on_warnings': True
}

db = None  # Initialize db to None

# SQL commands to populate the tables in the Outland Adventures database
sql_insert_data_commands = [
    {
        "table": "departments",
        "command": """
        INSERT INTO departments (department_name, description)
        VALUES
        ('Operations', 'Handles all operational tasks'),
        ('Administration', 'Handles administrative tasks'),
        ('Marketing', 'Handles marketing tasks'),
        ('Inventory', 'Handles inventory and equipment'),
        ('Tech', 'Handles e-commerce and technology');
        """
    },
    {
        "table": "roles",
        "command": """
        INSERT INTO roles (role_name, description)
        VALUES
        ('Guide', 'Responsible for leading trips'),
        ('Trip Planner', 'Plans the trips'),
        ('Visa & Airfare Coordinator', 'Handles visa and airfare arrangements'),
        ('Administrator', 'Handles administrative tasks'),
        ('Marketing Manager', 'Manages marketing campaigns'),
        ('Inventory Manager', 'Manages inventory and equipment'),
        ('Equipment Procurement', 'Procures equipment'),
        ('Web Developer', 'Develops and maintains the website');
        """
    },
    {
        "table": "owners",
        "command": """
        INSERT INTO owners (first_name, last_name, email, phone, job_title, department_id, role_id)
        VALUES
        ('Blythe', 'Timmerson', 'blythe.timmerson@example.com', '123-456-7890', 'Co-Owner', 2, 4),
        ('Jim', 'Ford', 'jim.ford@example.com', '234-567-8901', 'Co-Owner', 2, 4);
        """
    },
    {
        "table": "staff",
        "command": """
        INSERT INTO staff (first_name, last_name, email, phone, hire_date, job_title, department_id, salary, employment_status)
        VALUES
        ('John', 'MacNell', 'john.macnell@example.com', '123-456-7890', '2015-01-01', 'Guide', 1, 50000.00, 'Active'),
        ('D.B.', 'Marland', 'db.marland@example.com', '234-567-8901', '2016-02-01', 'Guide', 1, 48000.00, 'Active'),
        ('Anita', 'Gallegos', 'anita.gallegos@example.com', '345-678-9012', '2018-01-01', 'Marketing Manager', 3, 55000.00, 'Active'),
        ('Dimitrios', 'Stravopolous', 'dimitrios.stravopolous@example.com', '456-789-0123', '2017-01-01', 'Inventory Manager', 4, 50000.00, 'Active'),
        ('Mei', 'Wong', 'mei.wong@example.com', '567-890-1234', '2019-01-01', 'Web Developer', 5, 60000.00, 'Active');
        """
    },
    {
        "table": "staff_roles",
        "command": """
        INSERT INTO staff_roles (staff_id, role_id)
        VALUES
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 3),
        (3, 5),
        (4, 6),
        (4, 7),
        (5, 8);
        """
    },
    {
        "table": "trips",
        "command": """
        INSERT INTO trips (trip_name, region, start_date, end_date, min_bookings, visa_required, vaccination_required, airfare_included, status)
        VALUES
        ('African Safari', 'Africa', '2025-03-01', '2025-03-10', 10, TRUE, TRUE, TRUE, 'Upcoming'),
        ('Asian Adventure', 'Asia', '2025-04-01', '2025-04-15', 8, TRUE, TRUE, FALSE, 'Upcoming'),
        ('European Expedition', 'Southern Europe', '2025-02-20', '2025-03-01', 12, FALSE, TRUE, TRUE, 'Ongoing'),
        ('Desert Trek', 'Africa', '2025-02-01', '2025-02-10', 6, TRUE, FALSE, FALSE, 'Completed'),
        ('Mountain Climb', 'Asia', '2025-07-01', '2025-07-15', 5, FALSE, TRUE, TRUE, 'Canceled'),
        ('Beach Getaway', 'Southern Europe', '2025-08-01', '2025-08-10', 15, FALSE, FALSE, TRUE, 'Upcoming');
        """
    },
    {
        "table": "trip_guides",
        "command": """
        INSERT INTO trip_guides (trip_id, staff_id)
        VALUES
        (1, 1),
        (2, 2),
        (3, 1),
        (4, 2),
        (5, 1),
        (6, 2);
        """
    },
    {
        "table": "customers",
        "command": """
        INSERT INTO customers (first_name, last_name, email, phone, address)
        VALUES
        ('John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Main St, Anytown, USA'),
        ('Jane', 'Smith', 'jane.smith@example.com', '234-567-8901', '456 Oak St, Anytown, USA'),
        ('Jim', 'Brown', 'jim.brown@example.com', '345-678-9012', '789 Pine St, Anytown, USA'),
        ('Jake', 'White', 'jake.white@example.com', '456-789-0123', '101 Maple St, Anytown, USA'),
        ('Jill', 'Green', 'jill.green@example.com', '567-890-1234', '202 Birch St, Anytown, USA'),
        ('Jack', 'Black', 'jack.black@example.com', '678-901-2345', '303 Cedar St, Anytown, USA');
        """
    },
    {
        "table": "bookings",
        "command": """
        INSERT INTO bookings (customer_id, trip_id, status, deposit_paid, total_price, full_payment_due, cancellation_fee, booking_date)
        VALUES
        (1, 1, 'Confirmed', 100.00, 1000.00, '2025-02-15', 50.00, '2025-01-01'),
        (2, 2, 'Pending', 200.00, 1500.00, '2025-03-15', 75.00, '2025-02-01'),
        (3, 3, 'Canceled', 150.00, 2000.00, '2025-02-15', 100.00, '2025-01-01'),
        (4, 4, 'Confirmed', 250.00, 1200.00, '2025-01-15', 60.00, '2024-12-01'),
        (5, 5, 'Pending', 300.00, 1800.00, '2025-06-15', 90.00, '2025-05-01'),
        (6, 6, 'Confirmed', 350.00, 2200.00, '2025-07-15', 110.00, '2025-06-01');
        """
    },
    {
        "table": "customer_reviews",
        "command": """
        INSERT INTO customer_reviews (customer_id, trip_id, rating, review_text, review_date)
        VALUES
        (1, 1, 5, 'Amazing trip! Highly recommend.', '2025-03-15'),
        (2, 2, 4, 'Great experience, but could be better.', '2025-04-20'),
        (3, 3, 3, 'Average trip, not too exciting.', '2025-05-25'),
        (4, 4, 5, 'Loved every moment of it!', '2025-06-30'),
        (5, 5, 4, 'Good trip, but had some issues.', '2025-07-10'),
        (6, 6, 5, 'Best trip ever!', '2025-08-15');
        """
    },
    {
        "table": "equipment",
        "command": """
        INSERT INTO equipment (name, type, status, inventory_quantity, price, rental_return_date, purchase_date, equipment_condition, review_flag)
        VALUES
        ('Tent', 'Camping', 'available', 10, 100.00, NULL, '2020-01-01', 'New', FALSE),
        ('Sleeping Bag', 'Camping', 'rented', 5, 50.00, '2025-02-01', '2019-01-01', 'Good', FALSE),
        ('Backpack', 'Hiking', 'sold-out', 0, 75.00, NULL, '2018-01-01', 'Worn', TRUE),
        ('Hiking Boots', 'Hiking', 'available', 20, 120.00, NULL, '2021-01-01', 'New', FALSE),
        ('Water Bottle', 'Camping', 'available', 30, 15.00, NULL, '2022-01-01', 'Good', FALSE),
        ('Compass', 'Navigation', 'available', 15, 25.00, NULL, '2023-01-01', 'New', FALSE);
        """
    },
    {
        "table": "equipment_transactions",
        "command": """
        INSERT INTO equipment_transactions (customer_id, equipment_id, transaction_type, transaction_date, total_price, payment_method)
        VALUES
        (1, 1, 'Purchase', '2025-01-01', 100.00, 'Credit Card'),
        (2, 2, 'Rental', '2025-02-01', 50.00, 'Debit Card'),
        (3, 3, 'Purchase', '2025-03-01', 75.00, 'PayPal'),
        (4, 4, 'Purchase', '2025-04-01', 120.00, 'Credit Card'),
        (5, 5, 'Purchase', '2025-05-01', 15.00, 'Debit Card'),
        (6, 6, 'Purchase', '2025-06-01', 25.00, 'PayPal');
        """
    },
    {
        "table": "marketing_campaigns",
        "command": """
        INSERT INTO marketing_campaigns (campaign_name, strategy, start_date, end_date, budget, effectiveness_score)
        VALUES
        ('Spring Sale', 'Discounts on all equipment', '2025-03-01', '2025-03-31', 5000.00, 4.5),
        ('Summer Adventure', 'Promote summer trips', '2025-06-01', '2025-06-30', 7000.00, 4.8),
        ('Fall Expedition', 'Highlight fall trips', '2025-09-01', '2025-09-30', 6000.00, 4.6),
        ('Winter Wonderland', 'Winter trip promotions', '2025-12-01', '2025-12-31', 8000.00, 4.9),
        ('New Year New Adventures', 'New year trip discounts', '2025-01-01', '2025-01-31', 10000.00, 4.7),
        ('Black Friday Sale', 'Huge discounts on equipment', '2025-11-01', '2025-11-30', 12000.00, 5.0);
        """
    },
    {
        "table": "revenue",
        "command": """
        INSERT INTO revenue (booking_id, transaction_id, trip_region, source, amount)
        VALUES
        (1, NULL, 'Africa', 'Trip Booking', 1000.00),
        (NULL, 1, 'Africa', 'Equipment Sale', 500.00),
        (NULL, 2, 'Africa', 'Equipment Rental', 200.00),
        (2, NULL, 'Asia', 'Trip Booking', 1500.00),
        (NULL, 3, 'Asia', 'Equipment Sale', 750.00),
        (NULL, 4, 'Asia', 'Equipment Rental', 300.00);
        """
    }
]

try:
    # Connect as the new user
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    # Execute the SQL commands to insert data into the tables
    for command in sql_insert_data_commands:
        try:
            cursor.execute(command["command"])
            print(f"Data successfully inserted into table {command['table']}. Rows affected: {cursor.rowcount}")
        except mysql.connector.Error as err:
            print(f"Error inserting data into table {command['table']}: {err}")
    db.commit()
    print("\nInsert Procedure Complete! Data successfully inserted into database {}!".format(config["database"]))

    # Print the structure of each table in the database
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()  # Fetch all the tables
    print("\nTables in database {}:".format(config["database"]))
    for table in tables:
        print("\n{} Table:".format(table[0]))
        cursor.execute("SELECT * FROM {}".format(table[0]))
        rows = cursor.fetchall()
        cursor.execute("DESCRIBE {}".format(table[0]))
        columns = [col[0] for col in cursor.fetchall()]

        # Calculate the maximum width of each column
        col_widths = [max(len(str(value)) for value in col) for col in zip(*([columns] + rows))]

        # Print the column headers
        header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
        print(header)
        print("-" * len(header))

        # Print the rows
        for row in rows:
            print(" | ".join(f"{str(value):<{col_widths[i]}}" for i, value in enumerate(row)))

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
    if db:  # Check if db is not None before closing
        db.close()