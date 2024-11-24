import os
import json

# Initialize an empty list to store database names and their fields
database_list = []

# Add a new record to the database
def add_record(db_info: dict, db_records: list):
    if not db_info:
        print("Error: Database information are missing.")
        return
    
    fields = db_info["fields"]
    record = {}

    # Assign a unique Id to each record
    record["Id"] = str(len(db_records) + 1)

    for key, length in fields.items():
        if key == "Id":
            continue  # Skip ID field (auto-generated)
        field_value = input(f"Enter value for field '{key}': ")

        # Check if the input length exceeds the allowed length
        if len(field_value) > int(length):
            print(f"Error: Field '{key}' exceeds the maximum length of {length} characters.")
            return

        record[key] = field_value  # Store the input in the record dictionary

    # Add the validated record to the db_records list
    db_records.append(record)
    print("Record added successfully.")
    
    folder_path = f"databases/{db_info['name']}"
    records_file_path = os.path.join(folder_path, "records.txt")

    # Save records to records.txt
    try:
        with open(records_file_path, "w") as records_file:
            json.dump(db_records, records_file, indent=4)
    except Exception as e:
        print("An error occurred while updating records.txt:", e)

# Update an existing record
def update_record(db_info: dict, db_records: list):
    if not db_info or not db_records:
        print("Error: Database information or records are missing.")
        return
    
    fields = db_info["fields"]
    
    print("List of all records: \n")
    for record in db_records:
        for key in fields.keys():
            print(f"{key}: {record[key]}, ")
        print()    
    
    record_id = input("\nPlease enter the record Id to update: ")
    
    record_to_update = None
    for record in db_records:
        if record["Id"] == record_id:
            record_to_update = record
    
    if not record_to_update:
        print("Record not found.")
        return
    
    for key, length in fields.items():
        if key == "Id":
            continue  # Skip ID field (cannot be updated)
        new_value = input(f"Enter new value for '{key}' (or press Enter to keep current value): ")
        if new_value:
            if len(new_value) > int(length):
                print(f"Error: Field '{key}' exceeds the maximum length of {length} characters.")
                return
            record_to_update[key] = new_value
            
    # Save the updated records back to records.txt
    folder_path = f"databases/{db_info['name']}"
    records_file_path = os.path.join(folder_path, "records.txt")
    try:
        with open(records_file_path, "w") as records_file:
            json.dump(db_records, records_file, indent=4)
        print("Record updated successfully.")
    except Exception as e:
        print("An error occurred while updating records.txt:", e)        
   
# List all records
def list_records(db_info: dict, db_records: list):
    if not db_info or not db_records:
        print("Error: Database information or records are missing.")
        return
    
    fields:dict = db_info["fields"]
    
    print("List of all records: \n")
    for record in db_records:
        print("-", end=" ")
        for key in fields.keys():
            print(f"{key}: {record[key]}", end=", ")
        print()  
    
# Search specific record
def search_record(db_info: dict, db_records: list):
    if not db_info or not db_records:
        print("Error: Database information or records are missing.")
        return
    
    fields:dict = db_info["fields"]
    
    record_id = input("\nPlease enter the record Id to search: ")
    
    record_to_search = None
    for record in db_records:
        if record["Id"] == record_id:
            record_to_search = record
    
    if not record_to_search:
        print("Record not found.")
        return
    
    for field in fields.keys():
        print(f"{field}: {record_to_search[field]}")

# Delete specific record
def  delete_record(db_info: dict, db_records: list):
    if not db_info or not db_records:
        print("Error: Database information or records are missing.")
        return
    
    record_id = input("\nEnter the record ID to delete: ")
    updated_records = [record for record in db_records if record["Id"] != record_id]

    if len(updated_records) == len(db_records):
        print(f"No record found with ID '{record_id}'.")
        return

    folder_path = f"databases/{db_info['name']}"
    records_file_path = os.path.join(folder_path, "records.txt")
    try:
        with open(records_file_path, "w") as records_file:
            json.dump(updated_records, records_file, indent=4)
        print(f"Record with ID '{record_id}' has been deleted.")
    except Exception as e:
        print("An error occurred while updating records.txt:", e)
    

