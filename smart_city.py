# Implement mqtt message types used for pubs and subs 

class Messages:
    CHEAT_DETECTED = "cheat_detected"
    MOVEMENT_DETECTED = "movement_detected"
    
    def REWARD(points: int):
        return f"reward points={points}"
    