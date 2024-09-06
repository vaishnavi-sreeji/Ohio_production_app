from flask import Blueprint, request, jsonify
from app.db import get_annual_data

#Creating blueprint
api_create = Blueprint('api_create', __name__)

#This function gets the well data
@api_create .route('/data', methods=['GET'])
def get_data():
    well_number = request.args.get('well')
    if not well_number:
        return jsonify({"error": "Well number is required"}), 400
    
    data = get_annual_data(well_number)
    print("data",data)
    if data:
        # print("jsonified data",jsonify(data))
        return jsonify(data)
    else:
        return jsonify({"error": "Well number not found"}), 404
    
    
@api_create .route('/', methods=['GET'])
def test():
    return "Welcome to Ohio Production Application"





