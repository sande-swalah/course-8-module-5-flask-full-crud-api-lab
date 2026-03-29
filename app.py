from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


def next_event_id():
    return max((event.id for event in events), default=0) + 1


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_title_from_request():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, error_response("Request body must be a JSON object", 400)

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return None, error_response("Title is required", 400)

    return title.strip(), None


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Event API"}), 200


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


@app.route("/events", methods=["POST"])
def create_event():
    title, error = parse_title_from_request()
    if error:
        return error

    new_event = Event(next_event_id(), title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return error_response("Event not found", 404)

    title, error = parse_title_from_request()
    if error:
        return error

    event.title = title
    return jsonify(event.to_dict()), 200


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return error_response("Event not found", 404)

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
