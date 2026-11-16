"""FastAPI HTTP 服务入口。"""
from __future__ import annotations

from fastapi import FastAPI, Query

from omniprice import __version__
from omniprice.comparator import compare
from omniprice.models import Platform, SearchResult

app = FastAPI(title="omni-price", version=__version__, description="开源全网比价引擎")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.get("/api/search", response_model=SearchResult)
async def search(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    platforms: list[Platform] | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=50),
) -> SearchResult:
    return await compare(keyword=q, platforms=platforms, limit=limit)
