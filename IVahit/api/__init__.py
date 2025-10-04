from uuid import UUID

from fastapi import FastAPI, HTTPException

from IVahit.crud import (CreateNoteDef, Crud, CrudElementNotFoundException,
                         FullNoteDef)
from IVahit.engines import get_prod_endinge

from ..mylog import getLogger

logger = getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get(path="/note/")
async def notes() -> list[FullNoteDef]:
    crud = Crud(get_prod_endinge())
    return crud.ReadNote()


@app.get(path="/note/{note_id}")
async def note_by_id(note_id: UUID) -> FullNoteDef:
    try:
        crud = Crud(get_prod_endinge())
        notes = crud.ReadNote(note_id)
        return notes[0]
    except CrudElementNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"No Note with id: {e.missing_id}")


@app.post(path="/note/")
async def create_note(note: CreateNoteDef) -> FullNoteDef:
    try:
        crud = Crud(get_prod_endinge())
        return crud.CreateNote(note.note, list(map(lambda x: x.tag, note.tags)))
    except Exception as e:
        logger.error(e)
        raise e

@app.put(path="/note/{note_id}")
async def update_note(note_id: UUID, note: CreateNoteDef):
    assert note_id
    assert note