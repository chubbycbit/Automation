import csv
import mysql.connector
import psycopg2

def execute_query(db_type, connection_details, query):
    try:
        if db_type.lower() == "mysql":
            connection = mysql.connector.connect(**connection_details)
        elif db_type.lower() == "postgresql":
            connection = psycopg2.connect(**connection_details)
        else:
            return None, "Unsupported DB type"

        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result, None
    except Exception as e:
        return None, str(e)

def parse_connection_string(connection_string):
    details = {}
    for part in connection_string.split():
        if '=' in part:
            key, value = part.split('=')
            details[key] = value.strip("'")
    return details

def update_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Test Result', 'Reason']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            runs_on = row['RunsOn']
            db_type = row['DB Type']
            connection_string = row['DB Connection String']
            query = row['Sample Query']
            expected_output = row['Expected Output']

            connection_details = parse_connection_string(connection_string)

            # Update the host for MySQL to 10.0.0.5 if it is in the RunsOn column
            if db_type.lower() == "mysql" and runs_on == "10.0.0.5":
                connection_details['host'] = '10.0.0.5'

            result, error = execute_query(db_type, connection_details, query)
            if error:
                row['Test Result'] = 'Fail'
                row['Reason'] = error
            else:
                result_value = result[0][0] if result else None
                if str(result_value) == str(expected_output):
                    row['Test Result'] = 'Pass'
                    row['Reason'] = ''
                else:
                    row['Test Result'] = 'Fail'
                    row['Reason'] = f"Expected {expected_output}, but got {result_value}"

            writer.writerow(row)

if __name__ == "__main__":
    input_file = 'input.csv'
    output_file = 'output.csv'
    update_csv(input_file, output_file)
