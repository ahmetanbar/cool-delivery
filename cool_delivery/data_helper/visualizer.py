import matplotlib.pyplot as plt


class Visualizer:

    @staticmethod
    def visualize_coordinates(events):
        coordinates = [(event.x, event.y) for event in events]
        x, y = zip(*coordinates)

        plt.figure(figsize=(8, 8))
        plt.scatter(x, y, color='red', marker='o')

        for i in range(len(events)):
            plt.annotate(f"{events[i].id}", (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        for i in range(len(events) - 1):
            plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color='blue', linestyle='-', linewidth=2)

        plt.title('TSP Coordinate Visualization')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.show()
