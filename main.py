from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from STOUT import translate_forward
import uvicorn

app = FastAPI(title="STOUT IUPAC API")

class MoleculeRequest(BaseModel):
    smiles: str

@app.get("/")
def home():
    return {"status": "Active", "message": "STOUT is running on Cloud."}

@app.post("/get_iupac")
def generate_iupac(request: MoleculeRequest):
    smiles = request.smiles.strip()
    if not smiles:
        raise HTTPException(status_code=400, detail="SMILES is empty")
    
    try:
        iupac_name = translate_forward(smiles)
        if not iupac_name or "Could not" in iupac_name:
            raise HTTPException(status_code=400, detail="Invalid structure")
        return {"smiles": smiles, "iupac": iupac_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
