
#!/usr/bin/env python3

import sys
from collections import Counter


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_logs.py <log_file>")
        return 1

    file_path = sys.argv[1]
    error_counts = Counter()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                fields = line.split()

                if len(fields) < 9:
                    continue

                ip = fields[0]
                status = fields[8]

                if status.isdigit() and 500 <= int(status) <= 599:
                    error_counts[ip] += 1

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return 1

    except OSError as error:
        print(f"Error reading file: {error}")
        return 1

    print("Top 5 client IPs with HTTP 5xx errors:")

    for ip, count in error_counts.most_common(5):
        print(f"{ip}: {count}")

    if not error_counts:
        print("No HTTP 5xx errors found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
