# Flask Inventory Management System (MongoDB)

A full-stack Flask web application for managing product inventory across multiple warehouse locations, integrated with a MongoDB database. Users can manage products, locations, and product movements, and view real-time stock balances per location.

## Tech Stack

- **Backend**: Flask, Flask-PyMongo
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Database**: MongoDB
- **Tools**: python-dotenv

## Features

- Product Management (Add/Edit/Delete/View)
- Location Management (Add/Edit/Delete/View)
- 
- Product Movement Tracking (with timestamps)
- Dynamic Stock Report per Warehouse
- Form validation and error messages
- Reusable layout and navbar templates
- Responsive dashboard UI

## Setup and Configuration

### 1. Prerequisites

- Python 3.x
- MongoDB (local or cloud instance)
- Pip (Python package installer)

### 2. Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Flask-Inventory-Management-System
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Database Configuration

1.  **Create a `.env` file** in the root directory of the project.

2.  **Add your MongoDB connection string** to the `.env` file. The application will connect to a database named `inventory_db`.

    ```env
    MONGO_URI="mongodb://localhost:27017/inventory_db"
    SECRET_KEY="your-secret-key-here"
    ```

### 4. Initialize the Database

Run the `database_setup.py` script to clear any existing data and populate the database with sample products, locations, and movements.

```bash
python database_setup.py
```

### 5. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

## Screenshots

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/85e32c9c-5104-4e5a-9e7a-2ff76ed2352a" />
