import subprocess

segment_count = [30, 60, 90, 120]
for c in segment_count:
        for _ in range(5):
                segment_count_arg = ["--segment_count", str(c)]
                subprocess.run("python robustness_tester.py --segment_count " + str(c) + " --resolution 3000 --measure_generation")