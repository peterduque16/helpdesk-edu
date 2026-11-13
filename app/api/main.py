
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

app = FastAPI(
    title="Helpdesk EDU API",
    description="API del sistema de soporte técnico",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Helpdesk EDU",
        "estado": "API funcionando correctamente"
    }

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencias import obtener_sesion
from app.database.orm import ArticuloConocimientoDB

class ArticuloCrear(BaseModel):
    id: str
    ticket_id: str
    titulo: str
    solucion: str
@app.get("/articulos")
def listar_articulos(
    session: Session = Depends(obtener_sesion)
):
    consulta = select(ArticuloConocimientoDB)
    articulos = session.scalars(consulta).all()

    return [
        {
            "id": articulo.id,
            "ticket_id": articulo.ticket_id,
            "titulo": articulo.titulo,
            "solucion": articulo.solucion
        }
        for articulo in articulos
    ]

@app.get("/articulos/{articulo_id}")
def obtener_articulo(
    articulo_id: str,
    session: Session = Depends(obtener_sesion)
):
    articulo = session.get(
        ArticuloConocimientoDB,
        articulo_id
    )

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Artículo no encontrado"
        )

    return {
        "id": articulo.id,
        "ticket_id": articulo.ticket_id,
        "titulo": articulo.titulo,
        "solucion": articulo.solucion
    }
class ArticuloActualizar(BaseModel):
    titulo: str
    solucion: str

@app.post("/articulos", status_code=201)
def crear_articulo(
    datos: ArticuloCrear,
    session: Session = Depends(obtener_sesion)
):
    existente = session.get(
        ArticuloConocimientoDB,
        datos.id
    )

    if existente is not None:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un artículo con ese ID"
        )

    articulo = ArticuloConocimientoDB(
        id=datos.id,
        ticket_id=datos.ticket_id,
        titulo=datos.titulo,
        solucion=datos.solucion
    )

    session.add(articulo)

    try:
        session.commit()
        session.refresh(articulo)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto al guardar el artículo"
        )

    return {
        "id": articulo.id,
        "ticket_id": articulo.ticket_id,
        "titulo": articulo.titulo,
        "solucion": articulo.solucion
    }
@app.put("/articulos/{articulo_id}")
def actualizar_articulo(
    articulo_id: str,
    datos: ArticuloActualizar,
    session: Session = Depends(obtener_sesion)
):
    articulo = session.get(
        ArticuloConocimientoDB,
        articulo_id
    )

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Artículo no encontrado"
        )

    articulo.titulo = datos.titulo
    articulo.solucion = datos.solucion

    session.commit()
    session.refresh(articulo)

    return {
        "id": articulo.id,
        "ticket_id": articulo.ticket_id,
        "titulo": articulo.titulo,
        "solucion": articulo.solucion
    }

@app.delete("/articulos/{articulo_id}")
def eliminar_articulo(
    articulo_id: str,
    session: Session = Depends(obtener_sesion)
):
    articulo = session.get(
        ArticuloConocimientoDB,
        articulo_id
    )

    if articulo is None:
        raise HTTPException(
            status_code=404,
            detail="Artículo no encontrado"
        )

    session.delete(articulo)
    session.commit()

    return {
        "mensaje": "Artículo eliminado correctamente",
        "id": articulo_id
    }
