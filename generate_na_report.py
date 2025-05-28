import os
import csv
import re
from collections import defaultdict

def count_na_in_files(directory):
    # Dictionary to store station (subfolder) and file NA counts
    station_data = defaultdict(list)
    main_folder = os.path.basename(directory)  # Get main folder name (bag-basin)
    print(f"Scanning directory: {directory}")
    
    # Walk through all folders and subfolders
    for root, dirs, files in os.walk(directory):
        # Get relative path of current folder from main directory
        relative_root = os.path.relpath(root, directory)
        # Get station (Mean Daily Discharge folder)
        station = relative_root if relative_root != '.' else main_folder
        print(f"Processing folder: {root} (Station: {station})")
        
        for file in files:
            # Check only .txt files
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                print(f"Checking file: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Count occurrences of 'NA' (case-sensitive)
                        na_count = len(re.findall(r'\bNA\b', content))
                        if na_count > 0:
                            # Get relative file path for File Folder
                            file_folder = relative_root if relative_root != '.' else ''
                            # Get file name
                            file_name = os.path.basename(file_path)
                            station_data[station].append((file_folder, file_name, na_count))
                            print(f"Found {na_count} 'NA' in {file_name}")
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    
    return main_folder, station_data

def generate_csv_report(main_folder, station_data, output_file):
    # Prepare data for CSV
    report_data = []
    for station, files in station_data.items():
        for file_folder, file_name, na_count in files:
            report_data.append({
                'Main Folder': main_folder,
                'Mean Daily Discharge Folder': station,
                'File Folder': file_folder,
                'File Name (NA Count)': f"{file_name} ({na_count})"
            })
    
    # Sort by NA count in ascending order
    report_data.sort(key=lambda x: int(x['File Name (NA Count)'].split('(')[-1].rstrip(')')))
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Creating it.")
        os.makedirs(output_dir)
    
    # Write to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Main Folder', 'Mean Daily Discharge Folder', 'File Folder', 'File Name (NA Count)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_data:
                writer.writerow(row)
        print(f"Report generated: {output_file}")
    except Exception as e:
        print(f"Error writing CSV to {output_file}: {str(e)}")
    
    return report_data

# Specify the directory to search
directory_path = r"C:\Users\aaa\Desktop\bag-basin"

# Output CSV file in the main directory
output_csv = r"C:\Users\aaa\Desktop\bag-basin\na_report.csv"

# Check if directory exists
if os.path.exists(directory_path):
    print(f"Directory {directory_path} found. Starting scan...")
    main_folder, station_data = count_na_in_files(directory_path)
    if station_data:
        report_data = generate_csv_report(main_folder, station_data, output_csv)
        if not report_data:
            print("No data to write to CSV (empty report).")
    else:
        print("No files containing 'NA' found.")
else:
    print(f"Invalid directory path! Please check if '{directory_path}' exists.")