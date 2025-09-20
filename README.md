# Radar Surveillance System

A comprehensive multi-sensor defense network simulation system built with Flask and modern web technologies.

## Features

### 🎯 Core Functionality
- **Real-time Radar Display**: Interactive radar interface with threat tracking
- **Threat Management**: Add, track, and eliminate various threat types
- **AI-Powered Analysis**: Intelligent threat assessment and recommendations
- **Predictive Analytics**: Historical data analysis and vulnerability prediction
- **Voice Alerts**: AI voice assistant for real-time notifications

### 📊 Threat Types Supported
- Stealth Jets
- Fighter Jets  
- Cruise Missiles
- Ballistic Missiles
- Drones (Standard & Micro)
- Helicopters
- Transport Aircraft
- Unknown Threats

### 🔧 Technical Features
- **Flask Backend**: Python-based API server
- **SQLite Database**: Persistent data storage
- **Real-time Updates**: WebSocket-like functionality via polling
- **Responsive Design**: Mobile-friendly interface
- **Report Generation**: Excel, PDF, and CSV export capabilities
- **Sector Analysis**: 12-sector vulnerability heatmap
- **Predictive Modeling**: Attack pattern analysis

### 🎨 UI Components
- **Interactive Radar**: Canvas-based radar visualization
- **Threat Tables**: Real-time threat tracking
- **Settings Panel**: Customizable system parameters
- **Statistics Dashboard**: Performance metrics
- **Predictive Analysis**: Sector vulnerability visualization

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/radar-surveillance-system.git
   cd radar-surveillance-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask pandas openpyxl reportlab
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the system**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Adding Threats
1. Click "Add Threat" button
2. Fill in threat details (position, velocity, type, etc.)
3. Click "Add to Radar" to track the threat

### AI Analysis
- Enable voice alerts in settings
- AI will provide real-time recommendations
- View predictive analysis for vulnerability assessment

### Reports
- Generate Excel, PDF, or CSV reports
- Access database management tools
- View historical statistics

## Project Structure

```
radar-surveillance-system/
├── main.py                 # Flask application
├── database.py            # Database management
├── templates/
│   └── index.html         # Main interface
├── static/               # Static assets (if any)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Tailwind CSS
- **Visualization**: HTML5 Canvas
- **Reports**: Pandas, OpenPyXL, ReportLab

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DRDO Project 2025
- Multi-Sensor Defense Network
- Advanced Threat Analysis System