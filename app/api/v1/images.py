from urllib.parse import quote, unquote

import httpx
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

router = APIRouter(tags=["images"])

PROXY_BASE = "/api/v1/images/proxy"


def to_proxy_url(value: str) -> str:
    if PROXY_BASE in value:
        return value
    return f"{PROXY_BASE}?url={quote(value, safe='')}"


@router.get("/proxy")
async def proxy_image(url: str = Query(...)):
    decoded = unquote(url)
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(
            decoded,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; PortafolioBot/1.0)",
            },
        )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to fetch image: {resp.status_code}",
            )
        content_type = resp.headers.get("content-type", "image/jpeg")
        return Response(content=resp.content, media_type=content_type)
