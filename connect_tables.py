from pathlib import Path
import csv

def connect_tablets(folder_path, file_pattern):
    files = folder_path.glob(f'*{file_pattern}.csv')
    combined_data = []
    headers = None
    for file in files:
        name_in_csv = str(file.stem).replace(file_pattern, '')
        with file.open(newline='') as csvfile:
            reader = csv.reader(csvfile)
            current_headers = next(reader)

            if not headers:
                headers = current_headers
                combined_data.append(['Name'] + headers)

            for row in reader:
                combined_data.append([name_in_csv] + row)

    output_file = Path(folder_path, f'connect{file_pattern}.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(combined_data)

if __name__ == "__main__":
    folder_path = Path(r'C:\PROJECTS_Python\TEMP')
    connect_tablets(folder_path, '_result_F')
    connect_tablets(folder_path, '_result_E')
