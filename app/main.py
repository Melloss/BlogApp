from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI,Request,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .database import engine,Base
from .routes import auth,blog
from pydantic import BaseModel,Field
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI(
    title='Blog App',
    version='1.0.0',
    contact={
        "name": "Melloss",
        "url": "https://melloss.dev",
        # "email": "mellossdev@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "message": "string",
                        "error_type": "string"
                    }
                }
            },
        }
    },
)

class ServerResponse(BaseModel):
    message : str
    error_type : Optional[str] = Field(default=None)
    

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> ServerResponse:
    error = exc.errors();
    customError =  ServerResponse(
        message=error[0]['msg'],
        error_type=error[0]['type']
    )
    return JSONResponse(content=customError.model_dump(),status_code=422)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    custom_error = ServerResponse(
        message=exc.detail if isinstance(exc.detail, str) else "An error occurred",
        error_type="http_error"
    )
    return JSONResponse(content=custom_error.model_dump(), status_code=exc.status_code)




app.include_router(auth.router,prefix='/auth',tags=["Auth"])
app.include_router(blog.router,prefix='/blog',tags=["Blog"])

