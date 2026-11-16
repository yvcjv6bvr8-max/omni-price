"""命令行入口：`omni-price search "无线鼠标"` / `omni-price serve`。"""
from __future__ import annotations

import asyncio
import json

import typer

from omniprice.comparator import compare
from omniprice.models import Platform

app = typer.Typer(help="omni-price 全网比价 CLI")


@app.command()
def search(
    keyword: str,
    platforms: str = typer.Option(None, help="逗号分隔，如 taobao,jd,pdd；缺省为全部"),
    limit: int = typer.Option(20, min=1, max=50),
) -> None:
    """关键词比价，JSON 输出；全部平台失败时退出码为 1。"""
    selected = [Platform(p.strip()) for p in platforms.split(",")] if platforms else None
    result = asyncio.run(compare(keyword, selected, limit))
    typer.echo(result.model_dump_json(indent=2))
    if not result.items:
        raise typer.Exit(code=1)


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8790) -> None:
    """启动 HTTP API 服务。"""
    import uvicorn

    uvicorn.run("omniprice.api.main:app", host=host, port=port)


@app.command()
def history(keyword: str = typer.Option(None)) -> None:
    """查看搜索历史与价格快照（TODO M4：SQLite 落地后实现）。"""
    typer.echo(json.dumps({"todo": "M4: 历史记录待实现", "keyword": keyword}))
