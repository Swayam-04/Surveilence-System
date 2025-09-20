# Format: [rcs_min (m²), rcs_max (m²), velocity_min (m/s), velocity_max (m/s), acceleration_min (m/s²), acceleration_max (m/s²), weight_multiplier]
TARGET_TYPE_PROPERTIES = {
    # Stealth Fighter (e.g., F-22 Raptor, F-35 Lightning)
    "stealth jet": [0.01, 0.1, 500, 600, 20, 30, 2.0],  # very low RCS, fast, agile

    # Multirole Fighter Jet (e.g., Su-30MKI, Eurofighter)
    "fighter jet": [1, 5, 400, 600, 10, 20, 1.8],  # high speed, moderate RCS, agile

    # Heavy Bomber or Transport Aircraft (e.g., C-17, B-52)
    "transport": [10, 20, 150, 250, 2, 5, 1.2],  # large RCS, slower speed

    # Cruise Missile (e.g., Tomahawk, BrahMos)
    "cruise missile": [0.01, 0.05, 200, 250, 40, 50, 2.2],  # very small RCS, high accel

    # Hypersonic Glide Vehicle or Ballistic Missile (e.g., Agni V, DF-ZF)
    "ballistic missile": [0.05, 0.1, 3000, 4000, 150, 200, 3.0],  # extreme speed and acceleration

    # Tactical Drone (e.g., Bayraktar TB2, MQ-1 Predator)
    "drone": [0.01, 0.05, 50, 80, 2, 5, 1.0],  # small RCS, slow, low acceleration

    # Mini Drone / Quadrotor (e.g., DJI Matrice, commercial UAV)
    "micro drone": [0.001, 0.005, 10, 30, 1, 2, 0.8],  # tiny RCS, very low speed

    # Helicopter (e.g., Apache, Mi-17)
    "helicopter": [5, 8, 50, 100, 3, 5, 1.1],  # large RCS, slow, moderate agility

    # Default fallback
    "unknown": [None, None, None, None, None, None, 0.5],  # unknown type
}

def determine_target_type(rcs, velocity, acceleration, provided_type=None):
    if provided_type:
        return provided_type

    best_match = None
    best_score = 0 

    velocity_magnitude_sq = velocity[0]**2 + velocity[1]**2 if velocity else 0
    acceleration_magnitude_sq = acceleration[0]**2 + acceleration[1]**2 if acceleration else 0

    for target_type, properties in TARGET_TYPE_PROPERTIES.items():
        rcs_min, rcs_max, velocity_min, velocity_max, accel_min, accel_max, _ = properties
        score = 0

        if rcs_min and rcs_max and rcs_min <= rcs <= rcs_max:
            score += 1
        if velocity_min and velocity_max and velocity_min**2 <= velocity_magnitude_sq <= velocity_max**2:
            score += 1
        if accel_min and accel_max and acceleration and accel_min**2 <= acceleration_magnitude_sq <= accel_max**2:
            score += 1

        if score > best_score:
            best_score = score
            best_match = target_type

    return best_match if best_match else "unknown"
