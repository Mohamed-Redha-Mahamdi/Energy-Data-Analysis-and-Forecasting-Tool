# Energy Data Analysis and Forecasting Tool

Welcome to the **Energy Data Analysis and Forecasting Tool** project! This repository is your one-stop destination for automating the retrieval, summarization, and analysis of energy consumption and production data. Our mission is to equip you with actionable insights through descriptive statistics and trend analysis, all within an intuitive suite of scripts and applications.

## Overview

Dive into a comprehensive toolkit that includes modules for data fetching from APIs, storage in a MongoDB database, and analysis and visualization via a Streamlit web application.

## Components

### `download_data.sh`
- **Purpose:** Automates the fetching of historical power breakdown data for France from the Electricity Map API and stores it as a JSON file.
- **Operation:** Utilizes `curl` for API GET requests with an authorization token and saves the output as a timestamped file.
- **Output:** JSON files in `/home/redha/retrieved-data/`.

### `summary_to_mango_db.py`
- **Purpose:** Summarizes the latest JSON file and uploads the data to a MongoDB database.
- **Operation:** Leverages `pandas` for JSON processing, data normalization, and relevant column selection before database insertion.
- **Database Interaction:** Works with "mydatabase" and the "energy" collection in MongoDB.

### `streamlit_script.py`
- **Purpose:** Provides a user-friendly web interface for data visualization and trend analysis.
- **Operation:** Fetches data from MongoDB and employs `streamlit` to create an interactive web application.
- **Visualization Tools:** Uses `matplotlib`, `seaborn`, and `statsmodels` for detailed plotting and forecasting.

### `run_streamlit_app.sh`
- **Purpose:** Launches the Streamlit web application in a browser.
- **Operation:** Sets the `DISPLAY` variable, starts the Streamlit server, and opens the application in Firefox.

### Crontab Entries
- **Purpose:** Schedules script execution for automation.
- **Timing:** 
  - `download_data.sh` at 16:15 daily.
  - `summary_to_mango_db.py` at 16:17 daily.
  - `run_streamlit_app.sh` at 16:20 daily, with logs to `cron.log`.

## Getting Started

To begin:

1. **Clone the Repository:** Secure all scripts in their designated directories on your system.
2. **Set Permissions:** Ensure scripts are executable with `chmod +x`.
3. **Install Dependencies:** Verify installation of `curl`, `pandas`, `pymongo`, `streamlit`, `matplotlib`, `seaborn`, `statsmodels`, and MongoDB.
4. **Execute Scripts:** Run scripts manually or via crontab.
5. **Web Application Access:** Post-execution of `run_streamlit_app.sh`, visit `http://localhost:8501`.

## Customization Instructions

Tailor the toolkit to your environment:

- **Script Paths:** Modify script paths to match your directory structure.
- **Browser Settings:** Change the browser command in `run_streamlit_app.sh` if Firefox isn't your preference.

## Prerequisites

- A Unix-like OS with Bash shell.
- Python 3 with necessary libraries.
- MongoDB

## Important Notes

- Replace the demonstration API token in `download_data.sh` with a valid one.
- Confirm MongoDB configuration for script database access.
- Adjust `run_streamlit_app.sh` sleep duration if needed for Streamlit startup.
- Customize crontab entries to fit your schedule.

## Conclusion

This project simplifies energy data retrieval and analysis, facilitating the discovery of energy trends. With automated scripts and an interactive web application, visualizing and forecasting energy patterns is effortless. Dive into the data and enjoy your forecasting journey!
