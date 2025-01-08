import requests
import json
import sqlite3
import pytz
from datetime import datetime
import schedule
import time

# Database name
db_name = 'sushiro_dataset.db'

def get_json():
    """Fetch store list JSON data."""
    url = 'https://sushipass.sushiro.com.hk/api/2.0/info/storelist?latitude=22&longitude=114&numresults=33&region=HK'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def get_json_groupqueues(id):
    """Fetch queue data for a specific store by ID."""
    url = f'https://sushipass.sushiro.com.hk/api/2.0/remote/groupqueues?region=HK&storeid={id}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def get_sushi_data()->list: 
    """
    Fetch and combine store data with queue data.
    Returns a list of combined dicts.
    """
    sushi_list = get_json()
    hk_timezone = pytz.timezone('Asia/Hong_Kong')
    current_time_hk = datetime.now(hk_timezone)

    # Collect all data in one loop
    combined_data = []
    for store in sushi_list:
        store_id = store['id']
        store['timestamp'] = current_time_hk  # Add timestamp
        try:
            queue_data = get_json_groupqueues(store_id)
            combined_data.append({**store, **queue_data})  # Merge dictionaries
        except requests.RequestException as e:
            print(f"Failed to fetch queue data for store ID {store_id}: {e}")
            continue

    return combined_data

