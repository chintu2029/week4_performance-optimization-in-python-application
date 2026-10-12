
"""
Optimized Student Marks Processing Application.
"""

from collections import defaultdict


def process_students(records):
    # A set removes duplicate IDs efficiently.
    unique_ids = {
        record["student_id"] for record in records
    }

    # Store totals, counts, and passing counts.
    totals = defaultdict(int)
    counts = defaultdict(int)
    pass_counts = defaultdict(int)

    # Process every record once.
    for record in records:
        subject = record["subject"]
        marks = record["marks"]

        totals[subject] += marks
        counts[subject] += 1

        if marks >= 40:
            pass_counts[subject] += 1

    # Keep subject order consistent and predictable.
    subjects = sorted(totals)

    subject_totals = {
        subject: totals[subject]
        for subject in subjects
    }

    subject_averages = {
        subject: round(totals[subject] / counts[subject], 2)
        for subject in subjects
    }

    ordered_pass_counts = {
        subject: pass_counts[subject]
        for subject in subjects
    }

    return {
        "unique_students": len(unique_ids),
        "subject_totals": subject_totals,
        "subject_averages": subject_averages,
        "pass_counts": ordered_pass_counts,
    }