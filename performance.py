import math

class PerformanceAnalyzer:
    @staticmethod
    def analyze_results(drones, deliveries, routes, execution_time):
        total_deliveries = len(deliveries)
        completed_deliveries = sum(len(route) for route in routes.values())
        completion_rate = (completed_deliveries / total_deliveries) * 100
        
        # Enerji tüketimi hesaplama
        total_energy = 0
        for drone in drones:
            if drone.id in routes:
                current_pos = drone.start_pos
                for delivery_id in routes[drone.id]:
                    delivery = next(d for d in deliveries if d.id == delivery_id)
                    distance = math.sqrt((current_pos[0] - delivery.pos[0])**2 + 
                                       (current_pos[1] - delivery.pos[1])**2)
                    total_energy += drone.battery_consumption(distance)
                    current_pos = delivery.pos
        
        avg_energy = total_energy / len(drones) if drones else 0
        
        print(f"\n{'='*50}")
        print(f"PERFORMANS ANALİZİ")
        print(f"{'='*50}")
        print(f"Toplam Teslimat Sayısı: {total_deliveries}")
        print(f"Tamamlanan Teslimat: {completed_deliveries}")
        print(f"Tamamlanma Oranı: {completion_rate:.2f}%")
        print(f"Ortalama Enerji Tüketimi: {avg_energy:.2f} mAh")
        print(f"Algoritma Çalışma Süresi: {execution_time:.2f} saniye")
        print(f"{'='*50}")
        
        return {
            'completion_rate': completion_rate,
            'avg_energy': avg_energy,
            'execution_time': execution_time
        }