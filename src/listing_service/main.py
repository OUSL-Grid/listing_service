from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from listing_service.config import settings
from listing_service.events.publisher import event_publisher
from listing_service.routers import listings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await event_publisher.connect()
    yield
    # Shutdown
    await event_publisher.close()


app = FastAPI(
    title="Listings Service API",
    description="""
    ## Campus Marketplace — Listings Service

    Handles buy/sell item listings for verified university students.

    ### Features
    * Create, read, update, delete listings
    * Search & filter by category, price, keyword
    * Flag listings for moderation
    * Publishes events to NATS: `listing.created`, `listing.updated`,
      `listing.sold`, `listing.flagged`

    ### Authentication
    All endpoints require a valid JWT (RS256) issued by the Auth Service.
    Include it as: `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    contact={
        "name": "OSUL-Grid Team",
        "url": "https://github.com/OSUL-Grid/listing_service",
    },
    license_info={"name": "MIT"},
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,      # ← lifespan මෙතනම දාන්න
)

# CORS (access to frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(listings.router, prefix="/api/v1", tags=["listings"])


@app.get("/health", tags=["system"], summary="Health check")
async def health_check():
    """Check the service is alive."""
    return {"status": "ok", "service": "listings"}