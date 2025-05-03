from datetime import datetime, timezone
from typing import List
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class SignalType(Base):
    __tablename__ = "tipo_sinal"

    id:                 Mapped[int] = mapped_column(Integer, primary_key=True)
    name:               Mapped[str] = mapped_column(String, nullable=False)
    signals:            Mapped[List['Signal']] = relationship()
    
class Signal(Base):
    __tablename__ = "sinal"

    id:                 Mapped[int] = mapped_column(Integer, primary_key=True)
    data:               Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    timestamp:          Mapped[float] = mapped_column(Float)
    value:              Mapped[float] = mapped_column(Float)
    signal_id:          Mapped[int] = mapped_column(ForeignKey("tipo_sinal.id"))
    

