from sqlmodel import create_engine

from src.core.settings import settings

engine = create_engine(url=settings.POSTGRES_URL)  # type: ignore[arg-type]
