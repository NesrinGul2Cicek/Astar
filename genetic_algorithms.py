import matplotlib.pyplot as plt
import random
import math
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional


class GeneticAlgorithm:
    def __init__(self, drones, deliveries, no_fly_zones, pathfinder):
        self.drones = drones
        self.deliveries = deliveries
        self.no_fly_zones = no_fly_zones
        self.pathfinder = pathfinder
        
    def create_individual(self) -> Dict:
        """Rastgele bir birey (rota planı) oluştur"""
        individual = {drone.id: [] for drone in self.drones}
        available_deliveries = self.deliveries.copy()
        random.shuffle(available_deliveries)
        
        for delivery in available_deliveries:
            # Rastgele bir drone seç
            suitable_drones = [d for d in self.drones if d.can_carry(delivery.weight)]
            if suitable_drones:
                chosen_drone = random.choice(suitable_drones)
                individual[chosen_drone.id].append(delivery.id)
        
        return individual
    
    def fitness(self, individual: Dict) -> float:
        """Fitness fonksiyonu"""
        completed_deliveries = 0
        total_energy = 0
        rule_violations = 0
        
        for drone_id, delivery_ids in individual.items():
            drone = next(d for d in self.drones if d.id == drone_id)
            current_pos = drone.start_pos
            current_load = 0
            
            for delivery_id in delivery_ids:
                delivery = next(d for d in self.deliveries if d.id == delivery_id)
                
                # Kapasite kontrolü
                if current_load + delivery.weight > drone.max_weight:
                    rule_violations += 1
                    continue
                
                # Rota bul
                path, cost = self.pathfinder.find_path(current_pos, delivery.pos, drone, delivery)
                
                if path:
                    completed_deliveries += 1
                    # Enerji tüketimi hesapla
                    distance = sum(math.sqrt((path[i][0] - path[i+1][0])**2 + (path[i][1] - path[i+1][1])**2) 
                                 for i in range(len(path)-1))
                    total_energy += drone.battery_consumption(distance)
                    current_pos = delivery.pos
                    current_load += delivery.weight
                else:
                    rule_violations += 1
        
        # Fitness = teslim edilen × 500 - enerji tüketimi × 0.1 - kural ihlali × 1000
        fitness_score = completed_deliveries * 500 - total_energy * 0.1 - rule_violations * 1000
        return max(0, fitness_score)  # Negatif olmaz
    
    def crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Çaprazlama operatörü"""
        child = {drone.id: [] for drone in self.drones}
        
        # Her drone için rastgele parent seç
        for drone_id in child.keys():
            if random.random() < 0.5:
                child[drone_id] = parent1[drone_id].copy()
            else:
                child[drone_id] = parent2[drone_id].copy()
        
        return child
    
    def mutate(self, individual: Dict, mutation_rate: float = 0.1):
        """Mutasyon operatörü"""
        if random.random() < mutation_rate:
            # Rastgele bir teslimatı başka bir drone'a ver
            all_deliveries = []
            for drone_id, delivery_ids in individual.items():
                all_deliveries.extend(delivery_ids)
            
            if all_deliveries:
                # Rastgele teslimat seç
                delivery_id = random.choice(all_deliveries)
                
                # Eski konumdan kaldır
                for drone_id in individual.keys():
                    if delivery_id in individual[drone_id]:
                        individual[drone_id].remove(delivery_id)
                        break
                
                # Yeni drone'a ekle
                new_drone_id = random.choice(list(individual.keys()))
                individual[new_drone_id].append(delivery_id)
    
    def optimize(self, population_size: int = 50, generations: int = 100) -> Dict:
        """Genetik algoritma optimizasyonu"""
        # İlk popülasyonu oluştur
        population = [self.create_individual() for _ in range(population_size)]
        
        for generation in range(generations):
            # Fitness hesapla
            fitness_scores = [(individual, self.fitness(individual)) for individual in population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # En iyi %50'yi seç
            elite_size = population_size // 2
            elite = [individual for individual, _ in fitness_scores[:elite_size]]
            
            # Yeni nesil oluştur
            new_population = elite.copy()
            
            while len(new_population) < population_size:
                parent1 = random.choice(elite)
                parent2 = random.choice(elite)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)
            
            population = new_population
            
            if generation % 20 == 0:
                best_fitness = fitness_scores[0][1]
                print(f"Nesil {generation}: En iyi fitness = {best_fitness:.2f}")
        
        # En iyi bireyi döndür
        final_fitness = [(individual, self.fitness(individual)) for individual in population]
        best_individual = max(final_fitness, key=lambda x: x[1])[0]
        return best_individual