# Energy-Data-Analysis-and-Forecasting-Tool
Energy Data Analysis and Forecasting Tool

Welcome to the Energy Data Analysis and Forecasting Tool project! This suite of scripts and applications is designed to automate the process of retrieving, summarizing, and analyzing energy consumption and production data, with a focus on providing insights through descriptive statistics and trend analysis.


Overview

The project consists of several components that work together to fetch data from an API, store it in a MongoDB database, and then analyze and visualize the data using a Streamlit web application.


Components

download_data.sh

Purpose: Fetches historical power breakdown data for France from the Electricity Map API and saves it as a JSON file.


How it Works: Utilizes curl to make a GET request to the API with an authorization token and outputs the data to a file named with the current date and time.


Output: JSON files are saved to /home/redha/retrieved-data/.


summary_to_mango_db.py

Purpose: Processes the most recent JSON file, summarizes the data, and stores it in a MongoDB database.


How it Works: Uses Pandas to read the JSON file, normalizes the data, selects relevant columns, and inserts the data into a MongoDB collection.


Database Details: The script interacts with a MongoDB database named "mydatabase" and a collection named "energy".


streamlit_script.py

Purpose: Provides a web interface for data visualization and trend analysis.


How it Works: Connects to the MongoDB database, retrieves the data, and uses Streamlit to create an interactive web application. It includes descriptive statistics, bar plots, box plots, and ARIMA forecasting.


Visualization: Uses Matplotlib, Seaborn, and Statsmodels for plotting and forecasting.


run_streamlit_app.sh

Purpose: Launches the Streamlit web application and opens it in a web browser.


How it Works: Sets the DISPLAY environment variable, runs the Streamlit app, and opens the app in Firefox.


Crontab Entries

Purpose: Schedules the execution of the scripts.


Schedule:


download_data.sh runs daily at 16:15.
summary_to_mango_db.py runs daily at 16:17.
run_streamlit_app.sh runs daily at 16:20 and logs output to cron.log.

Getting Started

To use this project, follow these steps:


Clone the Repository: Obtain all the scripts and place them in the appropriate directories on your machine.
Set Permissions: Ensure the scripts are executable (chmod +x).
Install Dependencies: Ensure you have curl, pandas, pymongo, streamlit, matplotlib, seaborn, statsmodels, and MongoDB installed.
Run the Scripts: Execute the scripts either manually or let the crontab handle the scheduling.
Access the Web Application: After run_streamlit_app.sh is executed, the Streamlit app will be available at http://localhost:8501.

Customization Instructions

Script Paths and Browser Configuration:

Before using the project, it's important to customize the paths and browser settings according to your local environment. Here are the steps you should follow:

Script Paths: Update the paths in the scripts to match the directory structure of your machine. This includes changing the directory path in download_data.sh and summary_to_mango_db.py for where the retrieved data is stored, as well as the path to the streamlit_script.py in run_streamlit_app.sh.

Browser Choice: The run_streamlit_app.sh script is configured to open the Streamlit app in Firefox. If you prefer a different browser, or if your default browser is not Firefox, replace the firefox command with the command for your preferred browser. For example, if you want to use Google Chrome, replace firefox with google-chrome.

Prerequisites

A Unix-like operating system with a Bash-compatible shell.
Python 3 with the aforementioned libraries installed.
MongoDB installed and running on the default port (27017).
Firefox web browser for viewing the Streamlit app.

Important Notes

The API token in download_data.sh is for demonstration purposes. Replace it with your own valid token.
Ensure MongoDB is properly set up and that the Python script has the necessary permissions to access and modify the database.
Adjust the sleep duration in run_streamlit_app.sh if the Streamlit app takes longer to start.
The crontab entries are set to run at specific times; adjust these times as needed for your use case.

Conclusion

This project automates the retrieval and analysis of energy data, providing a streamlined process for gaining insights into energy trends. With the help of scheduled scripts and an interactive web application, users can easily visualize and forecast energy consumption and production patterns.
