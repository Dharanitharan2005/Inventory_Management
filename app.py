from flask import Flask, render_template
from config import Config
from extensions import mongo

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)

    # Register blueprints
    from routes.product_routes import product_bp
    from routes.location_routes import location_bp
    from routes.movement_routes import movement_bp
    from routes.report_routes import report_bp

    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(location_bp, url_prefix='/locations')
    app.register_blueprint(movement_bp, url_prefix='/movements')
    app.register_blueprint(report_bp, url_prefix='/reports')

    # Register a simple index route
    @app.route('/')
    def index():
        # --- Dashboard Stats ---
        total_products = mongo.db.products.count_documents({})
        total_locations = mongo.db.locations.count_documents({})

        # --- Recent Movements (with product and location names) ---
        recent_movements_pipeline = [
            {'$sort': {'timestamp': -1}},
            {'$limit': 5},
            {
                '$lookup': {
                    'from': 'products',
                    'localField': 'product_id',
                    'foreignField': '_id',
                    'as': 'product_info'
                }
            },
            {
                '$lookup': {
                    'from': 'locations',
                    'localField': 'from_location',
                    'foreignField': '_id',
                    'as': 'from_loc_info'
                }
            },
            {
                '$lookup': {
                    'from': 'locations',
                    'localField': 'to_location',
                    'foreignField': '_id',
                    'as': 'to_loc_info'
                }
            },
            {'$unwind': {'path': '$product_info', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$from_loc_info', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$to_loc_info', 'preserveNullAndEmptyArrays': True}},
            {
                '$project': {
                    'product_name': '$product_info.product_name',
                    'from_location_name': '$from_loc_info.location_name',
                    'to_location_name': '$to_loc_info.location_name',
                    'qty': '$qty',
                    'timestamp': '$timestamp'
                }
            }
        ]
        recent_movements = list(mongo.db.movements.aggregate(recent_movements_pipeline))

        # --- Low Stock Report --- 
        balance_pipeline = [
            {
                '$facet': {
                    'inbound': [
                        {'$match': {'to_location': {'$ne': None}}},
                        {'$group': {
                            '_id': {'product': '$product_id', 'location': '$to_location'},
                            'total_in': {'$sum': '$qty'}
                        }}
                    ],
                    'outbound': [
                        {'$match': {'from_location': {'$ne': None}}},
                        {'$group': {
                            '_id': {'product': '$product_id', 'location': '$from_location'},
                            'total_out': {'$sum': '$qty'}
                        }}
                    ]
                }
            },
            {
                '$project': {
                    'all_movements': {
                        '$concatArrays': ['$inbound', '$outbound']
                    }
                }
            },
            {'$unwind': '$all_movements'},
            {
                '$group': {
                    '_id': '$all_movements._id',
                    'total_in': {'$sum': {'$ifNull': ['$all_movements.total_in', 0]}},
                    'total_out': {'$sum': {'$ifNull': ['$all_movements.total_out', 0]}}
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'balance': {'$subtract': ['$total_in', '$total_out']}
                }
            },
            {'$match': {'balance': {'$lt': 10}}},
            {
                '$lookup': {
                    'from': 'products',
                    'localField': '_id.product',
                    'foreignField': '_id',
                    'as': 'product_info'
                }
            },
            {
                '$lookup': {
                    'from': 'locations',
                    'localField': '_id.location',
                    'foreignField': '_id',
                    'as': 'location_info'
                }
            },
            {'$unwind': '$product_info'},
            {'$unwind': '$location_info'},
            {
                '$project': {
                    'product_name': '$product_info.product_name',
                    'location_name': '$location_info.location_name',
                    'quantity': '$balance',
                    '_id': 0
                }
            }
        ]
        low_stock_items = list(mongo.db.movements.aggregate(balance_pipeline))

        return render_template(
            'index.html', 
            total_products=total_products, 
            total_locations=total_locations,
            recent_movements=recent_movements,
            low_stock_items=low_stock_items
        )

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
