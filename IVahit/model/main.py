from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from . import Base, Note, Tag


def test_main():
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        note = Note(note="Hallo Notiz!")
        tag1 = Tag(note=note, tag="RED")
        tag2 = Tag(note=note, tag="HOT")
        session.add_all([note, tag1, tag2])
        session.commit()
