from flask import Flask, request, jsonify, render_template
from DataWrapper import DataWrapper

from functools import wraps
import time


app = Flask(__name__)

db_file = 'Data.db'
wrapper = DataWrapper(db_file)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/note")
def note():
    note_id = request.args.get('noteid')
    if not note_id:
        return jsonify({"error": "Note ID is missing"}), 400

    return render_template("note.html", note_id=note_id)




@app.route("/api/note")
def get_note():
    note_id = request.args.get('noteid')
    if not note_id:
        return jsonify({"error": "Note ID is missing"}), 400

    data = wrapper.query_by_id(note_id)
    if not data:
        return jsonify({"error": "Note not found"}), 404

    return jsonify(data)



@app.route("/api/add_note", methods=["POST", "GET"])
def add_note():
    if request.method == "POST":
        note_data = request.form.get('notedata')
        if not note_data:
            return jsonify({"error": "Note Data is missing"}), 400

        # Replace this with your actual data insertion logic
        note_id = wrapper.insert_data(note_data)
        if not note_id:
            return jsonify({"error": "Something went wrong during data insertion."}), 500

        return jsonify({"note_id": note_id})
    
    elif request.method == "PUT":
        note_data = request.args.get('notedata')
        if note_data:
            note_id = wrapper.insert_data(note_data)
            if not note_id:
                return jsonify({"error": "Something went wrong during data insertion."}), 500
            return jsonify({"note_id": note_id})
        else:
            return jsonify({"error": "Note Data is missing"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)





