import os
import csv
import requests

def check_files_availability(site_id, num_files=2):
    available_files = 0
    for i in range(num_files * 2):  # Check twice as many files to be sure
        if "_" in site_id:
            transect_id = f"{site_id}-{i:04d}"
        else:
            transect_id = f"{site_id}_{i:04d}"
        url = f"http://coastsat.wrl.unsw.edu.au/time-series/{transect_id}/"
        response = requests.head(url)
        if response.status_code == 200:
            available_files += 1
            if available_files >= num_files:
                return True
    return False

def create_csv_files(site_id):
    if check_files_availability(site_id):
        # Get the directory of the current script
        script_dir = os.path.dirname(__file__)
        base_dir = os.path.join(script_dir, "time-series", site_id)
        num_files = 10000  # From -0000 to -9999

        # Create the base directory if it does not exist
        os.makedirs(base_dir, exist_ok=True)

        for i in range(num_files):
            if "_" in site_id:
                transect_id = f"{site_id}-{i:04d}"
            else:
                transect_id = f"{site_id}_{i:04d}"
            file_path = os.path.join(base_dir, f"{transect_id}.csv")
            url = f"http://coastsat.wrl.unsw.edu.au/time-series/{transect_id}/"

            try:
                response = requests.get(url)

                # Check if the request was successful
                if response.status_code == 200:
                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Date", "Distance"])
                        # Parse the CSV data from the response
                        for line in response.text.splitlines():
                            writer.writerow(line.split(','))

                    print(f"Successfully created {file_path}")
                else:
                    print(f"Failed to download {transect_id}, HTTP status code: {response.status_code}")
                    break

            except Exception as e:
                print(f"Error for {transect_id}: {e}")
                break

        print(f"Created up to {i} CSV files in {base_dir}")
    else:
        print(f"Not enough files available for {site_id}. Skipping directory creation.")

# Loop through site IDs from usa_CA_0000 to usa_CA_0099
for i in range(100):
    #site_id = f"usa_CA_{i:04d}"
    site_id = f"mex{i:04d}"
    # site_id = f"chi{i:04d}"
    # site_id = f"per{i:04d}"
    # site_id = f"aus{i:04d}"
    #NOT FOUND ON COASTSAT
    #site_id = f"usa_FL_{i:04d}"
    # site_id = f"usa_DE_{i:04d}"
    # site_id = f"usa_NC_{i:04d}"
    create_csv_files(site_id)
