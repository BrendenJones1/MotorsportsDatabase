import os
import time
import pandas as pd
from GoogleDriveUpload import GoogleDriveUploader
import mysql.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def connect_to_db():
    return mysql.connector.connect( #change database connection to actual
        host="localhost",
        user="saeUser",
        password="password",
        database="formulaSAE"
    )

def extract_metadata(file_path):
    metadata = {}
    with open(file_path, 'r') as file:
        for _ in range(13):
            line = file.readline().strip().strip('"').split('","')
            if len(line) >= 2:
                key, value = line[0], line[1]
                metadata[key] = value
    return metadata

def upload_data_to_sql(file_path):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    
    try:
        # Initialize Google Drive uploader
        drive_uploader = GoogleDriveUploader()
        
        # Create a folder for the session using timestamp
        folder_name = f"Session_{time.strftime('%Y%m%d_%H%M%S')}"
        folder_id = drive_uploader.create_folder(folder_name)
        
        # Upload file to Google Drive
        file_id, web_link = drive_uploader.upload_file(file_path, folder_id)
        
        # Extract metadata and process data as before
        metadata = extract_metadata(file_path)
        data = pd.read_csv(file_path, skiprows=15)
        
        # Insert session record
        session_sql = """
        INSERT INTO sessions (
            vehicle_id, driver_name, session_date, session_time, 
            sample_rate, duration, segment_type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(session_sql, (
            metadata.get('Vehicle', ''),
            metadata.get('Racer', ''),
            metadata.get('Date', ''),
            metadata.get('Time', ''),
            metadata.get('Sample Rate', ''),
            metadata.get('Duration', ''),
            metadata.get('Segment', '')
        ))
        
        session_id = cursor.lastrowid
        
        # Save file information to database
        save_file_info_to_db(cursor, session_id, file_path, file_id, web_link)
        
        # Insert telemetry data
        for index, row in data.iterrows():
            # Basic telemetry data
            basic_sql = """
            INSERT INTO basic_telemetry (
                session_id, time_stamp, logger_temp, external_voltage,
                speed1, speed2, brake_press_f, brake_press_r,
                upshift, downshift, neutral_req, inline_acc,
                lateral_acc, vertical_acc, roll_rate, pitch_rate,
                yaw_rate, luminosity, fuel_used
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(basic_sql, (
                session_id, row['Time'], row['LoggerTemp'], 
                row['External Voltage'], row['Speed1'], row['Speed2'],
                row['BrakePressF'], row['BrakePressR'], row['Upshift'],
                row['Downshift'], row['NeutralReq'], row['InlineAcc'],
                row['LateralAcc'], row['VerticalAcc'], row['RollRate'],
                row['PitchRate'], row['YawRate'], row['Luminosity'],
                row['Fuel Used']
            ))
            
            # ECU basic data
            ecu_basic_sql = """
            INSERT INTO ecu_basic (
                session_id, time_stamp, rpm, gear, veh_speed,
                wheel_spd_fr, wheel_spd_rl, wheel_spd_rr, wheel_spd_fl,
                long_g, lateral_g, coolant_temp, air_temp, oil_temp,
                amb_air_temp, diff_oil_temp, oil_press, brake_press,
                fuel_press, barom_press, manif_press, coolant_pres,
                throttle_pos, battery_volt, fuel_level, fuel_flow,
                lambda1
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(ecu_basic_sql, (
                session_id, row['Time'], row['ECU RPM'], row['ECU Gear 2'],
                row['ECU VehSpeed'], row['ECU WheelSpdFR'], row['ECU WheelSpdRL'],
                row['ECU WheelSpdRR'], row['ECU WheelSpdFL'], row['ECU LongG'],
                row['ECU LateralG'], row['ECU CoolantTemp'], row['ECU AirTemp'],
                row['ECU OilTemp'], row['ECU Amb Air T'], row['ECU DiffOilTemp'],
                row['ECU OilPress'], row['ECU BrakePress'], row['ECU FuelPress'],
                row['ECU BaromPress'], row['ECU ManifPress'], row['ECU CoolantPres'],
                row['ECU ThrottlePos'], row['ECU BatteryVolt'], row['ECU FuelLevel'],
                row['ECU FuelFlow'], row['ECU Lambda1']
            ))
            
            # ECU advanced data
            ecu_advanced_sql = """
            INSERT INTO ecu_advanced (
                session_id, time_stamp, egt_sensor1, egt_sensor2,
                egt_sensor3, egt_sensor4, inj_pres_d, exh_cam_ang1,
                tor_dr_rpmic, ign_ang_lead, intake_cam_a1, intake_cam_a2,
                exh_cam_ang2, steer_wheel_an, launch_ign_ret, ignition_ang1,
                torqc_ign_corr, ignition_ang2, inj_dt2, launch_fu_en,
                gen_out1dt, boost_ctr_out, rel_humidity
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(ecu_advanced_sql, (
                session_id, row['Time'], row['ECU EGTSensor1'],
                row['ECU EGTSensor2'], row['ECU EGTSensor3'],
                row['ECU EGTSensor4'], row['ECU Inj Pres D'],
                row['ECU ExhCamAng1'], row['ECU TorDrRPMIC'],
                row['ECU IgnAngLead'], row['ECU IntakeCamA1'],
                row['ECU IntakeCamA2'], row['ECU ExhCamAng2'],
                row['ECU SteerWheelAn'], row['ECU LaunchIgnRet'],
                row['ECU IgnitionAng1'], row['ECU TorqCIgnCorr'],
                row['ECU IgnitionAng2'], row['ECU InjDT2'],
                row['ECU LaunchFuEn'], row['ECU GenOut1DT'],
                row['ECU BoostCtrOut'], row['ECU Rel Humidity']
            ))
            
            # Tire temperature data
            tire_temp_sql = """
            INSERT INTO tire_temperatures (
                session_id, time_stamp,
                lf_gauge_press, lf_temp_ch1, lf_temp_ch2, lf_temp_ch3,
                rf_gauge_press, rf_temp_ch1, rf_temp_ch2, rf_temp_ch3,
                lr_gauge_press, lr_temp_ch1, lr_temp_ch2, lr_temp_ch3,
                rr_gauge_press, rr_temp_ch1, rr_temp_ch2, rr_temp_ch3
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s)
            """
            
            cursor.execute(tire_temp_sql, (
                session_id, row['Time'],
                row['LF Gauge Press'], row['LF Temp Ch1'],
                row['LF Temp Ch2'], row['LF Temp Ch3'],
                row['RF Gauge Press'], row['RF Temp Ch1'],
                row['RF Temp Ch2'], row['RF Temp Ch3'],
                row['LR Guage Press'], row['LR Temp Ch1'],
                row['LR Temp Ch2'], row['LR Temp Ch3'],
                row['RR Gauge Press'], row['RR Temp Ch1'],
                row['RR Temp Ch2'], row['RR Temp Ch3']
            ))
        
        db_connection.commit()
        print(f"Data from {file_path} uploaded successfully to database and Google Drive.")
        
    except Exception as e:
        print(f"Error uploading data from {file_path}: {e}")
        db_connection.rollback()
    finally:
        cursor.close()
        db_connection.close()

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.csv'):
            print(f"New CSV file detected: {event.src_path}")
            upload_data_to_sql(event.src_path)

def monitor_folder(folder_path):
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print("Monitoring folder for new CSV files...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    folder_to_watch = "path/to/export/folder"
    monitor_folder(folder_to_watch)
