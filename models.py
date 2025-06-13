import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
import time

class Drone:
    def __init__(self, id: int, max_weight: float, battery: int, speed: float, start_pos: Tuple[float, float]):
        self.id = id
        self.max_weight = max_weight  # kg
        self.battery = battery  # mAh
        self.speed = speed  # m/s
        self.start_pos = start_pos  # (x, y) metre
        self.current_pos = start_pos
        self.current_load = 0.0
        self.battery_used = 0
        
    def can_carry(self, weight: float) -> bool:
        return self.current_load + weight <= self.max_weight
    
    def battery_consumption(self, distance: float) -> int:
        # Basit batarya tüketim modeli: mesafe * ağırlık faktörü
        base_consumption = distance * 0.1  # mAh per meter
        weight_factor = 1 + (self.current_load / self.max_weight) * 0.5
        return int(base_consumption * weight_factor)

class Delivery:
    def __init__(self, id: int, pos: Tuple[float, float], weight: float, priority: int, time_window: Tuple[str, str]):
        self.id = id
        self.pos = pos  # (x, y) metre
        self.weight = weight  # kg
        self.priority = priority  # 1-5
        self.time_window = time_window  # ("09:00", "10:00")
        self.is_delivered = False
        
    def get_time_window_minutes(self) -> Tuple[int, int]:
        """Zaman penceresini dakikaya çevirir (gün başından itibaren)"""
        start_hour, start_min = map(int, self.time_window[0].split(':'))
        end_hour, end_min = map(int, self.time_window[1].split(':'))
        return (start_hour * 60 + start_min, end_hour * 60 + end_min)

class NoFlyZone:
    def __init__(self, id: int, coordinates: List[Tuple[float, float]], active_time: Tuple[str, str]):
        self.id = id
        self.coordinates = coordinates  # Çokgen köşe noktaları
        self.active_time = active_time  # ("09:30", "11:00")
        
    def is_point_inside(self, point: Tuple[float, float]) -> bool:
        """Bir noktanın yasak bölge içinde olup olmadığını kontrol eder (Ray Casting Algorithm)"""
        x, y = point
        n = len(self.coordinates)
        inside = False
        
        p1x, p1y = self.coordinates[0]
        for i in range(1, n + 1):
            p2x, p2y = self.coordinates[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    def get_active_time_minutes(self) -> Tuple[int, int]:
        """Aktif zaman aralığını dakikaya çevirir"""
        start_hour, start_min = map(int, self.active_time[0].split(':'))
        end_hour, end_min = map(int, self.active_time[1].split(':'))
        return (start_hour * 60 + start_min, end_hour * 60 + end_min)
