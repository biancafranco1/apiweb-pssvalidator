
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.models.classes import PasswordRequest, PasswordResponse
from app.services.validate_password import validate_password

app = FastAPI()

@app.post("/user/validate", response_model=PasswordResponse)
async def validation_pss(request: PasswordRequest):
    try:        
        notvalid = validate_password(request.password)
        if notvalid:
            return PasswordResponse(valid=False, notvalid=notvalid)
        return PasswordResponse(valid=True, notvalid=[])
    except Exception as e:
        print(f"Erro ao validar senha: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Ocorreu um erro de processamento no servidor"}
        )