# Create Database
def create_database():
    database_name = input("Please enter the name of your database: ").strip()
    if not database_name:
        print("Error: Database name cannot be empty.")
        return
    
    if find_database(database_name):
        print(f"Database '{database_name}' already exists.")
        return

    # Get field names
    try:
        num_fields = int(input("Enter the number of fields you want to add: "))
        field_names = {"Id": 12}  # Default ID field with length 12
      
        for i in range(num_fields):
            user_input = input(f"Enter field {i+1} details in the format 'name, length': ")
            try:
                field_name, field_length = user_input.split(', ')
                if not field_length.isdigit():
                    raise ValueError
                field_names[field_name.strip()] = int(field_length)
            except ValueError:
                print("Invalid input. Please use the format 'name, length'.")
                return

    except ValueError:
        print("Invalid input. Number of fields must be an integer.")
        return

    # Store database with field names
    database_list.append({
        'name': database_name,
        'fields': field_names,
    })
    
    # Define the folder and file paths
    folder_path = f"databases/{database_name}"
    os.makedirs(folder_path, exist_ok=True)

    # Save database info and initialize records
    try:
        with open(os.path.join(folder_path, "info.txt"), "w") as info_file:
            json.dump({"name": database_name, "fields": field_names}, info_file, indent=4)
        with open(os.path.join(folder_path, "records.txt"), "w") as records_file:
            json.dump([], records_file)
        print(f"Database '{database_name}' created successfully.")
    except Exception as e:
        print("An error occurred while creating the database:", e)
      

# Read database information
def read_database_info(database_name: str):
    # Find the files in the database directory
    files = find_database(database_name)
    
    if files:
        for file in files:
            if file.endswith("info.txt"):
                # Read the content of info.txt
                try:
                    with open(file, "r") as f:
                        data = json.load(f)  # Parse JSON data
                    return data
                except Exception as e:
                    print("An error occurred while reading info.txt:", e)
                    return None
    else:
        print(f"No info.txt file found for database '{database_name}'.")
        return None      
    
# Read database records    
def read_database_records(database_name: str):
    # Find the files in the database directory
    files = find_database(database_name)
    
    if files:
        for file in files:
            if file.endswith("records.txt"):
                # Read the content of records.txt
                try:
                    with open(file, "r") as f:
                        data = json.load(f)  # Parse JSON data
                    return data
                except Exception as e:
                    print("An error occurred while reading records.txt:", e)
                    return None
    else:
        print(f"No records.txt file found for database '{database_name}'.")
        return None            

# Find existing database
def find_database(database_name: str):
    if not database_name:
        return None
    
    directory_path = f"databases/{database_name}"
    if os.path.isdir(directory_path):
         files = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]
         
         return files
    else:
        return None

# Open database to perform further operations
def open_database():
    
    databases = os.listdir('databases')
    
    if not databases:
        print("No databases available.")
        return

    print("Available databases:")
    for db in databases:
        print(f"- {db}")

    database_name = input("Enter the name of the database you want to open: ")
    
    database_info = read_database_info(database_name)
    database_records = read_database_records(database_name)
    
    if database_info:
        print(f"Opening database '{database_info['name']}' with fields & length: {database_info['fields']}")
        print("\nPress - 1 to Add record\nPress - 2 to Update existing record\nPress - 3 to Search record\nPress - 4 to List all records\nPress - 5 to Delete a records\nPress - 6 to Exit ")
        
        choice = input("\nPlease enter your choice: ").strip()
        
        match choice:
            case "1":
                add_record(database_info, database_records)
            case "2":
                update_record(database_info, database_records)
            case "3":
                search_record(database_info, database_records)
            case "4":
                list_records(database_info, database_records)    
            case "5":
                delete_record(database_info, database_records)
            case "6":
                print(f"Exiting Database - {database_info['name']}")
            case _:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")    
    else:
        print(f"Database '{database_name}' does not exist.")

# Main Program
def main():
    while True:
        print("\nWelcome to NED DBMS - Your Own Database Management System")
        print("Press 1 to create a new database")
        print("Press 2 to open an existing database")
        print("Press 3 to exit")

        choice = input("Please enter your choice: ").strip()

        match choice:
            case "1":
                create_database()
            case "2":
                open_database()
            case "3":
                print("Exiting NED DBMS. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
