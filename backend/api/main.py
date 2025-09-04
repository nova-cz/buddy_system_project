from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.core.buddy_system import BuddySystem
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
buddy_system = None

class InitRequest(BaseModel):
    total_size: int
    unit: str = 'MB'

class AddProcessRequest(BaseModel):
    process_id: str
    process_size: int
    unit: str = 'MB'

class RemoveProcessRequest(BaseModel):
    process_id: str

@app.post("/init")
def init_memory(req: InitRequest):
    global buddy_system
    # Convertir a KB para manejo interno
    size_kb = req.total_size * 1024 if req.unit == 'MB' else req.total_size
    buddy_system = BuddySystem(size_kb)
    return {"status": "initialized"}

@app.post("/add_process")
def add_process(req: AddProcessRequest):
    if buddy_system is None:
        raise HTTPException(status_code=400, detail="Memory not initialized")
    # Convertir a KB para manejo interno
    size_kb = req.process_size * 1024 if req.unit == 'MB' else req.process_size
    ok, _ = buddy_system.allocate(req.process_id, size_kb)
    if not ok:
        # Mensaje más claro según la causa
        if buddy_system._process_exists(req.process_id):
            raise HTTPException(status_code=400, detail="Ya existe un proceso con ese nombre")
        if size_kb > buddy_system.total_size:
            raise HTTPException(status_code=400, detail="El proceso excede la memoria total disponible")
        raise HTTPException(
            status_code=400,
            detail="No se pudo asignar memoria al proceso. Puede que haya suficiente memoria libre en total, pero está fragmentada en bloques más pequeños que el tamaño solicitado. El Buddy System solo puede asignar procesos en bloques contiguos y del tamaño adecuado."
        )
    return {"status": "allocated"}

@app.post("/remove_process")
def remove_process(req: RemoveProcessRequest):
    if buddy_system is None:
        raise HTTPException(status_code=400, detail="Memory not initialized")
    success = buddy_system.deallocate(req.process_id)
    if not success:
        raise HTTPException(status_code=400, detail="Deallocation failed")
    return {"status": "deallocated"}

@app.get("/tree")
def get_tree():
    if buddy_system is None:
        raise HTTPException(status_code=400, detail="Memory not initialized")
    return buddy_system.get_tree()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Solo permite el frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)