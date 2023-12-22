from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random, os
from string import ascii_uppercase
from dotenv import load_dotenv

from controller.accounts import account_blueprint
from service.message import MessageService
from service.participants import ParticipantService
from service.rooms import RoomService

load_dotenv()

app = Flask(__name__)
app.register_blueprint(account_blueprint)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

room_service = RoomService()
message_service = MessageService()
participant_service = ParticipantService()
rooms = message_service.list_room_with_message()


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


@app.route("/home", methods=["POST", "GET"])
def home():
    list_room = room_service.list_rooms(session.get("name"))
    if request.method == "POST":
        name = session.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        join_exist = request.form.get("join-exist", False)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name, rooms=list_room)

        room = code
        if create != False:
            room = generate_unique_code(4)
            room_service.create_room(room)
            rooms[room] = {"messages": []}
            print(rooms)
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name, rooms=list_room)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html", rooms=list_room)


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    message_service.create_message(code_room=session.get("room"), content=data["data"], name=session.get("name"))
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    participant_service.create_participant(name=name, code_room=room)
    send({"name": name, "message": "has entered the room"}, to=room)
    print(f"{name} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app, debug=True)
