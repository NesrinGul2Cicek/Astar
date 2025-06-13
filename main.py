import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
import time
from models import Drone,Delivery,NoFlyZone
from data_generator import DataGenerator
from star_algorithms import AStarPathfinder
from genetic_algorithms import GeneticAlgorithm
from performance import PerformanceAnalyzer
from visualizer import MapVisualizer

def main():
    print("Drone Teslimat Optimizasyon Sistemi")
    print("="*50)
    
    # 1. Kendi verilerinizi tanımlayın
    print("1. Veriler yükleniyor...")
    
    drones = [
    {"id": 1, "max_weight": 4.0, "battery": 12000, "speed": 8.0, "start_pos": (10.0, 10.0)},
    {"id": 2, "max_weight": 3.5, "battery": 10000, "speed": 10.0, "start_pos": (20.0, 30.0)},
    {"id": 3, "max_weight": 5.0, "battery": 15000, "speed": 7.0, "start_pos": (50.0, 50.0)},
    {"id": 4, "max_weight": 2.0, "battery": 8000, "speed": 12.0, "start_pos": (80.0, 20.0)},
    {"id": 5, "max_weight": 6.0, "battery": 20000, "speed": 5.0, "start_pos": (40.0, 70.0)}
]


    deliveries = [
    {"id": 1, "pos": (15.0, 25.0), "weight": 1.5, "priority": 3, "time_window": (0, 60)},
    {"id": 2, "pos": (30.0, 40.0), "weight": 2.0, "priority": 5, "time_window": (0, 30)},
    {"id": 3, "pos": (70.0, 80.0), "weight": 3.0, "priority": 2, "time_window": (20, 80)},
    {"id": 4, "pos": (90.0, 10.0), "weight": 1.0, "priority": 4, "time_window": (10, 40)},
    {"id": 5, "pos": (45.0, 60.0), "weight": 4.0, "priority": 1, "time_window": (30, 90)},
    {"id": 6, "pos": (25.0, 15.0), "weight": 2.5, "priority": 3, "time_window": (0, 50)},
    {"id": 7, "pos": (60.0, 30.0), "weight": 1.0, "priority": 5, "time_window": (5, 25)},
    {"id": 8, "pos": (85.0, 90.0), "weight": 3.5, "priority": 2, "time_window": (40, 100)},
    {"id": 9, "pos": (10.0, 80.0), "weight": 2.0, "priority": 4, "time_window": (15, 45)},
    {"id": 10, "pos": (95.0, 50.0), "weight": 1.5, "priority": 3, "time_window": (0, 60)},
    {"id": 11, "pos": (55.0, 20.0), "weight": 0.5, "priority": 5, "time_window": (0, 20)},
    {"id": 12, "pos": (35.0, 75.0), "weight": 2.0, "priority": 1, "time_window": (50, 120)},
    {"id": 13, "pos": (75.0, 40.0), "weight": 3.0, "priority": 3, "time_window": (10, 50)},
    {"id": 14, "pos": (20.0, 90.0), "weight": 1.5, "priority": 4, "time_window": (30, 70)},
    {"id": 15, "pos": (65.0, 65.0), "weight": 4.5, "priority": 2, "time_window": (25, 75)},
    {"id": 16, "pos": (40.0, 10.0), "weight": 2.0, "priority": 5, "time_window": (0, 30)},
    {"id": 17, "pos": (5.0, 50.0), "weight": 1.0, "priority": 3, "time_window": (15, 55)},
    {"id": 18, "pos": (50.0, 85.0), "weight": 3.0, "priority": 1, "time_window": (60, 100)},
    {"id": 19, "pos": (80.0, 70.0), "weight": 2.5, "priority": 4, "time_window": (20, 60)},
    {"id": 20, "pos": (30.0, 55.0), "weight": 1.5, "priority": 2, "time_window": (40, 80)}
]

    no_fly_zones = [
    {
        "id": 1,
        "coordinates": [(40.0, 30.0), (60.0, 30.0), (60.0, 50.0), (40.0, 50.0)],
        "active_time": (0, 120)
    },
    {
        "id": 2,
        "coordinates": [(70.0, 10.0), (90.0, 10.0), (90.0, 30.0), (70.0, 30.0)],
        "active_time": (30, 90)
    },
    {
        "id": 3,
        "coordinates": [(10.0, 60.0), (30.0, 60.0), (30.0, 80.0), (10.0, 80.0)],
        "active_time": (0, 60)
    }
]

    
    drones = [Drone(**d) for d in drones]
    deliveries = [Delivery(**t) for t in deliveries]
    no_fly_zones = [NoFlyZone(**y) for y in no_fly_zones]

    

    print(f"   ✓ {len(drones)} drone yüklendi")
    print(f"   ✓ {len(deliveries)} teslimat noktası yüklendi")
    print(f"   ✓ {len(no_fly_zones)} yasak bölge yüklendi")
 
    
    # 2. A* ile temel rotalar
    print("\n2. A* algoritması ile temel rotalar oluşturuluyor...")
    pathfinder = AStarPathfinder(no_fly_zones)
    
    basic_routes = {drone.id: [] for drone in drones}
    for i, delivery in enumerate(deliveries):
        drone = drones[i % len(drones)]  # Round-robin atama
        if drone.can_carry(delivery.weight):
            basic_routes[drone.id].append(delivery.id)
    
    print("   ✓ Temel rotalar oluşturuldu")
    
    # 3. Genetik Algoritma ile optimizasyon
    print("\n3. Genetik algoritma ile optimizasyon yapılıyor...")
    start_time = time.time()
    
    ga = GeneticAlgorithm(drones, deliveries, no_fly_zones, pathfinder)
    optimized_routes = ga.optimize(population_size=30, generations=50)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("   ✓ Optimizasyon tamamlandı")
    
    # 4. Performans analizi
    print("\n4. Performans analizi yapılıyor...")
    results = PerformanceAnalyzer.analyze_results(drones, deliveries, optimized_routes, execution_time)
    
    # 5. Görselleştirme
    print("\n5. Sonuçlar görselleştiriliyor...")
    MapVisualizer.plot_results(drones, deliveries, no_fly_zones, optimized_routes)
    
    print("\n✓ Tüm işlemler tamamlandı!")
    
    return drones, deliveries, no_fly_zones, optimized_routes, results



