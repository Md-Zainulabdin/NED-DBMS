import os
import json

# Initialize an empty list to store database names and their fields
database_list = []

# Add a new record to the database
def add_record(db_info: dict, db_records: list):
    if not (db_info or db_records):
        print("Error: Database information or records are missing.")
        return
    
    fields:dict = db_info["fields"]
    record = {}
    
    for key, length in fields.items():
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
    if not db_info:
        print("Error: Database information are missing.")
        return None
    
    if not db_records:
        print("Error: Database records are missing.")
        return None
    
    fields:dict = db_info["fields"]
    
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
    
    fields = {field: value for field, value in fields.items() if "Id" not in field}
            
    for key, length in fields.items():
            #(or press Enter to keep current value)
            new_value = input(f"Enter a new value for '{key}': ")        
            # Check if the input length exceeds the allowed length
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
    if not db_info:
        print("Error: Database information are missing.")
        return None
    
    if not db_records:
        print("Error: Database records are missing.")
        return None
    
    fields:dict = db_info["fields"]
    
    print("List of all records: \n")
    for record in db_records:
        print("-", end=" ")
        for key in fields.keys():
            print(f"{key}: {record[key]}", end=", ")
        print()  
    
# Search specific record
def search_record(db_info: dict, db_records: list):
    if not db_info:
        print("Error: Database information are missing.")
        return None
    
    if not db_records:
        print("Error: Database records are missing.")
        return None
    
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
    if not db_info:
        print("Error: Database information are missing.")
        return None
    
    if not db_records:
        print("Error: Database records are missing.")
        return None
    
    record_id = input("\nPlease enter the record ID to delete: ")
    
    updated_records = []
    record_found = False
    
    for record in db_records:
        if record.get("Id") != record_id:
            updated_records.append(record)
        else:
            record_found = True

    if record_found:
        
         # Save the updated records back to records.txt
     
        folder_path = f"databases/{db_info['name']}"
        records_file_path = os.path.join(folder_path, "records.txt")
        try:
            with open(records_file_path, "w") as records_file:
                json.dump(updated_records, records_file, indent=4)
                print(f"Record with ID '{record_id}' has been deleted.")
        except Exception as e:
            print("An error occurred while updating records.txt:", e)
        
    else:
        print(f"No record found with ID '{record_id}'.")

    return updated_records
    

# Create Database
def create_database():
    database_name = input("Please enter the name of your database: ")
    existing_db = find_database(database_name)
    
    if existing_db:
        print(f"Database '{database_name}' already exists.")
        return

    # Get field names
    try:
        num_fields = int(input("Please enter the number of fields you want to add: "))
        field_names =  {"Id": 12}
      
        for i in range(num_fields):
            # Ask user to enter field name and length separated by a comma
            user_input = input(f"Enter field {i+1} details in the format 'name,length' (e.g., name,4): ")
    
            # Split the input into field name and length
            field_name, field_length = user_input.split(',')
            
            if not field_length.strip().isdigit():
                print("Invalid input. Please enter a valid length for the field.")
                return
            
            field_names[field_name.strip()] = int(field_length)

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
    info_file_path = os.path.join(folder_path, "info.txt")
    records_file_path = os.path.join(folder_path, "records.txt")
    
    # Create the database directory
    os.makedirs(folder_path, exist_ok=True)
    
   # Write database info to info.txt
    try:
        with open(info_file_path, "w") as info_file:
            json.dump({
                "name": database_name,
                "fields": field_names,
            }, info_file, indent=4)  # Writing JSON-formatted information for readability
    except Exception as e:
        print("An error occurred while writing to info.txt:", e)
        return

     # Initialize an empty records.txt file
    try:
        with open(records_file_path, "w") as records_file:
            records_file.write("[]")
    except Exception as e:
        print("An error occurred while creating records.txt:", e)
        return

    print(f"Database '{database_name}' created successfully with fields: {field_names}")

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
        print(f"Opening database '{database_info['name']}' with fields: {database_info['fields']}")
        print("\nPress - 1 to add record\nPress - 2 to update existing record\nPress - 3 to search record\nPress - 4 to list all records\nPress - 5 to delete a records\nPress - 6 to Exit ")
        
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
        print("\nWelcome to NedDB, Your Database Management System")
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
                print("Exiting NedDB. Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
