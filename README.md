# BACKGROUND
Although all these files (or a version of these files) can be found in `files.brandeis.edu`, this repository is meant to make the projects I presented on more accessible and easier to navigate since the network drive also contains files that may not be relevant or are related to side-tasks.
As a disclaimer, much work is still needed to be done to deploy to make it easier to access as well as for documentation purposes.

# REPOSITORY STRUCTURE
This is an overview of the structure of the repository. More specific tutorials or explanations can also be found in the README of the subfolders: **DATA**, **RIDERSHIP**, and **COMPLAINT ANALYSIS**.
Some notes about how files are used:
 - **Jupyter Notebooks** (`.ipnyb` files): I tend to use Jupyter Notebooks when first drafting a dashboard. I like to think of them as sketches before drafting a final art piece since I can debug and experiment with different elements as needed.

## DATA
 - **Complaints_Uncleaned** and **Ridership_Uncleaned**: These should complain the raw data of the corresponding projects. `Ridership_Uncleaned` can hold multiple files since the script is designed to handle multiple files.
 - **CleanRidershipData.py**: When running this script, it will condense all data files into one. However, this specifically applies to the Ridership data since it was used to condense all multiple report files into one.

## RIDERSHIP (Fall 2023)
This contains relevant work, finalized data, and notebooks of the project that pertains to analyzing trends in ridership.
- Jupyter Notebooks contain the work for the dashboard leading up to the final web app product.
- `WEB APP` contains the files necessary to run the web app application. This folder is necessary to open in terminal with so that you can run the script locally.
	 - **This is the most important part of this project since it is the closest to "deployment".**

## COMPLAINT ANALYSIS (Spring 2024)
This project is the complaint analysis dashboard. As of right now the visualizations have mostly been produced in Jupyter notebook to allow for experimentation.

## VIDEO TUTORIALS
This should contains relevant videos for how to use the dashboard and will be added as needed.