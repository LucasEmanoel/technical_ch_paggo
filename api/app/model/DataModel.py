from datetime import datetime
from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = "data"

    id:                 Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp:          Mapped[datetime] = mapped_column(DateTime, default=datetime.now(datetime.timezone.utc))
    wind_spped:         Mapped[float] = mapped_column(Float)
    power:              Mapped[float] = mapped_column(Float)
    ambient_temprature: Mapped[float] = mapped_column(Float)
    
    
