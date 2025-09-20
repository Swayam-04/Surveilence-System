# DRDO Radar Surveillance Defense System

A comprehensive multi-sensor defense network simulation system built with Flask and modern web technologies for the Defence Research & Development Organisation (DRDO), Government of India.

## 🚀 Features

### 🎯 Core Functionality
- **Real-time Radar Display**: Interactive radar interface with threat tracking and visualization
- **Advanced Threat Management**: Add, track, eliminate, and monitor various threat types
- **AI-Powered Analysis**: Intelligent threat assessment with automatic target classification
- **Predictive Analytics**: Historical data analysis and vulnerability prediction
- **Database Integration**: Complete SQLite database with persistent data storage
- **Event Logging**: Comprehensive tracking of all target movements and events

### 📊 Threat Types Supported
- **Stealth Jets**: F-22 Raptor, F-35 Lightning (RCS: 0.01-0.1 m²)
- **Fighter Jets**: Su-30MKI, Eurofighter (RCS: 1-5 m²)
- **Cruise Missiles**: Tomahawk, BrahMos (RCS: 0.01-0.05 m²)
- **Ballistic Missiles**: Agni V, DF-ZF (RCS: 0.05-0.1 m²)
- **Drones**: Tactical and Micro UAVs (RCS: 0.001-0.05 m²)
- **Helicopters**: Apache, Mi-17 (RCS: 5-8 m²)
- **Transport Aircraft**: C-17, B-52 (RCS: 10-20 m²)
- **Unknown Threats**: Automatic classification system

### 🔧 Technical Features
- **Flask Backend**: Python-based REST API server with comprehensive endpoints
- **SQLite Database**: Multi-table database with targets, events, and analytics
- **Real-time Updates**: Live threat tracking with position updates
- **Responsive Design**: Mobile-friendly military-grade interface
- **Multi-format Export**: Excel, PDF, and CSV report generation
- **Sector Analysis**: 12-sector vulnerability heatmap with threat patterns
- **Predictive Modeling**: Attack pattern analysis and vulnerability scoring
- **Target History**: Complete tracking of target lifecycle and movements
- **Event Management**: Comprehensive logging of all system events

### 🎨 UI Components
- **Interactive Radar**: Canvas-based radar visualization with real-time updates
- **Threat Tables**: Real-time threat tracking with status indicators
- **Settings Panel**: Customizable system parameters and weights
- **Statistics Dashboard**: Performance metrics and analytics
- **Predictive Analysis**: Sector vulnerability visualization
- **Database Management**: Target creation, elimination, and history viewing
- **Export Interface**: One-click report generation in multiple formats

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/radar-surveillance-system.git
   cd radar-surveillance-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install Flask==2.3.3 pandas==2.0.3 openpyxl==3.1.2 reportlab==4.0.4 Werkzeug==2.3.7
   ```

3. **Initialize the database**
   The SQLite database will be automatically created on first run with the following tables:
   - `targets`: Main target tracking data
   - `target_events`: Event logging and position history
   - `key_points`: Strategic key points for threat assessment
   - `attack_history`: Attack pattern data for predictive analysis
   - `sector_analysis`: Sector vulnerability analysis

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the system**
   Open your browser and navigate to `http://localhost:5000`

## 🚀 Usage

### Web Interface
1. **Adding Threats**: Click "Add Threat" button and fill in threat details
2. **Real-time Tracking**: Monitor threats on the interactive radar display
3. **Target Management**: View, eliminate, and track target history
4. **Analytics**: Access predictive analysis and sector heatmaps
5. **Reports**: Generate comprehensive reports in multiple formats

### API Endpoints

#### Target Management
- `POST /get_target` - Calculate threat priority and get best target
- `GET /api/targets` - Get all targets (active, eliminated, or all)
- `POST /api/targets` - Create a new target
- `GET /api/targets/<target_id>/history` - Get target history
- `POST /api/targets/<target_id>/eliminate` - Eliminate a target

#### Analytics & Reports
- `GET /api/statistics` - Get overall system statistics
- `GET /api/predictions` - Get predictive analysis data
- `GET /api/sector-heatmap` - Get sector heatmap data
- `GET /api/export/excel` - Export data to Excel format
- `GET /api/export/pdf` - Export data to PDF format
- `GET /api/export/csv` - Export data to CSV format

#### System Management
- `POST /api/cleanup` - Clean up old event logs
- `GET /api/keypoints` - Get strategic key points

### Example API Usage

#### Create a Target
```bash
curl -X POST http://localhost:5000/api/targets \
  -H "Content-Type: application/json" \
  -d '{
    "target_id": "TGT001",
    "target_type": "fighter jet",
    "position": [100, 200],
    "velocity": [50, 30],
    "acceleration": [5, 2],
    "rcs": 2.5,
    "name": "Hostile Fighter"
  }'
```

#### Get Threat Analysis
```bash
curl -X POST http://localhost:5000/get_target \
  -H "Content-Type: application/json" \
  -d '{
    "targets": [
      [[100, 200], [50, 30], [5, 2], 2.5, "fighter jet", {"id": "TGT001"}]
    ],
    "key_points": [[0, 0], [500, 300]],
    "weight_distance": 1.0,
    "weight_threat": 100.0,
    "weight_rcs": 10.0,
    "weight_type": 50.0
  }'
```

