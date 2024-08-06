import csv
import paramiko
import socket

def check_linux_service_status(host, service):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='sreedhe', password='Def@ult@280925')

        stdin, stdout, stderr = ssh.exec_command(f'systemctl is-active {service}')
        status = stdout.read().decode().strip()
        ssh.close()
        return status == 'active'
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
        return False

def is_resolvable(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

def process_services(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        # Read the first line to fix the headers
        first_line = infile.readline().strip()
        corrected_headers = first_line.split(',')
        
        print(f"Corrected Headers: {corrected_headers}")  # Debug output
        
        reader = csv.DictReader(infile, fieldnames=corrected_headers)
        writer = csv.DictWriter(outfile, fieldnames=corrected_headers)
        writer.writeheader()
        
        for row in reader:
            print(f"Processing row: {row}")  # Debug output
            runs_on = row['RunsOn'].strip()
            computer_name = row['ComputerName'].strip()
            service_name = row['ServiceName'].strip()
            expected_status = row['ExpectedStatus'].strip() if row['ExpectedStatus'] else 'inactive'
            
            if is_resolvable(computer_name):
                if 'linux' in runs_on.lower():
                    is_active = check_linux_service_status(computer_name, service_name)
                else:
                    is_active = False  # Assuming only Linux services need to be checked in this example

                row['TestResult'] = 'Pass' if is_active and expected_status == 'active' else 'Fail'
            else:
                print(f"Hostname {computer_name} is not resolvable.")
                row['TestResult'] = 'Fail'
            
            writer.writerow(row)

input_csv = r'C:\Users\sreedhe\Desktop\Automation\Aug1st\ServiceHealth\input.csv'  # Ensure the correct path to your input CSV file
output_csv = r'C:\Users\sreedhe\Desktop\Automation\Aug1st\ServiceHealth\output.csv'  # Output CSV file path

process_services(input_csv, output_csv)
