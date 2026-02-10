import os
import json
import hashlib

HASH_TABLE_FILE = "hash_table.json"


def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()


def traverse_directory(directory):
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_hashes[full_path] = hash_file(full_path)
    return file_hashes


def generate_table():
    directory = input("Enter directory path to hash: ")

    if not os.path.exists(directory):
        print("Directory not found.")
        return

    hashes = traverse_directory(directory)

    with open(HASH_TABLE_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

    print("Hash table generated.")


def validate_hash():
    if not os.path.exists(HASH_TABLE_FILE):
        print("Hash table not found. Generate it first.")
        return

    with open(HASH_TABLE_FILE, "r") as f:
        stored_hashes = json.load(f)

    directory = input("Enter directory path to verify: ")

    current_hashes = traverse_directory(directory)

    for path, old_hash in stored_hashes.items():
        if path in current_hashes:
            new_hash = current_hashes[path]
            if new_hash == old_hash:
                print(f"{path} hash is valid")
            else:
                print(f"{path} hash is INVALID")
        else:
            print(f"{path} has been deleted")

    # Check for new files
    for path in current_hashes:
        if path not in stored_hashes:
            print(f"{path} is a new file")


def main():
    print("1 - Generate new hash table")
    print("2 - Verify hashes")

    choice = input("Choose an option: ")

    if choice == "1":
        generate_table()
    elif choice == "2":
        validate_hash()
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
