from model.participants import Participants
from core.Database import SessionLocal


class ParticipantService:
    def __init__(self):
        self.db = SessionLocal()

    def create_participant(self, name, code_room):
        participant = Participants(name=name, code_room=code_room)
        self.db.add(participant)
        self.db.commit()
        self.db.close()
        return participant
