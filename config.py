import psycopg2
import pandas as pd

db_params1 = {     # ele database connection
    "dbname": "edge",
    "user": "analyst",
    "password": "analyst**",
    "host": "rdpms.in",
    "port": "5432"
}

def get_data(cursor, ts, tt):
    get_data_sql = """
    SELECT 
        h.ts,
        h.deviceid,
        h."key",
        h.long_v
    FROM 
        public.history h
    JOIN 
        public.device d ON h.deviceid = d.deviceid 
    WHERE 
        d.typeid = '69a18cc9-88d4-4b9a-87ac-4f58fceec109' 
        AND h."key" IN ('OC', 'OT', 'PC') 
        AND h.ts BETWEEN %s AND %s
    ORDER BY 
        h.ts ASC;
    """
    cursor.execute(get_data_sql, (ts, tt))
    rows = cursor.fetchall()
    
    
    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['Timestamp', 'DeviceID', 'Key', 'Long Value'])

    
    # Pivot the DataFrame
    df_pivot = df.pivot_table(index=['Timestamp', 'DeviceID'], columns='Key', values='Long Value', aggfunc='first').reset_index()

    
    return df_pivot

def main():
    conn1 = cursor1 = None
    ts = 1719772200000  # Example start timestamp
    tt = 1722450600000  # Example end timestamp

    try:
        conn1 = psycopg2.connect(**db_params1)
        cursor1 = conn1.cursor()
        print("ele connected")

        # Fetch the data for the specified time range
        df = get_data(cursor1, ts, tt)

        csv_file_path = "C:/Users/HP/Downloads/output_data.csv"

        df.to_csv(csv_file_path, index=False)  # Save DataFrame to CSV

        

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if cursor1:
            cursor1.close()
        if conn1:
            conn1.close()

if __name__ == "__main__":
    main()

