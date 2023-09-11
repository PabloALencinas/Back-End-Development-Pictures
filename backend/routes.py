from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture is None:
        abort(404)  # Return a 404 Not Found error if the picture is not found
    
    return jsonify(picture)

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture(id):
    # Check if the request data is in JSON format
    if not request.json:
        abort(400)  # Bad Request if the request data is not in JSON format

    new_picture = request.json  # Get the JSON data from the request

    # Check if a picture with the same ID already exists
    existing_picture = next((item for item in data if item["id"] == id), None)
    if existing_picture:
        return jsonify({"Message": f"Picture with id {id} already present"}), 302  # Found status code

    # Assign the provided ID to the new picture
    new_picture["id"] = id

    # Append the new picture to the data list
    data.append(new_picture)

    # Save the updated data back to the JSON file (optional)
    with open(json_url, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Return the newly created picture as JSON with a 201 Created status code
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Find the picture with the specified ID
    picture_to_update = next((item for item in data if item["id"] == id), None)

    # If the picture with the given ID doesn't exist, return a 404 error
    if picture_to_update is None:
        abort(404)

    # Get the updated data from the request
    updated_data = request.json

    # Update the fields of the picture with the new data
    for key, value in updated_data.items():
        picture_to_update[key] = value

    # Save the updated data back to the JSON file (optional)
    with open(json_url, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Return the updated picture as JSON
    return jsonify(picture_to_update)


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture with the specified ID
    picture_to_delete = next((item for item in data if item["id"] == id), None)

    # If the picture with the given ID doesn't exist, return a 404 error
    if picture_to_delete is None:
        abort(404)

    # Remove the picture from the data list
    data.remove(picture_to_delete)

    # Save the updated data back to the JSON file (optional)
    with open(json_url, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Return a response with a status of HTTP_204_NO_CONTENT (empty body)
    return make_response("", 204)