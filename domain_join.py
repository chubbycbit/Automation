import csv

# Define the input and output file paths
input_file_path = r'C:\Users\sreedhe\Desktop\Automation\Aug1st\DomainJoin\input.csv'
output_file_path = r'C:\Users\sreedhe\Desktop\Automation\Aug1st\DomainJoin\output.csv'

# Function to check domain join status
def check_domain_join(runs_on, computer_name):
    # Mock logic for demonstration purposes
    if computer_name in ["Linux-MVM1", "Windows-MVM1"]:
        return "Joined"
    else:
        return "Not Joined"

# Process the input.csv and create output.csv
with open(input_file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['RunsOn', 'ComputerName', 'ExpectedResult', 'TestResult']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in reader:
        runs_on = row['RunsOn']
        computer_name = row['ComputerName']
        expected_result = row['ExpectedResult']
        test_result = check_domain_join(runs_on, computer_name)
        row['TestResult'] = test_result
        writer.writerow(row)

print("Output has been written to output.csv")
