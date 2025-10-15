#!/usr/bin/env python3
import sys
import os
import csv
import json
import pickle

# ------------------------------ Base Class ------------------------------
class FileHandler:
    """Base class for file reading, writing, and applying changes."""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.data = []

    def read(self):
        """Read data from file."""
        raise NotImplementedError

    def write(self):
        """Write data to file."""
        raise NotImplementedError

    def display(self):
        """Display the data in a readable format."""
        print("\nModified File Content:")
        for row in self.data:
            print(','.join(map(str, row)))

    def apply_changes(self, changes):
        """Apply changes provided as 'X,Y,value'."""
        for change in changes:
            try:
                x_str, y_str, value = change.split(',', 2)
                x = int(x_str.strip())
                y = int(y_str.strip())

                if y < 0 or y >= len(self.data):
                    print(f"Warning: Row index {y} out of range. Skipping.")
                    continue
                if x < 0 or x >= len(self.data[y]):
                    print(f"Warning: Column index {x} out of range in row {y}. Skipping.")
                    continue

                self.data[y][x] = value
            except ValueError:
                print(f"Invalid change format: '{change}'. Expected format 'X,Y,value'. Skipping.")

# ------------------------------ CSV Handler ------------------------------
class CSVHandler(FileHandler):
    def read(self):
        with open(self.src, 'r', newline='') as f:
            reader = csv.reader(f)
            self.data = [row for row in reader]

    def write(self):
        with open(self.dst, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

# ------------------------------ JSON Handler ------------------------------
class JSONHandler(FileHandler):
    def read(self):
        with open(self.src, 'r') as f:
            self.data = json.load(f)

    def write(self):
        with open(self.dst, 'w') as f:
            json.dump(self.data, f, indent=4)

# ------------------------------ Pickle Handler ------------------------------
class PickleHandler(FileHandler):
    def read(self):
        with open(self.src, 'rb') as f:
            self.data = pickle.load(f)

    def write(self):
        with open(self.dst, 'wb') as f:
            pickle.dump(self.data, f)

# ------------------------------ Helper Functions ------------------------------
def print_usage():
    print(f"Usage: {sys.argv[0]} <src> <dst> <change1> <change2> ...")
    print("Example:")
    print(f"  {sys.argv[0]} data.csv new_data.json 0,0,piano 1,1,mug")
    sys.exit(1)

def list_files_in_dir(path):
    directory = os.path.dirname(path) or '.'
    print(f"\nFiles in '{directory}':")
    try:
        for f in os.listdir(directory):
            print(f" - {f}")
    except Exception as e:
        print(f"Error listing directory: {e}")

def get_handler_by_extension(file_path):
    """Return the correct handler class based on the file extension."""
    ext_map = {
        '.csv': CSVHandler,
        '.json': JSONHandler,
        '.pickle': PickleHandler
    }

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ext_map:
        print(f"Unsupported file type '{ext}'. Supported: .csv, .json, .pickle")
        sys.exit(1)

    return ext_map[ext]

# ------------------------------ Main Program ------------------------------
def main():
    if len(sys.argv) < 3:
        print_usage()

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.isfile(src):
        print(f"Error: '{src}' is not a valid file.")
        list_files_in_dir(src)
        sys.exit(1)

    # Select handlers based on extensions
    read_handler_class = get_handler_by_extension(src)
    write_handler_class = get_handler_by_extension(dst)

    # Instantiate handler using source for reading
    handler = read_handler_class(src, dst)

    try:
        handler.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Apply changes if provided
    if changes:
        handler.apply_changes(changes)

    # Display current data
    handler.display()

    # Write using destination format
    try:
        # If writing format differs, temporarily swap class
        if type(handler) != write_handler_class:
            handler.__class__ = write_handler_class
        handler.write()
        print(f"\nFile successfully saved to: {dst}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
