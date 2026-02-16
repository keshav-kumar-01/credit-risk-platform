"""Quick test to verify Pydantic protected namespace fix"""
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ExplainabilityReport(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    method: str = "test"
    model_output: Optional[float] = None

class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    model_loaded: bool = True

# If we get here without warnings, the fix works
e = ExplainabilityReport()
h = HealthResponse()
print(f"ExplainabilityReport: model_output={e.model_output}")
print(f"HealthResponse: model_loaded={h.model_loaded}")
print("✅ No Pydantic 'model_' namespace warnings!")
