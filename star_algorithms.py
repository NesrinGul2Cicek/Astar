import heapq
import math
from typing import List, Tuple, Dict, Optional
from models import Drone,Delivery,NoFlyZone

class AStarPathfinder:
    def __init__(self, no_fly_zones: List[NoFlyZone]):
        self.no_fly_zones = no_fly_zones
        
    def heuristic(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Euclidean distance + no-fly zone penalty"""
        base_distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        
        # No-fly zone cezası
        penalty = 0
        for zone in self.no_fly_zones:
            if zone.is_point_inside(pos1) or zone.is_point_inside(pos2):
                penalty += 1000  # Büyük ceza
                
        return base_distance + penalty
    
    def get_neighbors(self, pos: Tuple[float, float], step_size: float = 10.0) -> List[Tuple[float, float]]:
        """8 yönlü hareket"""
        x, y = pos
        neighbors = []
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dx, dy in directions:
            new_x = x + dx * step_size
            new_y = y + dy * step_size
            
            # Sınırlar içinde mi kontrol et
            if 0 <= new_x <= 500 and 0 <= new_y <= 500:
                neighbors.append((new_x, new_y))
                
        return neighbors
    
    def find_path(self, start: Tuple[float, float], goal: Tuple[float, float], 
                  drone: Drone, delivery: Delivery) -> Tuple[List[Tuple[float, float]], float]:
        """A* algoritması ile rota bulma"""
        
        # Başlangıç ve hedef yasak bölgede mi kontrol et
        for zone in self.no_fly_zones:
            if zone.is_point_inside(start) or zone.is_point_inside(goal):
                return [], float('inf')  # Rota bulunamaz
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        visited = set()
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Hedefe ulaştık mı?
            if math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2) < 10:
                # Yolu yeniden oluştur
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                path.append(goal)
                
                # Toplam maliyeti hesapla
                total_cost = self.calculate_path_cost(path, drone, delivery)
                return path, total_cost
            
            # Komşuları kontrol et
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                
                # Yasak bölgede mi kontrol et
                in_no_fly = False
                for zone in self.no_fly_zones:
                    if zone.is_point_inside(neighbor):
                        in_no_fly = True
                        break
                
                if in_no_fly:
                    continue
                
                tentative_g = g_score[current] + math.sqrt(
                    (current[0] - neighbor[0])**2 + (current[1] - neighbor[1])**2
                )
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return [], float('inf')  # Rota bulunamadı
    
    def calculate_path_cost(self, path: List[Tuple[float, float]], drone: Drone, delivery: Delivery) -> float:
        """Rota maliyetini hesapla"""
        if len(path) < 2:
            return float('inf')
        
        total_distance = 0
        for i in range(len(path) - 1):
            distance = math.sqrt((path[i][0] - path[i+1][0])**2 + (path[i][1] - path[i+1][1])**2)
            total_distance += distance
        
        # Maliyet formülü: distance × weight + (priority × 100)
        weight_factor = delivery.weight
        priority_penalty = (6 - delivery.priority) * 100  # Yüksek öncelik = düşük ceza
        
        return total_distance * weight_factor + priority_penalty