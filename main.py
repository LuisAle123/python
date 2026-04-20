from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# Asegúrate de que esto esté justo después de app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Esto permite que GitHub Pages se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para la reserva
class Reserva(BaseModel):
    cliente: str
    telefono: str
    fecha: str
    personas: int
    estado: str = "Pendiente" # Pendiente, Pagado, Cancelado
    metodo_pago: str # Ahora es obligatorio enviarlo desde la web

# Base de datos temporal en memoria (en producción usa PostgreSQL) [cite: 233]
db_reservas = []

@app.post("/reservar")
def crear_reserva(reserva: Reserva):
    db_reservas.append(reserva.dict())
    return {"status": "Reserva recibida exitosamente"}

@app.get("/lista_reservas")
def obtener_reservas():
    return db_reservas

@app.put("/pagar/{index}")
def procesar_pago(index: int, metodo: str):
    if 0 <= index < len(db_reservas):
        db_reservas[index]["estado"] = "Pagado"
        db_reservas[index]["metodo_pago"] = metodo
        return {"status": "Pago registrado"}
    return {"error": "Reserva no encontrada"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