def run_scenarios():
    """Test senaryolarını çalıştır"""
    print("TEST SENARYOLARI")
    print("="*50)
    
    # Senaryo 1: 5 drone, 20 teslimat, 2 no-fly zone
    print("\nSenaryo 1: 5 drone, 20 teslimat, 2 yasak bölge")
    drones1 = DataGenerator.generate_drones(5)
    deliveries1 = DataGenerator.generate_deliveries(20)
    zones1 = DataGenerator.generate_no_fly_zones(2)
    
    start_time = time.time()
    pathfinder1 = AStarPathfinder(zones1)
    ga1 = GeneticAlgorithm(drones1, deliveries1, zones1, pathfinder1)
    routes1 = ga1.optimize(population_size=20, generations=30)
    time1 = time.time() - start_time
    
    results1 = PerformanceAnalyzer.analyze_results(drones1, deliveries1, routes1, time1)
    
    # Senaryo 2: 10 drone, 50 teslimat, 5 no-fly zone
    print("\nSenaryo 2: 10 drone, 50 teslimat, 5 yasak bölge")
    drones2 = DataGenerator.generate_drones(10)
    deliveries2 = DataGenerator.generate_deliveries(50)
    zones2 = DataGenerator.generate_no_fly_zones(5)
    
    start_time = time.time()
    pathfinder2 = AStarPathfinder(zones2)
    ga2 = GeneticAlgorithm(drones2, deliveries2, zones2, pathfinder2)
    routes2 = ga2.optimize(population_size=30, generations=40)
    time2 = time.time() - start_time
    
    results2 = PerformanceAnalyzer.analyze_results(drones2, deliveries2, routes2, time2)
    
    # Karşılaştırma
    print(f"\nKARŞILAŞTIRMA:")
    print(f"Senaryo 1 - Tamamlanma: {results1['completion_rate']:.1f}%, Süre: {results1['execution_time']:.2f}s")
    print(f"Senaryo 2 - Tamamlanma: {results2['completion_rate']:.1f}%, Süre: {results2['execution_time']:.2f}s")

if __name__ == "__main__":
    # Ana demo
    main()
    
    # Test senaryolarını çalıştırmak isterseniz:
    run_scenarios()