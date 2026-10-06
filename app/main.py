import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

app = FastAPI(title="API de incidencias")


class Incidencia(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    tecnico: str


incidencias: list[Incidencia] = [
    Incidencia(
        id=1,
        titulo="No arranca el ordenador 12",
        descripcion="El equipo no muestra imagen",
        estado="abierta",
        prioridad="alta",
        tecnico="Ana",
    )
]

class IncidenciaActualizar(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    tecnico: str

class IncidenciaCrear(BaseModel):
    titulo: str
    descripcion: str
    estado: str = "abierta"
    prioridad: str
    tecnico: str

@app.get("/")
def inicio():
    return {"mensaje": "API de incidencias operativa"}


@app.get("/incidencias", response_model=list[Incidencia])
def listar_incidencias():
    return incidencias

@app.put("/incidencias/{id}", response_model=Incidencia)
def modificar_incidencia(id: int, datos: IncidenciaActualizar):
    for posicion, incidencia in enumerate(incidencias):
        if incidencia.id == id:
            actualizada = Incidencia(id=id, **datos.model_dump())
            incidencias[posicion] = actualizada
            return actualizada
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")


@app.delete("/incidencias/{id}")
def eliminar_incidencia(id: int, x_admin_token: str | None = Header(default=None)):
    if not ADMIN_TOKEN:
        raise HTTPException(status_code=500, detail="ADMIN_TOKEN no configurado en el entorno")
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Token de administrador no válido")
    for posicion, incidencia in enumerate(incidencias):
        if incidencia.id == id:
            incidencias.pop(posicion)
            return {"mensaje": f"Incidencia {id} eliminada"}
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")

@app.get("/incidencias/{id}", response_model=Incidencia)
def obtener_incidencia(id: int):
    for incidencia in incidencias:
        if incidencia.id == id:
            return incidencia
    raise HTTPException(status_code=404, detail=f"No existe la incidencia con id {id}")

@app.post("/incidencias", response_model=Incidencia, status_code=201)
def crear_incidencia(datos: IncidenciaCrear):
    nuevo_id = max((i.id for i in incidencias), default=0) + 1
    nueva = Incidencia(id=nuevo_id, **datos.model_dump())
    incidencias.append(nueva)
    return nueva