import csv
import matplotlib.pyplot as plt
import numpy as np
import os


runtime_generation_data_path = os.path.realpath(os.path.dirname(__file__) + r"\measurements\road_network_segments\runtime_generation_data.csv")

with open(runtime_generation_data_path, 'r') as tsvfile:
    csvreader = csv.reader(tsvfile, delimiter='\t')
    next(csvreader, None)
    
    data = [list(map(float, row)) for row in csvreader]

sorted_data = sorted(data, key=lambda x: x[0])

medians = {}
for item in sorted_data:
    seg_num = item[0]
    runtime = round(item[2], 6)

    if seg_num not in medians:
        medians[seg_num] = [runtime]
    else:
        medians[seg_num].append(runtime)

segments = list(medians.keys())
median_runtimes = [np.median(medians[seg]) for seg in segments]

plt.bar(segments, median_runtimes, width=10)
plt.xlabel('Szegmensszám (db)')
plt.ylabel('Futásidő másodpercben (s)')
plt.title('Futásidő változása a szegmensszám függvényében')

plt.xticks(segments)
plt.yticks(np.arange(0, max(median_runtimes) +10, 10))
plt.ylim(0, max(median_runtimes) + 10)

for i, val in enumerate(median_runtimes):
    plt.text(segments[i], val + 0.5, f'{val:.6f}', ha='center', va='bottom')

#plt.show()

plt.savefig('runtime_generation_runtime.png')
