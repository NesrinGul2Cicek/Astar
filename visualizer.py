import matplotlib.pyplot as plt

class MapVisualizer:
    @staticmethod
    def plot_results(drones, deliveries, no_fly_zones, routes=None):
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))

        # Maksimum X ve Y'yi otomatik belirle
        max_x = max(
            [drone.start_pos[0] for drone in drones] +
            [delivery.pos[0] for delivery in deliveries] +
            [x for zone in no_fly_zones for x, _ in zone.coordinates]
        )
        max_y = max(
            [drone.start_pos[1] for drone in drones] +
            [delivery.pos[1] for delivery in deliveries] +
            [y for zone in no_fly_zones for _, y in zone.coordinates]
        )

        padding = 10  # Harita kenarına boşluk
        ax.set_xlim(0, max_x + padding)
        ax.set_ylim(0, max_y + padding)

        # No-fly zones
        for zone in no_fly_zones:
            coords = zone.coordinates + [zone.coordinates[0]]  # Kapalı çokgen
            xs, ys = zip(*coords)
            ax.fill(xs, ys, alpha=0.3, color='red', label=f'No-Fly Zone {zone.id}')
        
        # Teslimat noktaları
        for delivery in deliveries:
            color = 'green' if delivery.priority >= 4 else 'orange' if delivery.priority >= 2 else 'blue'
            ax.scatter(delivery.pos[0], delivery.pos[1], c=color, s=100, marker='s', 
                       label=f'Delivery {delivery.id} (P{delivery.priority})')
        
        # Drone'lar ve rotalar
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']
        for i, drone in enumerate(drones):
            color = colors[i % len(colors)]
            ax.scatter(drone.start_pos[0], drone.start_pos[1], c=color, s=200, marker='^', 
                       label=f'Drone {drone.id}')
            
            if routes and drone.id in routes:
                current_pos = drone.start_pos
                for delivery_id in routes[drone.id]:
                    delivery = next(d for d in deliveries if d.id == delivery_id)
                    ax.plot([current_pos[0], delivery.pos[0]], 
                            [current_pos[1], delivery.pos[1]], 
                            color=color, linewidth=2, alpha=0.7)
                    current_pos = delivery.pos

        ax.set_xlabel('X (metre)')
        ax.set_ylabel('Y (metre)')
        ax.set_title('Drone Teslimat Rotaları')
        ax.grid(True, alpha=0.3)

        # Legend
        handles, labels = ax.get_legend_handles_labels()
        if len(handles) > 15:
            filtered_handles = []
            filtered_labels = []
            for h, l in zip(handles, labels):
                if 'Drone' in l or 'No-Fly' in l:
                    filtered_handles.append(h)
                    filtered_labels.append(l)
            ax.legend(filtered_handles, filtered_labels, bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.show()

