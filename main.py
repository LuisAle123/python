from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Reserva(BaseModel):
    cliente: str
    telefono: str
    fecha: str
    personas: int
    metodo_pago: str
    estado: str
    total_estimado: float # Nuevo campo para capturar la suma de la web

db_reservas = []

@app.post("/reservar")
def crear_reserva(reserva: Reserva):
    db_reservas.append(reserva.dict())
    return {"status": "Reserva enviada"}

@app.get("/lista_reservas")
def obtener_reservas():
    return db_reservas

@app.put("/pagar/{index}")
def procesar_pago(index: int, metodo: str):
    if 0 <= index < len(db_reservas):
        db_reservas[index]["estado"] = "Pagado/Confirmado"
        db_reservas[index]["metodo_pago"] = metodo
        return {"status": "Actualizado"}
    return {"error": "No encontrado"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
