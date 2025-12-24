"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from todo_app.api.router import api_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="ToDo List API",
        description="A RESTful API for managing projects and tasks.",
        version="3.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Health check endpoint
    @app.get("/", tags=["Health"])
    def health_check() -> dict[str, str]:
        """Check API health status."""
        return {"status": "ok", "message": "ToDo List API is running"}

    # Include API routes
    app.include_router(api_router)

    # Global exception handler for unexpected errors
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred", "error": str(exc)},
        )

    return app


app = create_app()