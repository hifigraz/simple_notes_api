from typing import override
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__: str = "note"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    note: Mapped[str] = mapped_column(String(1000))
    tags: Mapped[list["Tag"]] = relationship(back_populates="note")

    @override
    def __repr__(self) -> str:
        return f"Note(id={self.id!r} note={self.note!r})"


class Tag(Base):
    __tablename__: str = "tag"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    note_id: Mapped[UUID] = mapped_column(ForeignKey("note.id"))
    note: Mapped["Note"] = relationship(back_populates="tags")
    tag: Mapped[str] = mapped_column(String(30))

    @override
    def __repr__(self) -> str:
        return f"Tag(id={self.id!r} note_id={self.note_id!r} note={self.note.note!r} tag={self.tag!r})"
