
import unittest

from baseline import process_students as baseline_process
from optimized import process_students as optimized_process
from benchmark import make_dataset


class PerformanceOptimizationTests(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(
            baseline_process([]),
            optimized_process([])
        )

    def test_known_input(self):
        records = [
            {
                "student_id": "S1",
                "subject": "Python",
                "marks": 80
            },
            {
                "student_id": "S2",
                "subject": "Python",
                "marks": 30
            },
            {
                "student_id": "S1",
                "subject": "DBMS",
                "marks": 70
            }
        ]

        expected = {
            "unique_students": 2,
            "subject_totals": {
                "DBMS": 70,
                "Python": 110
            },
            "subject_averages": {
                "DBMS": 70.0,
                "Python": 55.0
            },
            "pass_counts": {
                "DBMS": 1,
                "Python": 1
            }
        }

        self.assertEqual(baseline_process(records), expected)
        self.assertEqual(optimized_process(records), expected)

    def test_generated_dataset(self):
        records = make_dataset(size=1500, seed=7)

        self.assertEqual(
            baseline_process(records),
            optimized_process(records)
        )


if __name__ == "__main__":
    unittest.main()