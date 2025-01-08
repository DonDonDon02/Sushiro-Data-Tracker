
# Sushiro Data Tracker

This project is a data tracker for Sushiro Hong Kong stores. It fetches real-time queue information and store details, stores the data in a SQLite database, and then transforms this data into a CSV file for analysis.

---

## Features

- Real-time Data Fetching: Retrieves up-to-date store and queue data
- Combine store information with queue data.
- Store data in an SQLite database.
- Export data to a CSV file for analysis.
- Run scheduled jobs to update data during store operating hours.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DonDonDon02/Sushiro-Data-Tracker.git
   ```  
   ```bash
   cd Sushiro-Data-Tracker
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
---

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```
    The script will start fetching data and store it in an SQLite database (`sushiro_dataset.db`). 
2. **How it works**:
   - The script fetches data from the Sushiro API and combines it into a single dataset.
   - Data is stored in an SQLite database (`sushiro_dataset.db`) and periodically updated during operating hours.
   - It creates a CSV file (`sushiro_dataset.csv`) for convenient data analysis.

3. **Scheduled Updates**:
   - The script uses the `schedule` library to automatically fetch and process data every 10 minutes during store operating hours (09:55–22:02).

---

## Usage of `transform_load.py`

The `transform_load.py` script is used to process and export data from the SQLite database (`sushiro_dataset.db`) created by the `main.py` script. It retrieves data from the `store` table, transforms it into a more analyzable format, and saves it as a CSV file (`sushiro_dataset.csv`).

#### **Steps to Use**:
1. Ensure the database (`sushiro_dataset.db`) exists and is populated by running `main.py`.
2. Run the script:
   ```bash
   python transform_load.py 
   ```
3. The script will:
   - Save the transformed data to a CSV file named `sushiro_dataset.csv` in the current directory. 

This CSV file can then be used for further data analysis or visualization.

## File Structure

- `main.py`: Main script to fetch, process, and store data.
- `transform_load.py`: Script for transforming and exporting the data to a CSV file.
- `requirements.txt`: List of required Python libraries.
- `README.md`: Documentation file.




