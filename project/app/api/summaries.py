from typing import List

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import HTTPException
from fastapi import Path

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema
from app.models.pydantic import SummaryResponseSchema
from app.models.pydantic import SummaryUpdatePayloadSchema
from app.models.tortoise import SummarySchema
from app.summarizer import generate_summary


router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema,
    background_tasks: BackgroundTasks,
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    background_tasks.add_task(generate_summary, summary_id, payload.url)

    return SummaryResponseSchema(
        id=summary_id,
        url=payload.url,
    )


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(id: int = Path(..., gt=0)) -> SummaryResponseSchema:
    summary = await crud.get(id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id)

    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema,
    id: int = Path(..., gt=0),
) -> SummarySchema:
    summary = await crud.put(id, payload)
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
