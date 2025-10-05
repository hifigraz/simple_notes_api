import re

from IVahit.crud import Crud
from IVahit.engines import get_test_engine
from IVahit.mylog import getLogger

logger = getLogger(__name__)


def strip_uuid(in_str: str) -> str:
    return re.sub(
        r"UUID\('[0-9,a-z,-]+'\)",
        "UUID('00000000-0000-0000-0000-000000000000')",
        str(in_str),
    )


def test_00():
    engine = get_test_engine()
    crud = Crud(engine)
    note_a_create = crud.CreateNote(note="Test A")
    logger.debug(repr(note_a_create))
    logger.debug(str(strip_uuid(repr(note_a_create))))
    assert (
        strip_uuid(repr(note_a_create))
        == "FullNoteDef(note='Test A', id=UUID('00000000-0000-0000-0000-000000000000'), tags=[])"
    )

    note_a_read = crud.ReadNote()[0]
    assert (
        repr(note_a_read)
        == f"FullNoteDef(note='Test A', id=UUID('{note_a_create.id}'), tags=[])"
    )

    note_b_create = crud.CreateNote(note="Test B", tags=["RED", "GREEN"])
    assert (
        strip_uuid(repr(note_b_create))
        == "FullNoteDef(note='Test B', id=UUID('00000000-0000-0000-0000-000000000000'), tags=[FullTagDef(tag='RED', id=UUID('00000000-0000-0000-0000-000000000000'), note_id=UUID('00000000-0000-0000-0000-000000000000')), FullTagDef(tag='GREEN', id=UUID('00000000-0000-0000-0000-000000000000'), note_id=UUID('00000000-0000-0000-0000-000000000000'))])"
    )
    assert note_a_create == note_a_read

    note_b_read = crud.ReadNote(id=note_b_create.id)
    assert note_b_create == note_b_read[0]
    assert repr(note_b_create) == repr(note_b_read[0])
