import csv
import paramiko

def check_connectivity_via_ssh(source, destination, port, username, key_file, key_type='pem', timeout=10):
    try:
        print(f"Connecting to {source} as {username} using {key_type} key...")

        # SSH connection details for the source machine
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load the appropriate private key file
        if key_type == 'pem':
            pkey = paramiko.RSAKey.from_private_key_file(key_file)
        elif key_type == 'ppk':
            pkey = paramiko.RSAKey.from_private_key_file(key_file, password=None)
        else:
            raise ValueError(f"Unsupported key type: {key_type}")

        # Connect using the private key
        ssh.connect(source, username=username, pkey=pkey)
        print(f"Connected to {source}")

        # Run the connectivity test command on the source machine
        command = f"nc -zv {destination} {port}"  # Using netcat to test port connectivity
        print(f"Executing command: {command}")
        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        print(f"Command executed. Output: {output}, Error: {error}")

        if 'succeeded' in output or 'succeeded' in error:
            return "Pass"
        elif error:
            return f"Fail: {error}"
        else:
            return "Fail: No specific error"
    except Exception as e:
        return f"Error: {e}"

def update_csv(file_path, results):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["RunsOn", "Source", "Destination", "Port", "ExpectedResult", "TestResult"])
        writer.writerows(results)

def main():
    input_file = 'input.csv'
    output_file = 'output.csv'
    key_file = r'C:\Users\sreedhe\Desktop\Automation\JUly31st\connectivity\Linux-MVM1.pem'  # Update this path
    key_type = 'pem'  # Change to 'ppk' if you are using a .ppk file
    username = 'sreedhe'  # Replace with your actual username
    results = []

    with open(input_file, mode='r') as file:
        # Skip the first line that says "Connectivity"
        next(file)
        csv_reader = csv.DictReader(file)
        
        # Print the header row to diagnose the issue
        headers = csv_reader.fieldnames
        print(f"CSV Headers: {headers}")
        
        for row in csv_reader:
            print(f"Row data: {row}")  # Print the row data for debugging
            runs_on = row["RunsOn"]
            source = row["Source"]
            destination = row["Destination"]
            port = row["Port"]
            expected_result = row["ExpectedResult"]
            print(f"Testing connectivity from {source} to {destination} on port {port}")
            test_result = check_connectivity_via_ssh(source, destination, port, username, key_file, key_type)
            if test_result.startswith("Error:"):
                test_result = f"Fail: {test_result}"
            results.append([runs_on, source, destination, port, expected_result, test_result])

    update_csv(output_file, results)
    print(f"Test results written to {output_file}")

if __name__ == "__main__":
    main()
