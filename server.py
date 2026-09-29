# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import numpy as np
from apex_guard import EntropyGuard, CodeDriftAuditor, SchemaSyncEngine

app = FastAPI(title="ApexGuard Live Engine", version="3.0.0")

@app.middleware("http")
async def apex_guard_middleware(request: Request, call_next):
    body = await request.body()
    payload_str = body.decode("utf-8", errors="ignore")
    
    # Audit incoming payload entropy and velocity
    audit_report = EntropyGuard.audit_request(payload_str, request_velocity_hz=18.5)
    
    if audit_report["status"] == "QUARANTINED_BOT_ANOMALY":
        return JSONResponse(
            status_code=429,
            content={"error": "Traffic blocked by ApexGuard EntropyGuard", "report": audit_report}
        )
        
    response = await call_next(request)
    return response

@app.post("/api/v1/execute")
async def execute_task(payload: dict):
    return {"status": "SUCCESS", "message": "Payload passed entropy inspection."}

@app.post("/api/v1/audit-code")
async def live_code_audit(data: dict):
    lambda_core = data.get("lambda_core", [6.0, 5.0, 7.2])
    v_overhead = np.array(data.get("v_overhead", [[1.0, 0.8, 0.4], [0.8, 1.0, 0.9], [0.4, 0.9, 1.0]]))
    
    auditor = CodeDriftAuditor(lambda_core, v_overhead)
    return auditor.audit_architecture()

@app.post("/api/v1/sync-schema")
async def live_schema_sync(data: dict):
    old_spec = data.get("old_spec", {})
    new_spec = data.get("new_spec", {})
    return SchemaSyncEngine.compare_specs(old_spec, new_spec)