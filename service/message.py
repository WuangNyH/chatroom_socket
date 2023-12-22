from model.message import Message
from core.Database import SessionLocal
from model.rooms import Room


class MessageService:
    def __init__(self):
        self.db = SessionLocal()

    def create_message(self, code_room, content, name):
        new_message = Message(code_room=code_room, content=content, name=name)
        self.db.add(new_message)
        self.db.commit()
        self.db.close()
        return new_message

    def get_message(self, code_room):
        result = self.db.query(Message).filter_by(code_room=code_room).all()
        list_content = []
        for message in result:
            content = {
                "name": message.name,
                "message": message.content
            }
            list_content.append(content)
        return list_content

    def list_room_with_message(self):
        code_rooms = self.db.query(Room.code_room).all()
        list_code = [code_room for (code_room,) in code_rooms]
        rooms = {}
        for code_room in list_code:
            rooms[code_room] = {"messages": self.get_message(code_room)}

        return rooms
