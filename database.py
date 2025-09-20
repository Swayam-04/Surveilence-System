import sqlite3
import datetime
from typing import List, Dict, Any, Optional
import os

class SurveillanceDatabase:
    def __init__(self, db_path: str = "surveillance.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create targets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id TEXT NOT NULL,
                name TEXT,
                target_type TEXT NOT NULL,
                position_x REAL NOT NULL,
                position_y REAL NOT NULL,
                velocity_x REAL NOT NULL,
                velocity_y REAL NOT NULL,
                acceleration_x REAL,
                acceleration_y REAL,
                rcs REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                eliminated_at TIMESTAMP,
                elimination_method TEXT,
                final_score REAL,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create target_events table for tracking position changes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS target_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                position_x REAL,
                position_y REAL,
                velocity_x REAL,
                velocity_y REAL,
                score REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (target_id) REFERENCES targets (target_id)
            )
        ''')
        
        # Create key_points table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                point_id TEXT NOT NULL,
                name TEXT,
                position_x REAL NOT NULL,
                position_y REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attack_history table for predictive analysis
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attack_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id TEXT NOT NULL,
                attack_sector INTEGER NOT NULL,
                attack_angle REAL NOT NULL,
                attack_distance REAL NOT NULL,
                target_type TEXT NOT NULL,
                attack_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                was_eliminated BOOLEAN DEFAULT FALSE,
                elimination_time REAL,
                threat_level INTEGER DEFAULT 1,
                FOREIGN KEY (target_id) REFERENCES targets (target_id)
            )
        ''')
        
        # Create sector_analysis table for storing computed predictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sector_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sector_number INTEGER NOT NULL,
                attack_count INTEGER DEFAULT 0,
                threat_level REAL DEFAULT 0.0,
                last_attack TIMESTAMP,
                vulnerability_score REAL DEFAULT 0.0,
                prediction_confidence REAL DEFAULT 0.0,
                analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_target(self, target_data: Dict[str, Any]) -> str:
        """Add a new target to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO targets (
                target_id, name, target_type, position_x, position_y,
                velocity_x, velocity_y, acceleration_x, acceleration_y, rcs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            target_data['target_id'],
            target_data.get('name', f"Target_{target_data['target_id']}"),
            target_data['target_type'],
            target_data['position'][0],
            target_data['position'][1],
            target_data['velocity'][0],
            target_data['velocity'][1],
            target_data.get('acceleration', [0, 0])[0],
            target_data.get('acceleration', [0, 0])[1],
            target_data.get('rcs', 0)
        ))
        
        target_id = target_data['target_id']
        conn.commit()
        conn.close()
        
        # Log the creation event
        self.log_target_event(target_id, 'created', target_data)
        
        return target_id
    
    def update_target_position(self, target_id: str, position: List[float], 
                             velocity: List[float], score: Optional[float] = None):
        """Update target position and log the event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update current position in targets table
        cursor.execute('''
            UPDATE targets 
            SET position_x = ?, position_y = ?, velocity_x = ?, velocity_y = ?
            WHERE target_id = ? AND status = 'active'
        ''', (position[0], position[1], velocity[0], velocity[1], target_id))
        
        conn.commit()
        conn.close()
        
        # Log the position update event
        self.log_target_event(target_id, 'position_update', {
            'position': position,
            'velocity': velocity,
            'score': score
        })
    
    def eliminate_target(self, target_id: str, elimination_method: str = "manual", 
                        final_score: Optional[float] = None):
        """Mark a target as eliminated"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Fetch latest known position and velocity to log accurate final point
        cursor.execute('''
            SELECT position_x, position_y, velocity_x, velocity_y
            FROM targets
            WHERE target_id = ?
            LIMIT 1
        ''', (target_id,))
        row = cursor.fetchone()
        latest_position = [row[0], row[1]] if row is not None else None
        latest_velocity = [row[2], row[3]] if row is not None else None

        cursor.execute('''
            UPDATE targets 
            SET eliminated_at = CURRENT_TIMESTAMP, 
                elimination_method = ?, 
                final_score = ?,
                status = 'eliminated'
            WHERE target_id = ? AND status = 'active'
        ''', (elimination_method, final_score, target_id))
        
        conn.commit()
        conn.close()
        
        # Log the elimination event
        self.log_target_event(target_id, 'eliminated', {
            'elimination_method': elimination_method,
            'final_score': final_score,
            'position': latest_position,
            'velocity': latest_velocity
        })
    
    def log_target_event(self, target_id: str, event_type: str, event_data: Dict[str, Any]):
        """Log a target event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO target_events (
                target_id, event_type, position_x, position_y, 
                velocity_x, velocity_y, score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            target_id,
            event_type,
            event_data.get('position', [0, 0])[0] if isinstance(event_data.get('position'), list) else None,
            event_data.get('position', [0, 0])[1] if isinstance(event_data.get('position'), list) else None,
            event_data.get('velocity', [0, 0])[0] if isinstance(event_data.get('velocity'), list) else None,
            event_data.get('velocity', [0, 0])[1] if isinstance(event_data.get('velocity'), list) else None,
            event_data.get('score')
        ))
        
        conn.commit()
        conn.close()
    
    def add_key_point(self, point_id: str, position: List[float], name: str = None):
        """Add a key point to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO key_points (point_id, name, position_x, position_y)
            VALUES (?, ?, ?, ?)
        ''', (point_id, name, position[0], position[1]))
        
        conn.commit()
        conn.close()
    
    def get_active_targets(self) -> List[Dict[str, Any]]:
        """Get all currently active targets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_id, name, target_type, position_x, position_y,
                   velocity_x, velocity_y, acceleration_x, acceleration_y, rcs,
                   created_at
            FROM targets 
            WHERE status = 'active'
            ORDER BY created_at DESC
        ''')
        
        targets = []
        for row in cursor.fetchall():
            targets.append({
                'target_id': row[0],
                'name': row[1],
                'target_type': row[2],
                'position': [row[3], row[4]],
                'velocity': [row[5], row[6]],
                'acceleration': [row[7], row[8]] if row[7] is not None else None,
                'rcs': row[9],
                'created_at': row[10]
            })
        
        conn.close()
        return targets
    
    def get_eliminated_targets(self) -> List[Dict[str, Any]]:
        """Get all eliminated targets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_id, name, target_type, position_x, position_y,
                   velocity_x, velocity_y, acceleration_x, acceleration_y, rcs,
                   created_at, eliminated_at, elimination_method, final_score
            FROM targets 
            WHERE status = 'eliminated'
            ORDER BY eliminated_at DESC
        ''')
        
        targets = []
        for row in cursor.fetchall():
            targets.append({
                'target_id': row[0],
                'name': row[1],
                'target_type': row[2],
                'position': [row[3], row[4]],
                'velocity': [row[5], row[6]],
                'acceleration': [row[7], row[8]] if row[7] is not None else None,
                'rcs': row[9],
                'created_at': row[10],
                'eliminated_at': row[11],
                'elimination_method': row[12],
                'final_score': row[13]
            })
        
        conn.close()
        return targets
    
    def get_target_history(self, target_id: str) -> List[Dict[str, Any]]:
        """Get complete history of a specific target"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT event_type, position_x, position_y, velocity_x, velocity_y,
                   score, timestamp
            FROM target_events 
            WHERE target_id = ?
            ORDER BY timestamp ASC
        ''', (target_id,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'event_type': row[0],
                'position': [row[1], row[2]] if row[1] is not None else None,
                'velocity': [row[3], row[4]] if row[3] is not None else None,
                'score': row[5],
                'timestamp': row[6]
            })
        
        conn.close()
        return events
    
    def get_target_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about targets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total targets
        cursor.execute('SELECT COUNT(*) FROM targets')
        total_targets = cursor.fetchone()[0]
        
        # Active targets
        cursor.execute('SELECT COUNT(*) FROM targets WHERE status = "active"')
        active_targets = cursor.fetchone()[0]
        
        # Eliminated targets
        cursor.execute('SELECT COUNT(*) FROM targets WHERE status = "eliminated"')
        eliminated_targets = cursor.fetchone()[0]
        
        # Targets by type
        cursor.execute('''
            SELECT target_type, COUNT(*) 
            FROM targets 
            GROUP BY target_type
        ''')
        targets_by_type = dict(cursor.fetchall())
        
        # Average time to elimination
        cursor.execute('''
            SELECT AVG(
                (julianday(eliminated_at) - julianday(created_at)) * 24 * 60 * 60
            ) 
            FROM targets 
            WHERE status = "eliminated"
        ''')
        avg_time_to_elimination = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_targets': total_targets,
            'active_targets': active_targets,
            'eliminated_targets': eliminated_targets,
            'targets_by_type': targets_by_type,
            'avg_time_to_elimination_seconds': avg_time_to_elimination
        }
    
    def cleanup_old_events(self, days_to_keep: int = 30):
        """Clean up old event logs to prevent database bloat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM target_events 
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days_to_keep))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def log_attack_event(self, target_id: str, position: List[float], target_type: str, threat_level: int = 1):
        """Log an attack event for predictive analysis"""
        import math
        
        # Calculate sector (0-11 for 12 sectors of 30 degrees each)
        angle = math.atan2(position[1], position[0])
        if angle < 0:
            angle += 2 * math.pi
        sector = int(angle / (math.pi / 6)) % 12
        
        # Calculate distance from center
        distance = math.sqrt(position[0]**2 + position[1]**2)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO attack_history (
                target_id, attack_sector, attack_angle, attack_distance,
                target_type, threat_level
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (target_id, sector, angle, distance, target_type, threat_level))
        
        conn.commit()
        conn.close()
    
    def get_attack_predictions(self) -> Dict[str, Any]:
        """Get predictive analysis of attack patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get attack counts by sector for last 30 days
        cursor.execute('''
            SELECT attack_sector, COUNT(*) as attack_count, 
                   AVG(threat_level) as avg_threat,
                   MAX(attack_timestamp) as last_attack
            FROM attack_history 
            WHERE attack_timestamp > datetime('now', '-30 days')
            GROUP BY attack_sector
            ORDER BY attack_count DESC
        ''')
        
        sector_data = cursor.fetchall()
        
        # Get recent attack patterns (last 7 days)
        cursor.execute('''
            SELECT attack_sector, target_type, COUNT(*) as count
            FROM attack_history 
            WHERE attack_timestamp > datetime('now', '-7 days')
            GROUP BY attack_sector, target_type
            ORDER BY count DESC
        ''')
        
        recent_patterns = cursor.fetchall()
        
        # Calculate vulnerability scores
        vulnerability_scores = {}
        for sector, count, avg_threat, last_attack in sector_data:
            # Higher score for more attacks, recent attacks, and higher threat levels
            recency_factor = 1.0
            if last_attack:
                days_ago = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_attack.replace('Z', '+00:00'))).days
                recency_factor = max(0.1, 1.0 - (days_ago / 30.0))
            
            vulnerability_scores[sector] = count * avg_threat * recency_factor
        
        # Find most vulnerable sectors
        most_vulnerable = sorted(vulnerability_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Get threat type patterns
        threat_types = {}
        for sector, target_type, count in recent_patterns:
            if sector not in threat_types:
                threat_types[sector] = {}
            threat_types[sector][target_type] = count
        
        conn.close()
        
        return {
            'sector_vulnerability': vulnerability_scores,
            'most_vulnerable_sectors': most_vulnerable,
            'threat_patterns': threat_types,
            'total_attacks_30d': sum(count for _, count, _, _ in sector_data),
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
    
    def get_sector_heatmap_data(self) -> List[Dict[str, Any]]:
        """Get data for sector heatmap visualization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT attack_sector, COUNT(*) as attack_count,
                   AVG(threat_level) as avg_threat,
                   MAX(attack_timestamp) as last_attack
            FROM attack_history 
            WHERE attack_timestamp > datetime('now', '-7 days')
            GROUP BY attack_sector
        ''')
        
        heatmap_data = []
        for sector, count, avg_threat, last_attack in cursor.fetchall():
            heatmap_data.append({
                'sector': sector,
                'attack_count': count,
                'threat_level': avg_threat,
                'last_attack': last_attack,
                'angle_start': sector * 30,
                'angle_end': (sector + 1) * 30
            })
        
        conn.close()
        return heatmap_data
