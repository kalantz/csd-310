#Description: This script connects to the Outland Adventures database and runs reports on customer buy vs. rent habits, booking trends, demographics, and equipment age/wear.

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

#Function to run and display a report with formatted output
def run_report(query, description):
    try:
      # Connect as the new user
      db = mysql.connector.connect(**config)
      cursor = db.cursor()
      print("\n Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

      print(f"\n--- {description} ---")

      cursor.execute(query)
      results = cursor.fetchall()
      columns = [col[0] for col in cursor.description] #get column names

      if results:
         #Determine column widths dynamically
         col_widths = [max(len(str(value)) for value in col) for col in zip(*([columns] + results))]

         #Print the column headers
         header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
         print(header)
         print("-" * len(header))

         #Print each row of results
         for row in results:
            print(" | ".join(f"{str(value):<{col_widths[i]}}" for i, value in enumerate(row)))
      else:
         print("No results found.")
    
    except mysql.connector.Error as err:
       print(f"Error: {err}")

    finally:
       cursor.close()
       db.close()
       print("\nReport execution completed.")

#Sales report for equipment (Buy vs. Rent)
sales_report_query = """
WITH transaction_types AS (
    SELECT 'Purchase' AS transaction_type
    UNION ALL
    SELECT 'Rental'
)
SELECT 
    e.type AS product_type, 
    tt.transaction_type, 
    COALESCE(SUM(et.total_price), 0) AS total_sales
FROM equipment e
CROSS JOIN transaction_types tt
LEFT JOIN equipment_transactions et 
    ON e.equipment_id = et.equipment_id 
    AND et.transaction_type = tt.transaction_type
    AND et.transaction_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY e.type, tt.transaction_type
ORDER BY e.type, tt.transaction_type;
"""

#Booking trends by location (Africa, Asia, Southern Europe)
booking_trends_query = """
SELECT 
    t.region,
    COUNT(b.booking_id) AS total_bookings,
    MAX(b.booking_date) AS most_recent_booking_date
FROM bookings b
JOIN trips t ON b.trip_id = t.trip_id
WHERE b.status IN ('Confirmed', 'Pending')
  AND b.booking_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY t.region
ORDER BY total_bookings DESC;
"""
#Customer demographics report
customer_demographics_query = """
WITH Demographics AS (
    -- Gender-based aggregation
    SELECT 
        c.gender AS demographic,
        COUNT(DISTINCT c.customer_id) AS total_customers,
        COUNT(DISTINCT b.booking_id) AS total_bookings,
        COUNT(DISTINCT et.transaction_id) AS total_transactions,
        1 AS sort_order
    FROM customers c
    LEFT JOIN bookings b ON c.customer_id = b.customer_id
    LEFT JOIN equipment_transactions et ON c.customer_id = et.customer_id
    GROUP BY c.gender

    UNION ALL

    -- Age range-based aggregation
    SELECT 
        CASE
            WHEN TIMESTAMPDIFF(YEAR, c.birthdate, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
            WHEN TIMESTAMPDIFF(YEAR, c.birthdate, CURDATE()) BETWEEN 25 AND 34 THEN '25-34'
            WHEN TIMESTAMPDIFF(YEAR, c.birthdate, CURDATE()) BETWEEN 35 AND 44 THEN '35-44'
            WHEN TIMESTAMPDIFF(YEAR, c.birthdate, CURDATE()) BETWEEN 45 AND 54 THEN '45-54'
            WHEN TIMESTAMPDIFF(YEAR, c.birthdate, CURDATE()) BETWEEN 55 AND 64 THEN '55-64'
            ELSE '65+'
        END AS demographic,
        COUNT(DISTINCT c.customer_id) AS total_customers,
        COUNT(DISTINCT b.booking_id) AS total_bookings,
        COUNT(DISTINCT et.transaction_id) AS total_transactions,
        2 AS sort_order
    FROM customers c
    LEFT JOIN bookings b ON c.customer_id = b.customer_id
    LEFT JOIN equipment_transactions et ON c.customer_id = et.customer_id
    GROUP BY demographic

    UNION ALL

    -- State-based aggregation
    SELECT 
        c.state AS demographic,
        COUNT(DISTINCT c.customer_id) AS total_customers,
        COUNT(DISTINCT b.booking_id) AS total_bookings,
        COUNT(DISTINCT et.transaction_id) AS total_transactions,
        3 AS sort_order
    FROM customers c
    LEFT JOIN bookings b ON c.customer_id = b.customer_id
    LEFT JOIN equipment_transactions et ON c.customer_id = et.customer_id
    GROUP BY c.state
)

SELECT demographic, total_customers, total_bookings, total_transactions
FROM Demographics
ORDER BY sort_order ASC, 
         FIELD(demographic, 'Male', 'Female', 'Non-binary', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'), 
         demographic;
"""

#Inventory age/wear report
inventory_age_query = """
SELECT
  e.equipment_id,
  e.name,
  e.type,
  e.acquisition_date,
  e.equipment_condition,
  DATEDIFF(CURDATE(), e.acquisition_date) / 365 AS age_in_years
FROM equipment e
WHERE e.acquisition_date <= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)
  OR e.equipment_condition IN ('Worn', 'Needs Repair')
  OR e.review_flag = 1
ORDER BY age_in_years DESC;
"""

#Running all reports
if __name__ == "__main__":
    run_report(sales_report_query, "Sales Report for Equipment (Buy vs. Rent)")
    run_report(booking_trends_query, "Booking Trends by Location (Africa, Asia, Southern Europe)")
    run_report(customer_demographics_query, "Customer Demographics Report")
    run_report(inventory_age_query, "Inventory Age Report")
