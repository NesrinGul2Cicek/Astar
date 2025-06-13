import numpy as np
import matplotlib.pyplot as plt
import random
import heapq
import math
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
import time
from models import Drone,Delivery,NoFlyZone
class DataGenerator:
    @staticmethod
    def generate_drones(count: int = 5) -> List[Drone]:
        drones = []
        for i in range(1, count + 1):
            drone = Drone(
                id=i,
                max_weight=random.uniform(5.0, 15.0),  # 5-15 kg
                battery=random.randint(3000, 8000),     # 3000-8000 mAh
                speed=random.uniform(8.0, 15.0),       # 8-15 m/s
                start_pos=(random.uniform(0, 100), random.uniform(0, 100))
            )
            drones.append(drone)
        return drones
    
    @staticmethod
    def generate_deliveries(count: int = 20) -> List[Delivery]:
        deliveries = []
        time_windows = [
            ("08:00", "10:00"), ("09:00", "11:00"), ("10:00", "12:00"),
            ("11:00", "13:00"), ("12:00", "14:00"), ("13:00", "15:00"),
            ("14:00", "16:00"), ("15:00", "17:00")
        ]
        
        for i in range(1, count + 1):
            delivery = Delivery(
                id=i,
                pos=(random.uniform(0, 500), random.uniform(0, 500)),
                weight=random.uniform(0.5, 5.0),  # 0.5-5 kg
                priority=random.randint(1, 5),
                time_window=random.choice(time_windows)
            )
            deliveries.append(delivery)
        return deliveries
    
    @staticmethod
    def generate_no_fly_zones(count: int = 2) -> List[NoFlyZone]:
        zones = []
        time_windows = [
            ("08:00", "18:00"), ("09:00", "17:00"), ("10:00", "14:00"),
            ("12:00", "13:00"), ("15:00", "16:00")
        ]
        
        for i in range(1, count + 1):
            # Rastgele çokgen oluştur (kare/dikdörtgen)
            center_x = random.uniform(50, 450)
            center_y = random.uniform(50, 450)
            width = random.uniform(30, 80)
            height = random.uniform(30, 80)
            
            coordinates = [
                (center_x - width/2, center_y - height/2),
                (center_x + width/2, center_y - height/2),
                (center_x + width/2, center_y + height/2),
                (center_x - width/2, center_y + height/2)
            ]
            
            zone = NoFlyZone(
                id=i,
                coordinates=coordinates,
                active_time=random.choice(time_windows)
            )
            zones.append(zone)
        return zones
