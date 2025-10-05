from sys import argv
from time import sleep

from sqlalchemy import Engine
from sqlalchemy.sql import text

from IVahit.api import app
from IVahit.crud import Crud
from IVahit.engines import get_prod_endinge, get_test_engine
from IVahit.model._model import Base

from .mylog import getLogger

assert app

logger = getLogger(__name__)


def clear_database():
    logger.critical("WARNING !! Clearing database")
    logger.critical("")
    logger.critical("Waiting 10 seconds. Interrupt with CTR-C if not intended")
    sleep(10)

    engine = get_prod_endinge()
    with engine.connect() as con:
        statement = text(
            "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE  table_type = 'BASE TABLE' AND table_schema = 'public'"
        )
        for i in con.execute(statement):
            logger.info(i)
            statement_str: str = f"DROP  TABLE {i[0]} CASCADE"
            statement = text(statement_str)
            logger.info(statement)
            try:
                logger.debug(con.execute(statement))
            except Exception as e:
                logger.error("Very dirty please FIXX ME: %s", e)
        con.commit()

    logger.debug(f"Engine: {engine}")


def create_database():
    logger.debug("Creating Database")
    engine = get_prod_endinge()
    Base.metadata.create_all(engine)


def test_crud():
    logger.info(argv)
    logger.info(len(argv))
    engine: None | Engine = None
    if len(argv) > 1 and argv[1] == "prod":
        logger.info("On PROD")
        engine = get_prod_endinge()
    else:
        logger.info("in Memory")
        engine = get_test_engine()
    crud = Crud(engine)
    logger.debug(engine)

    _ = crud.CreateNote("Das ist die Notiz")
    _ = crud.CreateNote("Und noch eine schöne Notiz")
    notes = crud.ReadNote()
    logger.debug(list(notes))
