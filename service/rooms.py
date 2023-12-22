from model.rooms import Room
from model.participants import Participants
from core.Database import SessionLocal


class RoomService:
    def __init__(self):
        self.db = SessionLocal()

    def create_room(self, code_room):
        new_room = Room(code_room=code_room)
        self.db.add(new_room)
        self.db.commit()
        self.db.close()
        return new_room

    def list_rooms(self, name):
        result = self.db.query(Room.id, Room.code_room).join(Participants, Room.code_room == Participants.code_room).filter(Participants.name == name).group_by(Room.code_room).all()
        return result
