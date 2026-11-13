
from sqlalchemy import select
from app.database.orm import ArticuloConocimientoDB


class ArticuloRepository:

    def __init__(self, session):
        self.session = session

    def crear(self, articulo):
        self.session.add(articulo)
        self.session.flush()
        return articulo

    def buscar_por_titulo(self, titulo):
        consulta = select(ArticuloConocimientoDB).where(
            ArticuloConocimientoDB.titulo.ilike(
                f"%{titulo}%"
            )
        )

        return self.session.scalars(consulta).all()

    def obtener_por_id(self, articulo_id):
        return self.session.get(
            ArticuloConocimientoDB,
            articulo_id
        )
