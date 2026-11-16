# omni-price 全网比价

> 开源的全网比价引擎：聚合淘宝 / 京东 / 拼多多等主流电商平台商品价格，一次搜索、多平台对比。
> 官方联盟 API 优先、第三方聚合服务兜底、网页采集可选的三通道可插拔架构。

## 特性（规划）

- 🔍 **多平台搜索比价**：统一关键词搜索，跨平台价格对比，找出当前最低
- 🔌 **三通道数据源**：官方联盟 API（淘宝联盟 / 京东联盟 / 多多进宝）→ 第三方聚合（大淘客 / 好单库）→ 网页采集，逐层降级
- 🧩 **适配器架构**：新增平台只需实现 `PlatformAdapter` 接口
- 💻 **多入口**：HTTP API（FastAPI）、CLI、MCP Server（供 AI Agent 调用）
- 💾 **本地优先**：SQLite 存储搜索历史与价格快照，支持历史价格趋势
- ⚖️ **合规底线**：不绕过平台验证、不编造价格，采集失败如实上报

## 快速开始

```bash
# 需要 Python 3.11+
pip install -e .

# 配置平台凭证（可选，无凭证时仅网页采集通道可用）
cp .env.example .env

# 启动 API 服务
omni-price serve
# 打开 http://127.0.0.1:8790/docs 查看 OpenAPI 文档

# CLI 搜索
omni-price search "无线鼠标"
```

## 架构

```
src/omniprice/
├── models.py          # 统一商品/价格数据模型
├── comparator.py      # 跨平台聚合与比价逻辑
├── platforms/         # 平台适配器（taobao / jd / pdd …）
│   └── base.py        # PlatformAdapter 抽象接口
├── providers/         # 通道实现：官方联盟 API / 聚合服务 / 网页采集
├── api/               # FastAPI HTTP 服务
├── cli.py             # 命令行入口
└── mcp_server.py      # MCP Server（AI Agent 工具）
```

## 文档

- [竞品调研](docs/research/竞品调研.md) — PriceRadar / price-compare-skill / AgenticCPS 等现有项目分析
- [技术选型](docs/技术选型.md) — 架构决策记录
- [联盟账号注册清单](docs/联盟账号注册清单.md) — 淘宝联盟 / 京东联盟 / 多多进宝接入准备

## Roadmap

- [ ] M1：数据模型 + 适配器接口 + 京东联盟官方 API 通道跑通
- [ ] M2：淘宝联盟（TOP）+ 多多进宝（DDK）通道
- [ ] M3：大淘客 / 好单库聚合兜底通道
- [ ] M4：CLI / MCP / 简单 Web 界面，历史价格趋势

## License

[MIT](LICENSE)

## 致谢与参考

- [AgenticCPS](https://github.com/zhuangpengLI/AgenticCPS)（AGPL-3.0）— 平台适配器架构与联盟准入文档参考
- [price-compare-skill](https://github.com/hopkdj/price-compare-skill)（MIT）— 轻量爬虫方案参考
- [PriceRadar 价探](https://github.com/E-R-Butch/PriceRadar) — 本地工作台形态参考（源码可见但禁止二开，仅参考思路）
