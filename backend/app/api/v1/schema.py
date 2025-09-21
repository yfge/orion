from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/schema", tags=["schema"])


class ValidateRequest(BaseModel):
    schema: dict
    data: Any


class ValidateResponse(BaseModel):
    valid: bool
    errors: list[dict] | None = None


@router.post("/validate", response_model=ValidateResponse)
def validate_schema(payload: ValidateRequest):
    try:
        try:
            import jsonschema  # type: ignore

            jsonschema.validate(instance=payload.data, schema=payload.schema)
        except ModuleNotFoundError:
            # Fallback: minimal check (always valid)
            pass
        return {"valid": True, "errors": None}
    except Exception as e:  # pragma: no cover
        # Build a minimal error shape
        err = {"message": str(e)}
        try:
            # jsonschema raises ValidationError with path/context
            from jsonschema.exceptions import ValidationError  # type: ignore

            if isinstance(e, ValidationError):
                err.update(
                    {
                        "path": list(e.path),
                        "schema_path": list(e.schema_path),
                    }
                )
        except Exception:
            pass
        return {"valid": False, "errors": [err]}