#### Export Reports
```bash
# Excel Report
curl -O http://localhost:5000/api/export/excel

# PDF Report  
curl -O http://localhost:5000/api/export/pdf

# CSV Report
curl -O http://localhost:5000/api/export/csv
```

## 📁 Project Structure

```
pxe-surveillance-system/
├── main.py                    # Flask application with API endpoints
├── database.py               # SQLite database management and operations
├── threat_type.py            # Target classification and threat properties
├── templates/
│   └── index.html            # Main web interface (2500+ lines)
├── static/
│   └── chart.js              # Chart visualization library
├── image/
│   └── drdo.jpg              # DRDO logo and assets
├── surveillance.db           # SQLite database (auto-generated)
├── requirements.txt          # Python dependencies
├── test_database.py          # Database testing utilities
├── DATABASE_INTEGRATION_SUMMARY.md  # Database documentation
├── build/                    # PyInstaller build artifacts
├── dist/                     # Executable distribution
├── main.spec                 # PyInstaller configuration
├── drdo-surveillance.spec    # DRDO-specific build config
└── README.md                 # This documentation
```

## 🛠️ Technologies Used

### Backend
- **Flask 2.3.3**: Python web framework with REST API
- **SQLite**: Lightweight database for data persistence
- **Pandas 2.0.3**: Data analysis and Excel export
- **ReportLab 4.0.4**: PDF report generation
- **OpenPyXL 3.1.2**: Excel file manipulation

### Frontend
- **HTML5**: Modern web standards
- **CSS3**: Advanced styling with gradients and animations
- **JavaScript**: Interactive radar and real-time updates
- **Tailwind CSS**: Utility-first CSS framework
- **HTML5 Canvas**: Radar visualization and graphics

### Database Schema
- **targets**: Main target tracking (position, velocity, type, status)
- **target_events**: Event logging and position history
- **key_points**: Strategic locations for threat assessment
- **attack_history**: Attack pattern data for predictive analysis
- **sector_analysis**: Sector vulnerability scoring

## 🔧 Advanced Features

### Target Classification System
The system automatically classifies threats based on:
- **Radar Cross Section (RCS)**: Physical size and stealth characteristics
- **Velocity**: Speed and movement patterns
- **Acceleration**: Maneuverability and threat level
- **Weight Multipliers**: Threat priority scoring

### Predictive Analytics
- **Sector Vulnerability Analysis**: 12-sector threat assessment
- **Attack Pattern Recognition**: Historical data analysis
- **Threat Level Scoring**: Dynamic risk assessment
- **Heatmap Visualization**: Real-time sector threat levels

### Export Capabilities
- **Excel Reports**: Multi-sheet reports with statistics and system info
- **PDF Reports**: Professional formatted reports with charts
- **CSV Export**: Raw data for external analysis
- **Timestamped Files**: Automatic file naming with generation time

## 🔒 Security Features

### Data Protection
- **Classified Data Handling**: Secure storage of sensitive threat information
- **Event Logging**: Comprehensive audit trail of all system activities
- **Data Retention**: Configurable cleanup of old event logs
- **Access Control**: Restricted access with security level indicators

### System Monitoring
- **Real-time Status**: Live system health monitoring
- **Performance Metrics**: Response time and accuracy tracking
- **Error Handling**: Robust error management and logging
- **Database Integrity**: Automatic data validation and consistency checks

## 🚀 Deployment Options

### Development Mode
```bash
python main.py
```

### Production Build
The system includes PyInstaller configuration for creating standalone executables:
```bash
# Build executable
pyinstaller drdo-surveillance.spec

# Run from dist folder
./dist/drdo-surveillance/drdo-surveillance.exe
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]
```

## 📊 Performance Metrics

- **Target Processing**: Real-time threat analysis and classification
- **Database Operations**: Optimized queries for large datasets
- **Export Generation**: Fast report generation in multiple formats
- **Memory Usage**: Efficient resource management
- **Response Time**: Sub-second API response times

## 🐛 Troubleshooting

### Common Issues
1. **Database Connection**: Ensure SQLite file permissions
2. **Export Dependencies**: Install pandas and openpyxl for Excel exports
3. **Port Conflicts**: Change port if 5000 is occupied
4. **Memory Issues**: Clean up old event logs using `/api/cleanup`

### Debug Mode
```bash
export FLASK_DEBUG=1
python main.py
```

## 📈 Future Enhancements

- **Machine Learning**: Advanced threat prediction algorithms
- **Real-time Alerts**: Push notifications and email alerts
- **Multi-user Support**: User authentication and role-based access
- **Cloud Integration**: AWS/Azure deployment options
- **Mobile App**: Native mobile application
- **Advanced Analytics**: Machine learning-based threat analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏛️ Acknowledgments

- **Defence Research & Development Organisation (DRDO)**
- **Government of India**
- **Multi-Sensor Defense Network Project 2025**
- **Advanced Threat Analysis System Development Team**

## 📞 Support

For technical support or questions about this system, please contact the DRDO development team or create an issue in the repository.

---

**⚠️ CLASSIFIED SYSTEM - RESTRICTED ACCESS**  
*This system is designed for authorized personnel only. All data and operations are subject to security protocols.*