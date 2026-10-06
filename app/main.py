from fastapi import FastAPI
from pydantic import BaseModel

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


@app.get("/")
def inicio():
    return {"mensaje": "API de incidencias operativa"}


@app.get("/incidencias", response_model=list[Incidencia])
def listar_incidencias():
    return incidencias

class IncidenciaCrear(BaseModel):
    titulo: str
    descripcion: str
    estado: str = "abierta"
    prioridad: str
    tecnico: str


@app.post("/incidencias", response_model=Incidencia, status_code=201)
def crear_incidencia(datos: IncidenciaCrear):
    nuevo_id = max((i.id for i in incidencias), default=0) + 1
    nueva = Incidencia(id=nuevo_id, **datos.model_dump())
    incidencias.append(nueva)
    return nueva