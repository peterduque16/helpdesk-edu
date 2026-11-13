
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TicketDB(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    requester_id: Mapped[str] = mapped_column(String(50))
    estado: Mapped[str] = mapped_column(String(20), default="abierto")

    articulos: Mapped[list["ArticuloConocimientoDB"]] = relationship(
        back_populates="ticket"
    )


class ArticuloConocimientoDB(Base):
    __tablename__ = "articulos_conocimiento"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)

    ticket_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("tickets.id"),
        nullable=False
    )

    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    solucion: Mapped[str] = mapped_column(String(2000), nullable=False)

    ticket: Mapped["TicketDB"] = relationship(
        back_populates="articulos"
    )
