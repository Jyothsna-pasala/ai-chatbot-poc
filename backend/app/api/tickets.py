from fastapi import APIRouter
from app.services.service import ticket_service

router = APIRouter()


@router.get("/tickets")
async def get_tickets():
    return ticket_service.get_all_tickets()