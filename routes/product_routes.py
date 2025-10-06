from flask import Blueprint, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from extensions import mongo

product_bp = Blueprint('product_routes', __name__)

@product_bp.route('/')
def products():
    # Use aggregation to join products with locations
    pipeline = [
        {
            '$lookup': {
                'from': 'locations',
                'localField': 'location_id',
                'foreignField': '_id',
                'as': 'location_info'
            }
        },
        {
            '$unwind': {
                'path': '$location_info',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$project': {
                '_id': 1,
                'product_name': 1,
                'description': 1,
                'location_id': 1,
                'location_name': '$location_info.location_name'
            }
        }
    ]
    products = list(mongo.db.products.aggregate(pipeline))
    return render_template('products/list.html', products=products)

@product_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    locations = list(mongo.db.locations.find())
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        location_id = request.form.get('location_id')

        if not product_id or not product_name:
            flash('Product ID and Product Name are required.', 'danger')
            return render_template('products/add.html', form_data=request.form, locations=locations)

        if mongo.db.products.find_one({'_id': product_id}):
            flash('Product ID already exists.', 'danger')
            return render_template('products/add.html', form_data=request.form, locations=locations)

        product_data = {
            '_id': product_id,
            'product_name': product_name,
            'description': request.form.get('description'),
            'location_id': location_id if location_id else None
        }
        mongo.db.products.insert_one(product_data)
        flash('Product added successfully!', 'success')
        return redirect(url_for('product_routes.products'))
    return render_template('products/add.html', locations=locations)

@product_bp.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = mongo.db.products.find_one_or_404({'_id': product_id})
    locations = list(mongo.db.locations.find())
    
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        location_id = request.form.get('location_id')
        
        if not product_name:
            flash('Product Name is required.', 'danger')
            product['product_name'] = request.form.get('product_name', product['product_name'])
            product['description'] = request.form.get('description', product['description'])
            product['location_id'] = request.form.get('location_id', product.get('location_id'))
            return render_template('products/edit.html', product=product, locations=locations)

        updated_data = {
            'product_name': product_name,
            'description': request.form.get('description'),
            'location_id': location_id if location_id else None
        }
        mongo.db.products.update_one({'_id': product_id}, {'$set': updated_data})
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product_routes.products'))
    return render_template('products/edit.html', product=product, locations=locations)

@product_bp.route('/delete/<product_id>', methods=['POST'])
def delete_product(product_id):
    # Check if the product is used in any movements
    if mongo.db.movements.find_one({'product_id': product_id}):
        flash('Cannot delete product as it is used in movements.', 'danger')
        return redirect(url_for('product_routes.products'))

    mongo.db.products.delete_one({'_id': product_id})
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product_routes.products'))
