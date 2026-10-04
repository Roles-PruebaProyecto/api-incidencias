from fastapi import FastAPI

app = FastAPI(title="API de incidencias")


@app.get("/")
def inicio():
    return {"mensaje": "API de incidencias operativa"}