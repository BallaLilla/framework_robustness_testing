import matplotlib.pyplot as plt

class Analyzer:

    def analyze_concrete_road_network_generation_time_depending_segment_counts(self, road_segments):
        generation_times = [entry.get('generation_time', 0) for entry in road_segments]
        segment_counts = [entry.get('segment_count', 0) for entry in road_segments]

        plt.plot(segment_counts, generation_times, marker='o', linestyle='-')
        plt.title('Concrete Road Network Generation Time Depending on Segment Counts')
        plt.xlabel('Segment Counts')
        plt.ylabel('Generation Time')
        plt.show()