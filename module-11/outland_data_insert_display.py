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
        ('Safari Adventure', 'Africa', '2024-08-01', '2024-08-10', 5, TRUE, TRUE, TRUE, 'Upcoming'),
        ('Himalayan Expedition', 'Asia', '2024-09-15', '2024-09-30', 8, TRUE, TRUE, FALSE, 'Upcoming'),
        ('Greek Island Trek', 'Southern Europe', '2024-07-20', '2024-07-30', 6, FALSE, FALSE, TRUE, 'Upcoming'),
        ('Sahara Desert Journey', 'Africa', '2024-05-05', '2024-05-15', 3, FALSE, FALSE, TRUE, 'Completed'),
        ('Asian Mountain Adventure', 'Asia', '2024-06-05', '2024-06-15', 4, TRUE, TRUE, FALSE, 'Completed'),
        ('Mediterranean Coastal Trek', 'Southern Europe', '2024-10-01', '2024-10-10', 7, FALSE, TRUE, TRUE, 'Upcoming');
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
        INSERT INTO customers (first_name, last_name, email, phone, gender, birthdate, street_address, city, state, zipcode, created_at)
        VALUES 
        ('John', 'Doe', 'johndoe@example.com', '123-456-7890', 'Male', '1985-06-15', '123 Elm St', 'Denver', 'CO', '80202', NOW()),
        ('Jane', 'Smith', 'janesmith@example.com', '987-654-3210', 'Female', '1990-09-25', '456 Maple Ave', 'Seattle', 'WA', '98101', NOW()),
        ('Alex', 'Johnson', 'alexj@example.com', '555-123-4567', 'Non-binary', '1995-12-05', '789 Oak Ln', 'Austin', 'TX', '73301', NOW()),
        ('Emily', 'Brown', 'ebrown@example.com', '222-333-4444', 'Female', '1988-03-22', '567 Pine St', 'Chicago', 'IL', '60616', NOW()),
        ('Michael', 'Williams', 'mwilliams@example.com', '777-888-9999', 'Male', '1982-11-10', '101 Birch Rd', 'New York', 'NY', '10001', NOW()),
        ('Sarah', 'Lee', 'slee@example.com', '111-222-3333', 'Female', '1993-07-19', '890 Cedar Dr', 'Los Angeles', 'CA', '90012', NOW());
        """
    },
    {
        "table": "bookings",
        "command": """
        INSERT INTO bookings (customer_id, trip_id, status, deposit_paid, total_price, full_payment_due, cancellation_fee, booking_date)
        VALUES 
        (1, 1, 'Confirmed', 500.00, 2500.00, '2024-07-20', NULL, '2024-06-15'),
        (2, 2, 'Confirmed', 600.00, 3000.00, '2024-08-30', NULL, '2024-06-20'),
        (3, 3, 'Confirmed', 400.00, 2000.00, '2024-07-10', NULL, '2024-05-25'),
        (4, 4, 'Canceled', 300.00, 1500.00, '2024-05-30', 150.00, '2024-04-10'),
        (4, 1, 'Pending', 150.00, 600.00, '2024-09-10', NULL, '2024-08-01'),
        (5, 4, 'Pending', 200.00, 800.00, '2024-09-15', NULL, '2024-08-05'),
        (5, 5, 'Confirmed', 350.00, 1750.00, '2024-04-25', NULL, '2024-03-05'),
        (6, 6, 'Confirmed', 450.00, 2250.00, '2024-09-25', NULL, '2024-08-01');
        """
    },
    {
        "table": "customer_reviews",
        "command": """
        INSERT INTO customer_reviews (customer_id, trip_id, rating, review_text, review_date)
        VALUES 
        (1, 1, 5, 'Amazing experience! The guides were fantastic.', '2024-08-12 10:00:00'),
        (2, 2, 4, 'Challenging but rewarding. Would do it again!', '2024-10-01 09:30:00'),
        (3, 3, 3, 'Beautiful scenery but some logistics could be better.', '2024-07-31 14:00:00'),
        (4, 4, 5, 'Loved every minute. Highly recommend.', '2024-06-28 11:15:00'),
        (5, 5, 2, 'Too hot and not enough water stops.', '2024-05-20 08:45:00'),
        (6, 6, 4, 'Spectacular views but bring warm clothes!', '2024-10-20 07:50:00');
        """
    },
    {
        "table": "equipment",
        "command": """
        INSERT INTO equipment (name, type, status, inventory_quantity, price, rental_return_date, acquisition_date, equipment_condition)
        VALUES 
        ('Mountain Tent', 'Tent', 'available', 5, 249.99, '2024-06-01', '2024-01-01', 'New'),
        ('Camping Stove', 'Stove', 'rented', 3, 199.99, '2024-06-10', '2023-11-15', 'Good'),
        ('Backpack', 'Bag', 'sold-out', 0, 129.99, NULL, '2022-08-01', 'Worn'),
        ('Sleeping Bag', 'Bag', 'available', 8, 89.99, NULL, '2023-05-10', 'New'),
        ('Flashlight', 'Accessory', 'rented', 2, 19.99, '2024-06-05', '2022-01-20', 'Needs Repair'),
        ('Hiking Boots', 'Footwear', 'available', 4, 149.99, NULL, '2023-09-01', 'Good'),
        ('Kayak', 'Transportation', 'rented', 3, 1200.99, '2025-03-01','2020-01-01', 'Good');
        """
    },
    {
        "table": "equipment_transactions",
        "command": """
        INSERT INTO equipment_transactions (customer_id, equipment_id, transaction_type, transaction_date, quantity, total_price, payment_method)
        VALUES 
        (1, 2, 'Rental', '2024-07-10 14:30:00', 1, 89.99, 'Credit Card'),
        (5, 5, 'Rental', '2024-07-12 11:00:00', 2, 71.98, 'Cash'),
        (3, 1, 'Rental', '2024-07-15 09:45:00', 1, 249.99, 'Credit Card'),
        (6, 2, 'Rental', '2024-07-18 16:20:00', 3, 269.97, 'Debit Card'),
        (2, 3, 'Purchase', '2024-07-08 10:15:00', 1, 119.99, 'PayPal'),
        (3, 4, 'Purchase', '2024-07-05 16:45:00', 1, 49.99, 'Debit Card'),
        (4, 1, 'Purchase', '2024-06-15 09:30:00', 1, 249.99, 'Credit Card'),
        (6, 6, 'Purchase', '2024-07-18 13:20:00', 3, 59.97, 'Credit Card'),
        (6, 7, 'Rental', '2025-02-18 13:20:00', 1, 1200.99, 'Paypal');
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
        INSERT INTO revenue (booking_id, transaction_id, source, amount, revenue_date)
        VALUES 
        (1, NULL, 'Trip Booking', 2500.00, '2024-06-15 12:00:00'),
        (2, NULL, 'Trip Booking', 3000.00, '2024-06-20 14:30:00'),
        (3, NULL, 'Trip Booking', 2000.00, '2024-05-25 10:45:00'),
        (4, NULL, 'Trip Booking', 1750.00, '2024-03-05 16:20:00'),
        (NULL, 2, 'Equipment Sale', 119.99, '2024-07-08 10:15:00'),
        (NULL, 6, 'Equipment Sale', 19.99, '2024-07-18 13:20:00'),
        (NULL, 3, 'Equipment Rental', 75.00, '2024-07-05'),
        (NULL, 4, 'Equipment Rental', 120.00, '2024-06-25');
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