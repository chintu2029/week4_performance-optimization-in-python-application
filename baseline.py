
"""
Original Student Marks Processing Application.
This version uses inefficient techniques for comparison.
"""

def process_students(records):
    # Find unique student IDs using a list.
    unique_ids = []

    for record in records:
        if record["student_id"] not in unique_ids:
            unique_ids.append(record["student_id"])

    # Find unique subjects using a list.
    subjects = []

    for record in records:
        if record["subject"] not in subjects:
            subjects.append(record["subject"])

    subject_totals = {}
    subject_averages = {}
    pass_counts = {}

    # Scan the complete dataset separately for each subject.
    for subject in subjects:
        total = 0
        count = 0
        passed = 0

        for record in records:
            if record["subject"] == subject:
                total += record["marks"]
                count += 1

                if record["marks"] >= 40:
                    passed += 1

        subject_totals[subject] = total
        subject_averages[subject] = (
            round(total / count, 2) if count else 0
        )
        pass_counts[subject] = passed

    return {
        "unique_students": len(unique_ids),
        "subject_totals": subject_totals,
        "subject_averages": subject_averages,
        "pass_counts": pass_counts,
    }