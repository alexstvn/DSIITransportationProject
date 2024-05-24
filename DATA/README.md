# How to use
## Usage
This folder is mostly used for **data cleaning**, meaning if we're downloading reports or need to update data, we can use this folder as a workspace to do so.
## For Ridership Data
### Obtaining Data
1. Open *TripShot Admin* and navigate to *Reports* and then select *Ridership*.
2. Select desired date range. Deselect the columns related to *Bikes On/Off*. Select the additional columns *Actual Arrival, Actual Departure, Vehicle Capacity, Day of Week*.
3. Download and place the .csv file into the folder `Ridership_Uncleaned`. 
4. To follow file naming consistency, I use the format `DDMMYY-DDMMYY_RidershipData.csv` (e.g. March 2, 2024 - March 10, 2024 would be `030224-041024_RidershipData.csv`). However, this will not affect the code.
### Cleaning Data
1. Place all ridership into `Ridership_Uncleaned`.
2. Right-click the folder `DATA` in file explorer and click *Open in Terminal*.
3. Assuming Python is downloaded, type `python CleanRidershipData.py` into the terminal and hit enter. It should print out the data file names as it processes it.
4. A new file named `RidershipData.csv` should appear in `RIDERSHIP (Fall 2023) > InputData`.