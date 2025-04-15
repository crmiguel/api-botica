
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica ["http://127.0.0.1:5500"] si prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Config
SUPABASE_URL = "https://jvhbaqjfhakieczxlcmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp2aGJhcWpmaGFraWVjenhsY212Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2OTczMjQsImV4cCI6MjA2MDI3MzMyNH0.4IFF706s_CGFRNsq73LCA2GFCpnPVJjKJSMCXaFnoSA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Modelo de Producto
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

# Rutas API

@app.get("/")
def root():
    return {"mensaje": "API Botica funcionando"}

@app.get("/productos")
def listar_productos():
    try:
        response = supabase.table("productos").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

@app.post("/productos")
def agregar_producto(producto: Producto):
    try:
        response = supabase.table("productos").insert(producto.dict()).execute()
        return {"mensaje": "Producto agregado", "data": response.data}
    except Exception as e:
        return {"error": str(e)}

@app.put("/productos/{id}")
def editar_producto(id: int, producto: Producto):
    try:
        response = supabase.table("productos").update(producto.dict()).eq("id", id).execute()
        return {"mensaje": "Producto actualizado", "data": response.data}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    try:
        response = supabase.table("productos").delete().eq("id", id).execute()
        return {"mensaje": "Producto eliminado", "data": response.data}
    except Exception as e:
        return {"error": str(e)}
