import csv
from collections import Counter

def count_unique_subject_ids(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        subject_ids = (row[4] for row in reader)
        subject_count = Counter(subject_ids)
    return subject_count

if __name__ == '__main__':
    # Example usage
    csv_file = 'files.csv'
    subject_count = count_unique_subject_ids(csv_file)
    print(subject_count)
    print(f"Number of unique subject IDs: {len(subject_count)}")