def create_database():
    """Create the SQLite database and store table if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER,
        storeStatus TEXT,
        name TEXT,
        waitingGroup INTEGER,
        timestamp DATETIME,
        boothQueue TEXT,
        counterQueue TEXT,
        mixedQueue TEXT,
        reservationQueue TEXT,
        reservationCounterQueue TEXT,
        reservationBoothQueue TEXT,
        storeQueue TEXT,
        storeCounterQueue TEXT,
        storeBoothQueue TEXT,
        separateQueue INTEGER,
        nameKana TEXT,
        nameEn TEXT,
        address TEXT,
        area TEXT,
        latitude REAL,
        longitude REAL,
        distance TEXT,
        sortOrder INTEGER,
        wait INTEGER,
        waitTimeCounter INTEGER,
        waitTimeCap INTEGER,
        netTicketStatus TEXT,
        remoteTicketingManualStatus TEXT,
        reservationStatus TEXT,
        checkinStatus TEXT,
        requireNetTicketLogin BOOLEAN,
        forceLocalMode BOOLEAN,
        prefecturesJisCode TEXT,
        municipalities TEXT,
        municipalitiesJisCode TEXT,
        spot TEXT,
        tel TEXT,
        parkingInfo INTEGER,
        reservationPagelink TEXT,
        counterReservationsAllowed BOOLEAN,
        openDate TEXT,
        commencementDate TEXT,
        cancellationMobileMinutes INTEGER,
        cancellationReservationMinutes INTEGER,
        tablesCapacity INTEGER,
        countersCapacity INTEGER,
        maxCustomersMobileTable INTEGER,
        minCustomersMobileTable INTEGER,
        maxCustomersMobileCounter INTEGER,
        minCustomersMobileCounter INTEGER,
        maxCustomersMobileCounter2 INTEGER,
        minCustomersMobileCounter2 INTEGER,
        maxCustomersMobileCounter3 INTEGER,
        minCustomersMobileCounter3 INTEGER,
        maxCustomersReservationTable INTEGER,
        minCustomersReservationTable INTEGER,
        maxCustomersReservationCounter INTEGER,
        minCustomersReservationCounter INTEGER,
        maxCustomersReservationCounter2 INTEGER,
        minCustomersReservationCounter2 INTEGER,
        maxCustomersReservationCounter3 INTEGER,
        minCustomersReservationCounter3 INTEGER,
        isAgs BOOLEAN,
        waitingGroupTable INTEGER,
        waitingGroupCounter INTEGER,
        waitingGroupPair INTEGER,
        localTicketingStatus TEXT,
        clientVersion TEXT,
        seatConfig INTEGER,
        pairReservationsAllowed BOOLEAN,
        showCheckinCode BOOLEAN,
        showCheckinCodeDialog BOOLEAN,
        waitShowType INTEGER,
        region TEXT
    );
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def insert_data(data):
    """Insert data into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    insert_sql = '''
    INSERT INTO store (
        id, storeStatus, name, waitingGroup, timestamp, boothQueue, counterQueue,
        mixedQueue, reservationQueue, reservationCounterQueue, reservationBoothQueue,
        storeQueue, storeCounterQueue, storeBoothQueue, separateQueue, nameKana, nameEn, 
        address, area, latitude, longitude, distance, sortOrder, wait, waitTimeCounter, 
        waitTimeCap, netTicketStatus, remoteTicketingManualStatus, reservationStatus, 
        checkinStatus, requireNetTicketLogin, forceLocalMode, prefecturesJisCode, 
        municipalities, municipalitiesJisCode, spot, tel, parkingInfo, reservationPagelink, 
        counterReservationsAllowed, openDate, commencementDate, cancellationMobileMinutes, 
        cancellationReservationMinutes, tablesCapacity, countersCapacity, maxCustomersMobileTable,
        minCustomersMobileTable, maxCustomersMobileCounter, minCustomersMobileCounter, 
        maxCustomersMobileCounter2, minCustomersMobileCounter2, maxCustomersMobileCounter3, 
        minCustomersMobileCounter3, maxCustomersReservationTable, minCustomersReservationTable, 
        maxCustomersReservationCounter, minCustomersReservationCounter, maxCustomersReservationCounter2, 
        minCustomersReservationCounter2, maxCustomersReservationCounter3, minCustomersReservationCounter3, 
        isAgs, waitingGroupTable, waitingGroupCounter, waitingGroupPair, localTicketingStatus,
        clientVersion, seatConfig, pairReservationsAllowed, showCheckinCode, showCheckinCodeDialog,
        waitShowType, region
    ) VALUES (
        :id, :storeStatus, :name, :waitingGroup, :timestamp, :boothQueue, :counterQueue,
        :mixedQueue, :reservationQueue, :reservationCounterQueue, :reservationBoothQueue,
        :storeQueue, :storeCounterQueue, :storeBoothQueue, :separateQueue, :nameKana, :nameEn, 
        :address, :area, :latitude, :longitude, :distance, :sortOrder, :wait, :waitTimeCounter, 
        :waitTimeCap, :netTicketStatus, :remoteTicketingManualStatus, :reservationStatus, 
        :checkinStatus, :requireNetTicketLogin, :forceLocalMode, :prefecturesJisCode, 
        :municipalities, :municipalitiesJisCode, :spot, :tel, :parkingInfo, :reservationPagelink, 
        :counterReservationsAllowed, :openDate, :commencementDate, :cancellationMobileMinutes, 
        :cancellationReservationMinutes, :tablesCapacity, :countersCapacity, :maxCustomersMobileTable,
        :minCustomersMobileTable, :maxCustomersMobileCounter, :minCustomersMobileCounter, 
        :maxCustomersMobileCounter2, :minCustomersMobileCounter2, :maxCustomersMobileCounter3, 
        :minCustomersMobileCounter3, :maxCustomersReservationTable, :minCustomersReservationTable, 
        :maxCustomersReservationCounter, :minCustomersReservationCounter, :maxCustomersReservationCounter2, 
        :minCustomersReservationCounter2, :maxCustomersReservationCounter3, :minCustomersReservationCounter3,
        :isAgs, :waitingGroupTable, :waitingGroupCounter, :waitingGroupPair, :localTicketingStatus,
        :clientVersion, :seatConfig, :pairReservationsAllowed, :showCheckinCode, :showCheckinCodeDialog,
        :waitShowType, :region
    );
    '''

    # Ensure JSON-serializable fields are handled
    for record in data:
        for key, value in record.items():
            if isinstance(value, list):
                record[key] = json.dumps(value)  # Convert lists to JSON strings
        cursor.execute(insert_sql, record)

    conn.commit()
    conn.close()

def data_processing():
    """Fetch, process, and store data."""
    hk_tz = pytz.timezone("Asia/Hong_Kong")
    now = datetime.now(hk_tz).time()
    data = get_sushi_data()
    insert_data(data)
    print(f"Data inserted successfully at {now}")

def job():
    """Scheduled job to fetch and process data within operating hours."""
    hk_tz = pytz.timezone("Asia/Hong_Kong")
    now = datetime.now(hk_tz).time()

    # Define start and end times in HK timezone
    start = datetime.strptime("09:55", "%H:%M").time()
    end = datetime.strptime("22:02", "%H:%M").time()

    if start <= now <= end:
        data_processing()
    else:
        print(f"The shop is closed at {datetime.now(hk_tz)}")

if __name__ == '__main__':
    create_database()  # Ensure database and table exist
    data_processing()
    schedule.every(600).seconds.do(job)  # Schedule job every 600 seconds

    while True:
        schedule.run_pending()
        time.sleep(1)