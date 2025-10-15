#!/usr/bin/env python3
import sys
import os
import csv


def print_usage():
    print(f"Usage: {sys.argv[0]} <src> <dst> <change1> <change2> ...")
    print('Example:')
    print(f"  {sys.argv[0]} data.csv new_data.csv 0,1,Hello 2,3,World")
    sys.exit(1)


def list_files_in_dir(path):
    directory = os.path.dirname(path) or '.'
    print(f"\nFiles in '{directory}':")
    try:
        for f in os.listdir(directory):
            print(f" - {f}")
    except Exception as e:
        print(f"Error listing directory: {e}")


def apply_changes(data, changes):
    for change in changes:
        try:
            x_str, y_str, value = change.split(',', 2)
            x = int(x_str)
            y = int(y_str)

            if y < 0 or y >= len(data):
                print(f"Warning: Row index {y} out of range. Skipping.")
                continue
            if x < 0 or x >= len(data[y]):
                print(f"Warning: Column index {x} out of range in row {y}. Skipping.")
                continue

            data[y][x] = value
        except ValueError:
            print(f"Invalid change format: '{change}'. Expected format 'X,Y,value'. Skipping.")


def display_csv(data):
    print("\nModified CSV Content:")
    for row in data:
        print(','.join(row))


def main():
    if len(sys.argv) < 3:
        print_usage()

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    # Check if source file exists
    if not os.path.isfile(src):
        print(f"Error: '{src}' is not a valid file.")
        list_files_in_dir(src)
        sys.exit(1)

    # Read CSV file
    try:
        with open(src, 'r', newline='') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    # Apply user changes
    if changes:
        apply_changes(data, changes)

    # Display modified CSV
    display_csv(data)

    # Save to destination file
    try:
        with open(dst, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"\nFile successfully saved to: {dst}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
