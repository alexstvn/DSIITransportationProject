import pandas as pd
import os

def main():
    # STEP 0: Create references for directories and file names.
    new_data_folder = (r"Z:\Data\RIDERSHIP\Ridership CSV Files") # data that is being added
    read_data_folder = (r"Z:\Data\RIDERSHIP\Already Added") # where data is moved once added
    data_folder = r"Z:\Data\RIDERSHIP"

    filtered_file_name = "RidershipData.csv"
    unfiltered_file_name = "UnfilteredRidershipData.csv"

    filtered_path = os.path.join(data_folder, filtered_file_name)
    unfiltered_path = os.path.join(data_folder, unfiltered_file_name)

    extension = '.csv'

    # STEP 1: Create an array of csv files to read from.
    
    # STEP 2: Create an array of dataframes from those csv files.
    dfs = []
    for root, dirs, files in os.walk(new_data_folder):
        for file in files:
            if file.endswith(extension):
                # Read CSV file and append to dfs
                file_path = os.path.join(root, file)
                print(file_path)
                df = pd.read_csv(file_path)
                dfs.append(df)
                # Optionally, move the processed file to another folder
                # os.rename(file_path, os.path.join(read_data_folder, file))

    # STEP 3: Append the dataframes to the existing data file containing all the rows.
    # if file exists: 
        # append rows
    df = pd.concat(dfs, ignore_index=True)

    # STEP 4: Cleaning dataframe.
    clean_df(df)

    # STEP 5: Saving unfiltered dataframe.
    df.to_csv(unfiltered_path, index=False)
    # updating code folder
    web_app_file = r"Z:\Code\Web Application\RidershipData.csv"
    df.to_csv(web_app_file, index=False)

    # STEP 6: Filtering out cancelled rides + skipped/awaiting stops
    filter_df(df)

    # STEP 7: Saving filtered dataframe.
    df.to_csv(filtered_path, index=False)

# This cleans the dataframe to allow the data to be more readable by shortening text and relabelling items that refer to the same thing.
def clean_df(df):
    # DROPPING COLUMNS
    columns_to_drop = ['Vehicle Id', 'Vehicle', 'Device Down']
    df.drop(columns=columns_to_drop, inplace=True)
    
    # CLEANING UP ROUTE COLUMN
    df['Route'] = df['Route'].replace('Waltham Shuttle (Mon-Fri)', 'Waltham Shuttle')
    df['Route'] = df['Route'].replace('Boston Cambridge Shuttle (FRI-SAT-SUN)', 'Boston Cambridge Shuttle')
    df['Route'] = df['Route'].replace('Campus Shuttle (Mon-Fri)', 'Campus Shuttle')

    # CLEANING UP STOP COLUMN
    df['Stop'] = df['Stop'].str.replace("\(MBTA Stop\)", "").str.strip()

    # SHORTENING STOP/ROUTE TEXT
    df = df.replace('Usdan Student Center (across from Rabb steps)', 'Rabb Steps')
    df = df.replace('Boston Cambridge Shuttle', 'Boston Shuttle')
    df = df.replace('South Street @ Brandeis Commuter Rail Station', 'Commuter Rail Station')
    df = df.replace('Moody St at Main St (Merc Apartments)', 'Moody St/Main St')
    df = df.replace('Shakespeare Rd and South St (Northbound)', 'Shakespeare Rd @ South St')
    df = df.replace('Mass Ave and Marlborough St', 'Mass/Marlborough')
    df = df.replace('Crescent St @ Cherry St (in front of Watch Factory)', 'Crescent St @ Cherry St')
    df = df.replace('Spingold (front )', 'Spingold')

def filter_df(df):
    df.drop(df[df['Ride State'] == 'Cancelled'].index, inplace = True)
    df.drop(df[df['Stop State'] == 'Skipped'].index, inplace = True)
    df.drop(df[df['Stop State'] == 'Awaiting'].index, inplace = True)

if __name__ == '__main__':
    main()