"""
FastAPI Backend — Main application entry point.
Handles CSV upload, employee search, ML prediction, and chatbot.
"""

import io
import json
import os

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import init_db, store_dataset, search_employees, get_employee_by_id, get_dataset_employees, get_latest_dataset_id
from ml_engine import train_models, predict_employee, get_model_info
from chatbot import generate_advice, chat_response

app = FastAPI(title="9-Box Grid Prediction API", version="1.0.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


# ── Upload CSV ──────────────────────────────────────────────

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV dataset, store it, and train ML models."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded CSV is empty.")

    # Store in SQLite
    dataset_id = store_dataset(file.filename, df)

    # Train ML models
    try:
        model_info = train_models(df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to train models: {str(e)}")

    return {
        "message": "Dataset uploaded and models trained successfully!",
        "dataset_id": dataset_id,
        "total_employees": len(df),
        "columns": list(df.columns),
        "model_info": model_info,
    }


# ── Search Employees ────────────────────────────────────────

@app.get("/api/employees")
def search(q: str = Query("", min_length=0), dataset_id: int = Query(None)):
    """Search employees by name."""
    did = dataset_id or get_latest_dataset_id()
    if not did:
        raise HTTPException(status_code=404, detail="No dataset uploaded yet.")

    if q.strip() == "":
        # Return all employees for the dataset (limited)
        employees = get_dataset_employees(did)[:50]
    else:
        employees = search_employees(q, did)

    results = []
    for emp in employees:
        data = json.loads(emp["data_json"])
        results.append({
            "id": emp["id"],
            "name": emp["employee_name"],
            "data": data,
        })

    return {"employees": results, "count": len(results)}


# ── Predict Employee 9-Box Position ─────────────────────────

@app.get("/api/predict/{employee_id}")
def predict(employee_id: int):
    """Predict an employee's 9-box grid position."""
    emp = get_employee_by_id(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found.")

    try:
        result = predict_employee(emp["data_json"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "employee_id": employee_id,
        "employee_name": emp["employee_name"],
        "prediction": result,
    }


# ── Chatbot ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    employee_id: int
    message: str = ""
    grid_label: str = ""


@app.post("/api/chat")
def chat(req: ChatRequest):
    """Get chatbot advice for an employee."""
    emp = get_employee_by_id(req.employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found.")

    if not req.message:
        # Initial advice — predict first if no label provided
        if not req.grid_label:
            try:
                result = predict_employee(emp["data_json"])
                grid_label = result["label"]
                prediction_details = result
            except Exception:
                grid_label = "Core Player"
                prediction_details = {"performance": "Medium", "potential": "Medium", "model_used": "N/A"}
        else:
            grid_label = req.grid_label
            prediction_details = {"performance": "N/A", "potential": "N/A", "model_used": "N/A"}

        messages = generate_advice(grid_label, emp["employee_name"], prediction_details)
        return {"messages": messages, "grid_label": grid_label}
    else:
        # Follow-up conversation
        grid_label = req.grid_label or "Core Player"
        response = chat_response(req.message, grid_label, emp["employee_name"])
        return {
            "messages": [{"role": "assistant", "content": response}],
            "grid_label": grid_label,
        }


# ── Model Info ──────────────────────────────────────────────

@app.get("/api/model-info")
def model_info():
    """Get information about the trained models."""
    info = get_model_info()
    if not info:
        raise HTTPException(status_code=404, detail="No model trained yet.")
    return info


# ── Health Check ────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
