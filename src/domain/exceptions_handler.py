from fastapi import Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import NotFound


async def not_found_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exc.name} not found."}, )
