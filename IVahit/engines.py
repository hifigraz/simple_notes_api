from sqlalchemy import Engine, create_engine

from IVahit.model import Base


def _get_test_engine(url: str) -> Engine:
    engine = create_engine(url, echo=False)
    Base.metadata.create_all(engine)
    return engine


def get_test_engine() -> Engine:
    return _get_test_engine("sqlite://")


def get_prod_endinge() -> Engine:
    return _get_test_engine("postgresql://notes:Kennwort1@postgres:5432/notes")


__all__ = ["get_test_engine", "get_prod_endinge"]
