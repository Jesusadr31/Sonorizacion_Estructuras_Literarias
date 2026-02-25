from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
import csv
import os

app = FastAPI()

# Modelo para validar email
class UserEmail(BaseModel):
    email: EmailStr

# Montar carpeta estática para servir frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

# Ruta para servir la página principal
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Endpoint para registrar email
@app.post("/register")
async def register_email(user: UserEmail):
    file_exists = os.path.isfile('usuarios.csv')
    try:
        with open('usuarios.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['email'])  # encabezado si no existe archivo
            writer.writerow([user.email])
        return {"message": "Correo registrado correctamente"}
    except Exception:
        raise HTTPException(status_code=500, detail="Error al guardar el correo")