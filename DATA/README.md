# How to use
## Usage
This folder is mostly used for **data cleaning**, meaning if we're downloading reports or need to update data, we can use this folder as a workspace to do so.
## For Ridership Data
### Obtaining Data (in batches)
1. Open *TripShot Admin* and navigate to *Reports* and then select *Ridership*.
2. Select desired date range. Deselect the columns related to *Bikes On/Off* and *Bikes Cumulative*. Select the additional columns *Actual Arrival, Actual Departure, Vehicle Capacity, Day of Week*. It should look something like this (*Day of Week selected is out of view*).\
![Columns that should be selected.](../VIDEO%20TUTORIALS/_img/DATA_Ridership_TripShot_1.png)
3. Download and place the .csv file into the folder `Ridership_Uncleaned`. 
4. To follow file naming consistency, I use the format `DDMMYY-DDMMYY_RidershipData.csv` (e.g. March 2, 2024 - March 10, 2024 would be `030224-041024_RidershipData.csv`). However, this will not affect the code.
    - The script is configured to allow for subfolders. So for example, we can have subfolders within `Ridership_Uncleaned` that contains data separated by semester:\
    ![Example photo of directory.](../VIDEO%20TUTORIALS/_img/DATA_Ridership_TripShot_2.png)
    - Then, within a folder (e.g. `Spring 2024`), we can have a larger list of data:\
    ![Example photo of directory.](../VIDEO%20TUTORIALS/_img/DATA_Ridership_TripShot_3.png)
    - Again, you can name it anything that works for you! It will not affect the code.

### Cleaning Data
1. Make sure all **uncleaned** ridership data into `Ridership_Uncleaned`.
2. Now, go into the `DATA` folder and double click `CleanRidershipData.py`.
3. A new file named `RidershipData.csv` should appear in `RIDERSHIP (Fall 2023)/InputData`.

### Inserting already clean data.
1. Drag and drop the already clean data file into `RIDERSHIP (Fall 2023)/InputData`, but if you're unsure, you can follow the steps in **Obtaining Data** and **Cleaning Data**. It should *not* have any impact on the file.