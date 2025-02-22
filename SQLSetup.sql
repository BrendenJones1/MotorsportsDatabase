
CREATE TABLE vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_name VARCHAR(50),
    vehicle_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    driver_id INT PRIMARY KEY AUTO_INCREMENT,
    driver_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT,
    driver_id INT,
    session_date DATE,
    session_time TIME,
    sample_rate INT,
    duration FLOAT,
    segment_type VARCHAR(50),
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);

-- Sensor configuration tables
CREATE TABLE sensor_types (
    type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50),
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    sensor_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_id INT,
    sensor_name VARCHAR(50),
    sensor_type_id INT,
    units VARCHAR(20),
    min_value FLOAT,
    max_value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (sensor_type_id) REFERENCES sensor_types(type_id)
);

-- Telemetry data tables
CREATE TABLE basic_telemetry (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    time_stamp FLOAT,
    logger_temp FLOAT,
    external_voltage FLOAT,
    speed1 FLOAT,
    speed2 FLOAT,
    brake_press_f FLOAT,
    brake_press_r FLOAT,
    upshift FLOAT,
    downshift FLOAT,
    neutral_req FLOAT,
    inline_acc FLOAT,
    lateral_acc FLOAT,
    vertical_acc FLOAT,
    roll_rate FLOAT,
    pitch_rate FLOAT,
    yaw_rate FLOAT,
    luminosity FLOAT,
    fuel_used FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE ecu_basic (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    time_stamp FLOAT,
    rpm FLOAT,
    gear FLOAT,
    veh_speed FLOAT,
    wheel_spd_fr FLOAT,
    wheel_spd_rl FLOAT,
    wheel_spd_rr FLOAT,
    wheel_spd_fl FLOAT,
    long_g FLOAT,
    lateral_g FLOAT,
    coolant_temp FLOAT,
    air_temp FLOAT,
    oil_temp FLOAT,
    amb_air_temp FLOAT,
    diff_oil_temp FLOAT,
    oil_press FLOAT,
    brake_press FLOAT,
    fuel_press FLOAT,
    barom_press FLOAT,
    manif_press FLOAT,
    coolant_pres FLOAT,
    throttle_pos FLOAT,
    battery_volt FLOAT,
    fuel_level FLOAT,
    fuel_flow FLOAT,
    lambda1 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE ecu_advanced (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    time_stamp FLOAT,
    egt_sensor1 FLOAT,
    egt_sensor2 FLOAT,
    egt_sensor3 FLOAT,
    egt_sensor4 FLOAT,
    inj_pres_d FLOAT,
    exh_cam_ang1 FLOAT,
    tor_dr_rpmic FLOAT,
    ign_ang_lead FLOAT,
    intake_cam_a1 FLOAT,
    intake_cam_a2 FLOAT,
    exh_cam_ang2 FLOAT,
    steer_wheel_an FLOAT,
    launch_ign_ret FLOAT,
    ignition_ang1 FLOAT,
    torqc_ign_corr FLOAT,
    ignition_ang2 FLOAT,
    inj_dt2 FLOAT,
    launch_fu_en FLOAT,
    gen_out1dt FLOAT,
    boost_ctr_out FLOAT,
    rel_humidity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

CREATE TABLE tire_temperatures (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    time_stamp FLOAT,
    lf_gauge_press FLOAT,
    lf_temp_ch1 FLOAT,
    lf_temp_ch2 FLOAT,
    lf_temp_ch3 FLOAT,
    rf_gauge_press FLOAT,
    rf_temp_ch1 FLOAT,
    rf_temp_ch2 FLOAT,
    rf_temp_ch3 FLOAT,
    lr_gauge_press FLOAT,
    lr_temp_ch1 FLOAT,
    lr_temp_ch2 FLOAT,
    lr_temp_ch3 FLOAT,
    rr_gauge_press FLOAT,
    rr_temp_ch1 FLOAT,
    rr_temp_ch2 FLOAT,
    rr_temp_ch3 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Raw sensor data table for flexible data storage
CREATE TABLE sensor_data (
    data_id INT PRIMARY KEY AUTO_INCREMENT,
    sensor_id INT,
    session_id INT,
    timestamp FLOAT,
    value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Add table for Race Studio file types
CREATE TABLE file_types (
    file_type_id INT PRIMARY KEY AUTO_INCREMENT,
    extension VARCHAR(10),
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add table for Race Studio files
CREATE TABLE session_files (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT,
    file_type_id INT,
    file_name VARCHAR(255),
    cloud_storage_url VARCHAR(2048),  -- URL to Google Drive file
    cloud_file_id VARCHAR(255),       -- Google Drive's unique file ID
    file_size_bytes BIGINT,
    upload_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (file_type_id) REFERENCES file_types(file_type_id)
);

-- Indexes for better query performance
CREATE INDEX idx_session_timestamp ON basic_telemetry(session_id, time_stamp);
CREATE INDEX idx_session_timestamp_ecu ON ecu_basic(session_id, time_stamp);
CREATE INDEX idx_session_timestamp_adv ON ecu_advanced(session_id, time_stamp);
CREATE INDEX idx_session_timestamp_tire ON tire_temperatures(session_id, time_stamp);
CREATE INDEX idx_sensor_data ON sensor_data(sensor_id, timestamp);
