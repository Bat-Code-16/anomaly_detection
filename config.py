import psycopg2
import pandas as pd
from datetime import datetime

db_params1 = {     # ele database connection
    "dbname": "edge",
    "user": "analyst",
    "password": "analyst**",
    "host": "rdpms.in",
    "port": "5432"

}

def date_to_ts(start_date,end_date):
    ts=(start_date.timestamp())*1000,
    te=(end_date.timestamp())*1000,
    return ts, te

def get_data(cursor):
    get_data_sql="""
    SELECT * 
    FROM
        public.history
    LIMIT 100
    """
    cursor.execute(get_data_sql)
    rows=cursor.fetchall()
    return rows

def get_data(cursor, ts, tt):
#     get_data_sql = """
#     SELECT 
#         h.ts,
#         h.deviceid,
#         h."key",
#         h.long_v
#     FROM 
#         public.history h
#     JOIN 
#         public.device d ON h.deviceid = d.deviceid 
#     WHERE 
#         d.typeid = '69a18cc9-88d4-4b9a-87ac-4f58fceec109'
#         AND h."key" IN ('OC', 'OT', 'PC') 
#         AND h.ts BETWEEN %s AND %s
#     ORDER BY 
#         h.ts ASC
#     LIMIT 100;
#     """
    
#     # get_data_sql = """
#     # SELECT 
#     #     h.ts,
#     #     h.deviceid,
#     #     h."key",
#     #     h.long_v
#     # FROM 
#     #     public.history h
#     # JOIN 
#     #     public.device d ON h.deviceid = d.deviceid 
#     # WHERE 
#     #     d.typeid = '69a18cc9-88d4-4b9a-87ac-4f58fceec109' AND d.customer_id='50bc6230-3efb-11ed-818c-150801d2970c'
#     #     AND h."key" IN ('OC', 'OT', 'PC') 
#     #     AND h.ts BETWEEN %s AND %s
#     # ORDER BY 
#     #     h.ts ASC
#     #     LIMIT 100;
#     # """
    
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
        d.typeid = '5e2684a1-0725-415f-9cd3-3b8159cdda45' AND d.customer_id='50bc6230-3efb-11ed-818c-150801d2970c'
        AND h."key" IN ('VR', 'IR', 'IF') 
        AND h.ts BETWEEN %s AND %s
    ORDER BY
        h.ts ASC
        LIMIT 100;
    """
    
    cursor.execute(get_data_sql, (ts, tt))
    rows = cursor.fetchall()
    
    
    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['Timestamp', 'DeviceID', 'Key', 'Long Value'])

    
    # Pivot the DataFrame
    df_pivot = df.pivot_table(index=['Timestamp', 'DeviceID'], columns='Key', values='Long Value', aggfunc='first').reset_index()

    
    return df_pivot

def main():
    
    conn = cursor = None
    start_date=datetime(2024, 7, 30)
    end_date=datetime(2024, 8, 1)
    try:
        conn = psycopg2.connect(**db_params1)
        cursor = conn.cursor()
        print("ele connected")
        
        ts,tt=date_to_ts(start_date,end_date)
        #Fetch the data for the specified time range
        df = get_data(cursor, ts, tt)

        csv_file_path = "C:/Users/HP/Downloads/output_data1.csv"

        df.to_csv(csv_file_path, index=False)  # Save DataFrame to CSV
        
        # print(get_data(cursor))

        

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

