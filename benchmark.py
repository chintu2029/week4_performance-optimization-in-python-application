
import csv
import cProfile
import io
import pstats
import random
import statistics
import timeit
from pathlib import Path

from baseline import process_students as baseline_process
from optimized import process_students as optimized_process


# Project folders
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"


def make_dataset(size=12000, seed=42):
    """Generate reproducible test data without external files."""

    rng = random.Random(seed)

    subjects = [
        "Python",
        "Database",
        "Networks",
        "Operating Systems",
        "AI",
    ]

    records = []

    for _ in range(size):
        records.append({
            "student_id": f"STU{rng.randint(1, max(1, size // 3)):06d}",
            "subject": subjects[rng.randrange(len(subjects))],
            "marks": rng.randint(0, 100),
        })

    return records


def profile_function(function, records, output_file):
    """Profile a function and save its statistics."""

    profiler = cProfile.Profile()

    profiler.enable()
    function(records)
    profiler.disable()

    output = io.StringIO()

    stats = pstats.Stats(profiler, stream=output)
    stats.sort_stats("cumulative")
    stats.print_stats(20)

    output_file.write_text(
        output.getvalue(),
        encoding="utf-8"
    )


def main():
    RESULTS.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)

    # Generate data automatically.
    records = make_dataset()

    print("=" * 50)
    print("STUDENT MARKS PERFORMANCE OPTIMIZATION")
    print("=" * 50)

    print(f"Dataset size: {len(records)} records")

    # 1. Verify that both versions produce identical results.
    baseline_result = baseline_process(records)
    optimized_result = optimized_process(records)

    assert baseline_result == optimized_result, (
        "ERROR: Outputs do not match!"
    )

    print("Correctness check: PASS")

    # 2. Benchmark both implementations.
    repeats = 5
    number = 3

    baseline_samples = timeit.repeat(
        lambda: baseline_process(records),
        repeat=repeats,
        number=number
    )

    optimized_samples = timeit.repeat(
        lambda: optimized_process(records),
        repeat=repeats,
        number=number
    )

    baseline_seconds = [
        sample / number for sample in baseline_samples
    ]

    optimized_seconds = [
        sample / number for sample in optimized_samples
    ]

    baseline_median = statistics.median(baseline_seconds)
    optimized_median = statistics.median(optimized_seconds)

    speedup = (
        baseline_median / optimized_median
        if optimized_median > 0 else 0
    )

    improvement = (
        (baseline_median - optimized_median)
        / baseline_median * 100
        if baseline_median > 0 else 0
    )

    # 3. Save detailed benchmark measurements.
    csv_file = RESULTS / "benchmark_results.csv"

    with csv_file.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Implementation",
            "Dataset Records",
            "Median Seconds Per Run",
            "Repeat Samples In Seconds"
        ])

        writer.writerow([
            "Baseline",
            len(records),
            f"{baseline_median:.6f}",
            ";".join(f"{x:.6f}" for x in baseline_seconds)
        ])

        writer.writerow([
            "Optimized",
            len(records),
            f"{optimized_median:.6f}",
            ";".join(f"{x:.6f}" for x in optimized_seconds)
        ])

    # 4. Save cProfile reports.
    profile_function(
        baseline_process,
        records,
        RESULTS / "baseline_cprofile.txt"
    )

    profile_function(
        optimized_process,
        records,
        RESULTS / "optimized_cprofile.txt"
    )

    # 5. Generate a report with actual measured values.
    report = f"""# Week 4: Performance Optimization in Python Applications

## 1. Objective

To identify performance bottlenecks in a Python application,
apply optimization techniques, and compare performance before
and after optimization.

## 2. Application Description

The Student Marks Processing Application processes generated
student marks records. It calculates the number of unique
students, total marks per subject, average marks, and pass
counts. A mark of 40 or above is considered a pass.

Dataset size: {len(records)} records.

## 3. Baseline Performance Issues

1. List membership checks can be slow for large collections.
2. Unique subjects are found using repeated list searches.
3. The original program scans the dataset separately for each
   subject, repeating work unnecessarily.

## 4. Optimization Techniques

1. Replaced list-based unique ID collection with a set.
2. Used defaultdict to aggregate subject statistics.
3. Processed the records in one aggregation pass.
4. Reused totals and counts to calculate averages.

## 5. Testing and Profiling

Tools used: timeit, cProfile, and unittest.

Benchmark settings: five repeats, three executions per repeat,
and a generated dataset of {len(records)} records.

The complete output from the baseline and optimized programs
was compared before benchmarking.

Correctness check: PASS.

## 6. Performance Comparison

| Metric | Baseline | Optimized |
|---|---:|---:|
| Median runtime (seconds) | {baseline_median:.6f} | {optimized_median:.6f} |
| Relative speed | 1.00x | {speedup:.2f}x |
| Runtime reduction | 0% | {improvement:.2f}% |

The CSV file contains the timing samples.
The cProfile text files contain the profiling statistics.

## 7. Conclusion

The optimized implementation reduces repeated work by using
a set for unique student IDs and aggregating statistics in one
pass. The measurements above were obtained on the computer
used to run this script. Results may vary across systems.
"""

    report_file = REPORTS / "performance_report.md"

    report_file.write_text(
        report,
        encoding="utf-8"
    )

    # 6. Print a summary.
    print("-" * 50)
    print(f"Baseline median:  {baseline_median:.6f} seconds")
    print(f"Optimized median: {optimized_median:.6f} seconds")
    print(f"Speedup:          {speedup:.2f}x")
    print(f"Runtime reduction: {improvement:.2f}%")
    print("-" * 50)

    print("Benchmark CSV saved:", csv_file)
    print("Baseline profile saved.")
    print("Optimized profile saved.")
    print("Performance report saved:", report_file)


if __name__ == "__main__":
    main()