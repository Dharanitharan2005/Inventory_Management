from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import mongo
from datetime import datetime
from bson.objectid import ObjectId

movement_bp = Blueprint('movement_routes', __name__)

@movement_bp.route('/')
def movements():
    movements = mongo.db.movements.find().sort('timestamp', -1)
    return render_template('movements/list.html', movements=movements)

@movement_bp.route('/add', methods=['GET', 'POST'])
def add_movement():
    products = list(mongo.db.products.find())
    locations = list(mongo.db.locations.find())

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        qty_str = request.form.get('qty')

        if not product_id:
            flash('Product is required.', 'danger')
            return render_template('movements/add.html', products=products, locations=locations, form_data=request.form)

        if not from_location and not to_location:
            flash('A movement must have a from or to location.', 'danger')
            return render_template('movements/add.html', products=products, locations=locations, form_data=request.form)

        if from_location and to_location and from_location == to_location:
            flash('From and To locations cannot be the same.', 'danger')
            return render_template('movements/add.html', products=products, locations=locations, form_data=request.form)

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            flash('Quantity must be a positive integer.', 'danger')
            return render_template('movements/add.html', products=products, locations=locations, form_data=request.form)

        movement_data = {
            'product_id': product_id,
            'from_location': from_location if from_location else None,
            'to_location': to_location if to_location else None,
            'qty': qty,
            'timestamp': datetime.utcnow()
        }
        mongo.db.movements.insert_one(movement_data)
        flash('Movement added successfully!', 'success')
        return redirect(url_for('movement_routes.movements'))
    
    return render_template('movements/add.html', products=products, locations=locations)

@movement_bp.route('/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = mongo.db.movements.find_one_or_404({'_id': ObjectId(movement_id)})
    products = list(mongo.db.products.find())
    locations = list(mongo.db.locations.find())

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        qty_str = request.form.get('qty')

        # Create a mutable copy of the movement to update on error
        form_data = movement.copy()
        form_data.update(request.form)

        if not product_id:
            flash('Product is required.', 'danger')
            return render_template('movements/edit.html', movement=form_data, products=products, locations=locations)

        if not from_location and not to_location:
            flash('A movement must have a from or to location.', 'danger')
            return render_template('movements/edit.html', movement=form_data, products=products, locations=locations)

        if from_location and to_location and from_location == to_location:
            flash('From and To locations cannot be the same.', 'danger')
            return render_template('movements/edit.html', movement=form_data, products=products, locations=locations)

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            flash('Quantity must be a positive integer.', 'danger')
            return render_template('movements/edit.html', movement=form_data, products=products, locations=locations)

        updated_data = {
            'product_id': product_id,
            'from_location': from_location if from_location else None,
            'to_location': to_location if to_location else None,
            'qty': qty,
            'timestamp': datetime.utcnow()
        }
        mongo.db.movements.update_one({'_id': ObjectId(movement_id)}, {'$set': updated_data})
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('movement_routes.movements'))
    
    return render_template('movements/edit.html', movement=movement, products=products, locations=locations)

@movement_bp.route('/delete/<movement_id>', methods=['POST'])
def delete_movement(movement_id):
    mongo.db.movements.delete_one({'_id': ObjectId(movement_id)})
    flash('Movement deleted successfully!', 'success')
    return redirect(url_for('movement_routes.movements'))
