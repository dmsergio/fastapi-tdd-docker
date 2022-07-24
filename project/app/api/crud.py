from typing import List
from typing import Union

from app import summarizer
from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    article_summary = summarizer.generate_summary(payload.url)
    summary = await TextSummary(
        url=payload.url,
        summary=article_summary,
    )
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    return None


async def get_all() -> List:
    return await TextSummary.all().values()


async def delete(id: int) -> int:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary


async def put(id: int, payload: SummaryPayloadSchema) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).update(
        url=payload.url,
        summary=payload.summary,
    )
    if summary:
        return await TextSummary.filter(id=id).first().values()

    return None
