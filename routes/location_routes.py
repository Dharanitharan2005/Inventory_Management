from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import mongo

location_bp = Blueprint('location_routes', __name__)

@location_bp.route('/')
def locations():
    locations = mongo.db.locations.find()
    return render_template('locations/list.html', locations=locations)

@location_bp.route('/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form.get('location_id')
        location_name = request.form.get('location_name')

        if not location_id or not location_name:
            flash('Location ID and Location Name are required.', 'danger')
            return render_template('locations/add.html', form_data=request.form)

        if mongo.db.locations.find_one({'_id': location_id}):
            flash('Location ID already exists.', 'danger')
            return render_template('locations/add.html', form_data=request.form)

        location_data = {
            '_id': location_id,
            'location_name': location_name
        }
        mongo.db.locations.insert_one(location_data)
        flash('Location added successfully!', 'success')
        return redirect(url_for('location_routes.locations'))
    return render_template('locations/add.html')

@location_bp.route('/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = mongo.db.locations.find_one_or_404({'_id': location_id})
    if request.method == 'POST':
        location_name = request.form.get('location_name')
        if not location_name:
            flash('Location Name is required.', 'danger')
            # Pass the invalid submission back to the template
            location['location_name'] = request.form.get('location_name', location['location_name'])
            return render_template('locations/edit.html', location=location)

        updated_data = {
            'location_name': location_name
        }
        mongo.db.locations.update_one({'_id': location_id}, {'$set': updated_data})
        flash('Location updated successfully!', 'success')
        return redirect(url_for('location_routes.locations'))
    return render_template('locations/edit.html', location=location)

@location_bp.route('/delete/<location_id>', methods=['POST'])
def delete_location(location_id):
    # Check if location is in use by any movements
    if mongo.db.movements.find_one({'$or': [{'from_location': location_id}, {'to_location': location_id}]}):
        flash('Cannot delete location as it is used in movements.', 'danger')
        return redirect(url_for('location_routes.locations'))
    
    mongo.db.locations.delete_one({'_id': location_id})
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('location_routes.locations'))
