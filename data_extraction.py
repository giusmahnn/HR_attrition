import sqlite3
import csv

def extract_data_to_csv(db_file, table_name, csv_file):
    # Connect to the SQLite database
    conn = sqlite3.connect('attr_data.db')
    cursor = conn.cursor()

    # Execute a query to fetch data from the specified table
    cursor.execute(f"SELECT * FROM {'attrition_records'}")

    # Fetch all rows from the result
    rows = cursor.fetchall()

    # Get the column names
    column_names = [description[0] for description in cursor.description]

    # Write the data to a CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the column names as the header
        csv_writer.writerow(column_names)
        # Write the rows of data
        csv_writer.writerows(rows)

    # Close the database connection
    conn.close()

# Example usage:
extract_data_to_csv('example.db', 'my_table', 'Attrition.csv')
