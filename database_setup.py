import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.get_database()

# Collections
products_collection = db.products
locations_collection = db.locations
movements_collection = db.movements

def setup_database():
    """Clears existing data and inserts sample data into the collections."""
    print("Clearing existing data...")
    products_collection.delete_many({})
    locations_collection.delete_many({})
    movements_collection.delete_many({})

    print("Inserting sample data...")

    # Sample Products
    products = [
        {"_id": "prod1", "product_name": "Laptop", "description": "15-inch, 16GB RAM"},
        {"_id": "prod2", "product_name": "Keyboard", "description": "Mechanical, RGB"},
        {"_id": "prod3", "product_name": "Mouse", "description": "Wireless, Optical"},
        {"_id": "prod4", "product_name": "Monitor", "description": "27-inch, 4K"}
    ]
    products_collection.insert_many(products)
    print(f"{len(products)} products inserted.")

    # Sample Locations
    locations = [
        {"_id": "loc1", "location_name": "Warehouse A"},
        {"_id": "loc2", "location_name": "Warehouse B"},
        {"_id": "loc3", "location_name": "Storefront"}
    ]
    locations_collection.insert_many(locations)
    print(f"{len(locations)} locations inserted.")

    # Sample Movements
    movements = [
        # Inbound to Warehouse A
        {"timestamp": datetime(2023, 1, 10), "from_location": None, "to_location": "loc1", "product_id": "prod1", "qty": 10},
        {"timestamp": datetime(2023, 1, 11), "from_location": None, "to_location": "loc1", "product_id": "prod2", "qty": 50},
        
        # Inbound to Warehouse B
        {"timestamp": datetime(2023, 1, 12), "from_location": None, "to_location": "loc2", "product_id": "prod3", "qty": 100},
        {"timestamp": datetime(2023, 1, 13), "from_location": None, "to_location": "loc2", "product_id": "prod4", "qty": 20},

        # Transfer from Warehouse A to B
        {"timestamp": datetime(2023, 2, 1), "from_location": "loc1", "to_location": "loc2", "product_id": "prod1", "qty": 5},

        # Transfer from Warehouse B to Storefront
        {"timestamp": datetime(2023, 2, 15), "from_location": "loc2", "to_location": "loc3", "product_id": "prod3", "qty": 20},
        {"timestamp": datetime(2023, 2, 16), "from_location": "loc2", "to_location": "loc3", "product_id": "prod4", "qty": 5},

        # Outbound (Sale) from Storefront
        {"timestamp": datetime(2023, 3, 1), "from_location": "loc3", "to_location": None, "product_id": "prod3", "qty": 2},
        {"timestamp": datetime(2023, 3, 2), "from_location": "loc3", "to_location": None, "product_id": "prod4", "qty": 1},

        # More movements to reach ~20
        {"timestamp": datetime(2023, 3, 5), "from_location": "loc1", "to_location": "loc3", "product_id": "prod2", "qty": 10},
        {"timestamp": datetime(2023, 3, 6), "from_location": "loc3", "to_location": None, "product_id": "prod2", "qty": 3},
        {"timestamp": datetime(2023, 3, 10), "from_location": None, "to_location": "loc1", "product_id": "prod1", "qty": 5},
        {"timestamp": datetime(2023, 3, 12), "from_location": "loc1", "to_location": "loc2", "product_id": "prod1", "qty": 2},
        {"timestamp": datetime(2023, 3, 15), "from_location": None, "to_location": "loc2", "product_id": "prod2", "qty": 30},
        {"timestamp": datetime(2023, 4, 1), "from_location": "loc2", "to_location": "loc3", "product_id": "prod2", "qty": 15},
        {"timestamp": datetime(2023, 4, 5), "from_location": "loc3", "to_location": None, "product_id": "prod2", "qty": 5},
        {"timestamp": datetime(2023, 4, 10), "from_location": None, "to_location": "loc1", "product_id": "prod4", "qty": 10},
        {"timestamp": datetime(2023, 4, 12), "from_location": "loc1", "to_location": "loc2", "product_id": "prod4", "qty": 5},
        {"timestamp": datetime(2023, 4, 15), "from_location": "loc2", "to_location": None, "product_id": "prod3", "qty": 10},
        {"timestamp": datetime(2023, 4, 20), "from_location": "loc2", "to_location": None, "product_id": "prod1", "qty": 1}
    ]
    movements_collection.insert_many(movements)
    print(f"{len(movements)} movements inserted.")

    print("\nDatabase setup complete!")

if __name__ == '__main__':
    setup_database()
