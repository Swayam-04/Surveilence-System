#!/usr/bin/env python3
"""
Test script for the surveillance system database functionality
"""

from database import SurveillanceDatabase
import time

def test_database():
    """Test basic database operations"""
    print("Testing Surveillance Database...")
    
    # Initialize database
    db = SurveillanceDatabase("test_surveillance.db")
    
    # Test 1: Add a target
    print("\n1. Testing target creation...")
    target_data = {
        'target_id': 'TEST001',
        'target_type': 'fighter_jet',
        'position': [100.0, 200.0],
        'velocity': [10.0, 15.0],
        'acceleration': [0.5, 0.3],
        'rcs': 2.5,
        'name': 'Test Fighter Jet'
    }
    
    target_id = db.add_target(target_data)
    print(f"✓ Target created with ID: {target_id}")
    
    # Test 2: Update target position
    print("\n2. Testing target position update...")
    db.update_target_position('TEST001', [150.0, 250.0], [12.0, 18.0], 85.5)
    print("✓ Target position updated")
    
    # Test 3: Get active targets
    print("\n3. Testing get active targets...")
    active_targets = db.get_active_targets()
    print(f"✓ Found {len(active_targets)} active targets")
    for target in active_targets:
        print(f"  - {target['target_id']}: {target['name']} at {target['position']}")
    
    # Test 4: Eliminate target
    print("\n4. Testing target elimination...")
    db.eliminate_target('TEST001', 'test_elimination', 85.5)
    print("✓ Target eliminated")
    
    # Test 5: Get eliminated targets
    print("\n5. Testing get eliminated targets...")
    eliminated_targets = db.get_eliminated_targets()
    print(f"✓ Found {len(eliminated_targets)} eliminated targets")
    for target in eliminated_targets:
        print(f"  - {target['target_id']}: eliminated at {target['eliminated_at']}")
    
    # Test 6: Get target history
    print("\n6. Testing target history...")
    history = db.get_target_history('TEST001')
    print(f"✓ Found {len(history)} history events")
    for event in history:
        print(f"  - {event['event_type']}: {event['timestamp']}")
    
    # Test 7: Get statistics
    print("\n7. Testing statistics...")
    stats = db.get_target_statistics()
    print("✓ Statistics retrieved:")
    print(f"  - Total targets: {stats['total_targets']}")
    print(f"  - Active targets: {stats['active_targets']}")
    print(f"  - Eliminated targets: {stats['eliminated_targets']}")
    print(f"  - Targets by type: {stats['targets_by_type']}")
    
    # Test 8: Add key point
    print("\n8. Testing key point addition...")
    db.add_key_point('KP001', [0.0, 0.0], 'Radar Center')
    print("✓ Key point added")
    
    # Test 9: Cleanup old events
    print("\n9. Testing cleanup...")
    deleted_count = db.cleanup_old_events(0)  # Clean all old events
    print(f"✓ Cleaned up {deleted_count} old events")
    
    print("\n🎉 All database tests completed successfully!")
    
    # Clean up test database
    import os
    if os.path.exists("test_surveillance.db"):
        os.remove("test_surveillance.db")
        print("✓ Test database cleaned up")

if __name__ == "__main__":
    test_database()
