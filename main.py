from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

# Modelo de datos para la reserva
class Reserva(BaseModel):
    cliente: str
    telefono: str
    fecha: str
    personas: int
    estado: str = "Pendiente" # Pendiente, Pagado, Cancelado
    metodo_pago: str = "N/A"

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
