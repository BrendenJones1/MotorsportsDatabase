import React, { useState } from 'react';

const MotorsportsFilter = () => {
  // Sample motorsports data
  const sensorData = [
    { id: 1, sensorId: 'TEMP_001', vehicleId: 'MK1', trackLayout: 'Oval', sensorValue: 95.5, year: 2022 },
    { id: 2, sensorId: 'PRES_002', vehicleId: 'EV1', trackLayout: 'Street', sensorValue: 2.1, year: 2024 },
    { id: 3, sensorId: 'TEMP_002', vehicleId: 'MK4', trackLayout: 'Oval', sensorValue: 98.2, year: 2022 },
    { id: 4, sensorId: 'SPEED_003', vehicleId: 'MK3', trackLayout: 'Road', sensorValue: 180.5, year: 2023 },
    { id: 5, sensorId: 'PRES_002', vehicleId: 'MK2', trackLayout: 'Street', sensorValue: 2.3, year: 2022 }
  ];

  // Filter states
  const [filters, setFilters] = useState({
    search: '',
    sensorId: 'all',
    vehicleId: 'all',
    trackLayout: 'all',
    minSensorValue: 0,
    year: 'all'
  });

  // Get unique values for filter options
  const sensorIds = ['all', ...new Set(sensorData.map(d => d.sensorId))];
  const vehicleIds = ['all', ...new Set(sensorData.map(d => d.vehicleId))];
  const trackLayouts = ['all', ...new Set(sensorData.map(d => d.trackLayout))];
  const years = ['all', ...new Set(sensorData.map(d => d.year))];

  // Filter the data
  const filteredData = sensorData.filter(data => {
    const matchesSearch = Object.values(data).some(value => 
      value.toString().toLowerCase().includes(filters.search.toLowerCase())
    );
    const matchesSensorId = filters.sensorId === 'all' || data.sensorId === filters.sensorId;
    const matchesVehicleId = filters.vehicleId === 'all' || data.vehicleId === filters.vehicleId;
    const matchesTrackLayout = filters.trackLayout === 'all' || data.trackLayout === filters.trackLayout;
    const matchesSensorValue = data.sensorValue >= filters.minSensorValue;
    const matchesYear = filters.year === 'all' || data.year === Number(filters.year);

    return matchesSearch && matchesSensorId && matchesVehicleId && 
           matchesTrackLayout && matchesSensorValue && matchesYear;
  });

  return (
    <div style={{ display: 'flex', gap: '20px', padding: '20px' }}>
      {/* Filter Sidebar */}
      <div style={{ width: '250px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Search</h3>
          <input
            type="text"
            placeholder="Search data..."
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Sensor ID</h3>
          <select
            value={filters.sensorId}
            onChange={(e) => setFilters({...filters, sensorId: e.target.value})}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          >
            {sensorIds.map(id => (
              <option key={id} value={id}>{id}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Vehicle ID</h3>
          <select
            value={filters.vehicleId}
            onChange={(e) => setFilters({...filters, vehicleId: e.target.value})}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          >
            {vehicleIds.map(id => (
              <option key={id} value={id}>{id}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Track Layout</h3>
          <select
            value={filters.trackLayout}
            onChange={(e) => setFilters({...filters, trackLayout: e.target.value})}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          >
            {trackLayouts.map(layout => (
              <option key={layout} value={layout}>{layout}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Minimum Sensor Value: {filters.minSensorValue}</h3>
          <input
            type="range"
            min="0"
            max="200"
            value={filters.minSensorValue}
            onChange={(e) => setFilters({...filters, minSensorValue: Number(e.target.value)})}
            style={{ width: '100%' }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ marginBottom: '10px' }}>Year</h3>
          <select
            value={filters.year}
            onChange={(e) => setFilters({...filters, year: e.target.value})}
            style={{ width: '100%', padding: '8px', border: '1px solid #ddd', borderRadius: '4px' }}
          >
            {years.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Data Grid */}
      <div style={{ flex: 1 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
          {filteredData.map(data => (
            <div 
              key={data.id} 
              style={{ 
                border: '1px solid #ddd', 
                borderRadius: '8px', 
                padding: '15px',
                backgroundColor: '#f8f9fa'
              }}
            >
              <h3 style={{ marginBottom: '8px', color: '#333' }}>Sensor: {data.sensorId}</h3>
              <div style={{ fontSize: '0.9em', color: '#666' }}>
                <p>Vehicle: {data.vehicleId}</p>
                <p>Track: {data.trackLayout}</p>
                <p>Value: {data.sensorValue}</p>
                <p>Year: {data.year}</p>
              </div>
            </div>
          ))}
        </div>
        
        {filteredData.length === 0 && (
          <div style={{ textAlign: 'center', color: '#666', marginTop: '30px' }}>
            No data matches your filters
          </div>
        )}
      </div>
    </div>
  );
};

export default MotorsportsFilter;