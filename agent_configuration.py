import csv
import subprocess
import os

def check_tool_installed(tool_name, config_signature, config_signature_type):
    if tool_name == "Notepad++":
        # Check for Notepad++ installation
        try:
            result = subprocess.run(["where", "notepad++"], capture_output=True, text=True, shell=True)
            if result.returncode == 0 and "notepad++" in result.stdout.lower():
                return "Pass"
            else:
                return "Fail"
        except Exception as e:
            return f"Error: {str(e)}"
    elif tool_name == "7-Zip":
        # Check for 7-Zip installation
        if config_signature_type == "FileConfig" and os.path.exists(config_signature):
            return "Pass" if os.path.basename(config_signature) == "7zFM.exe" else "Fail"
        else:
            return "Fail"
    else:
        return "Unknown Tool"

def process_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Test Result', 'Debug Info']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            result = check_tool_installed(row['Tool Name'], row['Config Signature'], row['Config Signature Type'])
            debug_info = f"Checked {row['Tool Name']} with signature {row['Config Signature']}"
            row['Test Result'] = result
            row['Debug Info'] = debug_info
            writer.writerow(row)

input_file = 'input.csv'
output_file = 'output.csv'
process_csv(input_file, output_file)
