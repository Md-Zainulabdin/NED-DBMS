# Welcome to NedDB - Your Own Database Management System

NedDB is a lightweight, command-line-based database management system designed to allow users to create, manage, and access databases with simple functionality. Users can create database, define fields, add records, and retrieve stored information.

## Features

- **Create Databases:** Create a custom database with a unique name and custom fields.
- **Manage Fields:** Define specific fields for each database (e.g., name, age, ID).
- **Add and Retrieve Records:** Add records to databases and retrieve them as needed.
- **Persistent Storage:** Stores database metadata (info.txt) and records (records.txt) within dedicated folders.
- **Directory and File Management:** Automatically creates folders and files as required for each database.

## Getting Started

Follow these instructions to set up and run NedDB on your local machine.

### Prerequisites
 - Python 3.x installed on your system.

### Installation

1. **Clone the Repository:**

```
  git clone https://github.com/Md-Zainulabdin/NedDB.git
  cd NedDB
```

2. **Run the Application:** Start the application by running:

```
  python main.py
```

## Usage

Upon running <code>main.py</code> , the CLI menu will guide you through the various functionalities:

1. **Creating a Database**:
    - Select the option to create a new database.
    - Enter the database name and the number of fields.
    - Specify the names of the fields, which will be saved in an info.txt file inside the database folder.

2. **Opening an Existing Database:**:
    - Choose the option to open a database.
    - Enter the name of the database to access its records.
    - View fields in the <code>info.txt</code> file and add records if needed. Records are stored in <code>records.txt</code>.  

3. **Exiting the Application:**:
    - Select the option to exit the application.

## Directory Structure

When you create a database, NedDB sets up the following structure:

```
  NedDB/
  │
  └───databases/
      └───database_name/
          └── info.txt          # Contains the database name and defined fields
          └── records.txt       # Stores records added to the database
```

- **info.txt**: Stores metadata like database name and field names.
- **records.txt**: Contains the records entered by the user for each database..

## Example

```
Welcome to NedDB, Your own Database Management System
Press 1 to create a new database
Press 2 to open an existing database
Press 3 to exit
```

### Sample Database Creation

```
Please enter the name of your database: students
Please enter the number of fields you want to add: 2
Enter name of field 1: Name
Enter name of field 2: Age

Database 'students' created successfully with fields: ['Name', 'Age']
```

### Adding Records

```
Available databases:
- students
Enter the name of the database you want to open: students
Do you want to add any record in your database (Y/N): Y
Enter value for field 'Name': John Doe
Enter value for field 'Age': 21

Record added successfully.
```

## Error Handling

NedDB includes basic error handling:

- Ensures database names are unique.
- Validates user input for fields and names.
- Manages file read/write errors with descriptive messages.

## Contributing

Contributions are welcome! If you have ideas or find issues, please open an issue or submit a pull request.