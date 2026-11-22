> 此副本托管在 https://github.com/DIOovo/aimarket 。

# FaceOnTrend 竞品 sitemap 日报 — 完整交接包

这份压缩包是给**另一个 AI** 独立接手「竞品模板日报」用的完整交接，而不只是一份库存快照。截止时点以 `store/ledger.json` 为准：

**2026-11-22T09:34:26+08:00（Asia/Shanghai）**，当时库存 **3673** 个模板、**28** 家竞品。`baseline=false`。上一轮检查时间为 `2026-11-21T09:40:54+08:00`。

自家产品是 [FaceOnTrend](https://faceontrend.com/)，仓库是 https://github.com/DIOovo/faceontrend 。不要再把 pioneertemplate.com 当作线上站点。

本包只包含从磁盘和公开页面**复制或抓取**的资料，**没有改动** live store，也没有 commit、push 或修改 FaceOnTrend 代码。上一份仅含库存与扫描记录的包（`/workspace/competitor-monitoring-export-2026-11-22.zip`）没有被覆盖；其说明副本在 `extras/previous-export-README.md`。

## 新 AI 从这里读起

按这个顺序即可开始工作，不必先猜规则：

1. 本文件（交接首页与文件树）
2. `docs/01-每日任务原文.md` — 每日要做什么的原文，以及调度时间
3. `docs/02-操作口径与例外.md` — 赫阳已确认或实践定下的口径（不要再发明规则）
4. `docs/03-快照与算法.md` — ledger / 单站快照字段，以及 `core_key` / `ALIASES` 撞车算法（指向 `scripts/`）
5. `docs/04-FaceOnTrend本站模板.md` 与 `data/faceontrend-templates.json` — 本站当前公开模板，用来对照竞品缺页
6. 当前库存：`store/`（不要把结构拆散）
7. 需要动手跑扫描时，再打开 `scripts/`，并把脚本里的 `STORE` / `OUTDIR` 改到你的环境；先对照 `store/`，再写回 store

日报只在有确认的新视频模板时发给**赫阳**，用**中文**，短、带可点击的 markdown 链接。没有新增就保持安静，不要发「今日无新增」。

## store 如何迁移

- 当前权威库存是 `store/`，对应原路径 `/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps/`。
- 可以整目录迁到新环境的持久 store，但请保持「一个目录里放 `ledger.json` + 28 个 `{sitekey}.json` + `excluded-non-templates.json`」这个结构，不要把各站文件拆到别处。
- 不要用某天的 `daily-scans/*/store-backup-pre` 或 `extras/store-baseline-pre-scan-2026-11-22/` 当成最新库存；那些是写入前的备份。
- 新环境路径若不同，只改脚本常量，不要改快照字段含义。

## 文件树

```
competitor-monitoring-handover-2026-11-22/
  README.md                          ← 本交接首页
  docs/
    01-每日任务原文.md
    02-操作口径与例外.md
    03-快照与算法.md
    04-FaceOnTrend本站模板.md
  data/
    faceontrend-templates.json       ← 本站 70 个公开模板（2026-11-22 抓取）
    raw/sitemap.xml
    raw/robots.txt
  store/                             ← 当前竞品库存（source of truth，截止同上）
    ledger.json
    excluded-non-templates.json
    overlaps-2026-11-07.json / .md
    {sitekey}.json                   ← 28 家
  daily-scans/                       ← 历史每日扫描工作目录
    2026-11-05/                      ← 早期部分站点抓取，尚无中文日报
    2026-11-12/ … 2026-11-22/        ← 日报流程（11/06–11/11 磁盘上本来就没有这些目录）
  scripts/                           ← 2026-11-22 的现行方法脚本
    scan.py、scrape_ricebowl.py、finalize.py、finalize_today.py、check_urls.py、…
  extras/
    store-baseline-pre-scan-2026-11-22/  ← 11/22 扫描开始前的 store 备份
    previous-export-README.md            ← 上一份导出包的说明
```

打包时排除了 `__pycache__` / `*.pyc`。每日 `raw/` 下的 sitemap 与 WebFetch 原文都保留了。

## 调度与日常动作（摘要）

细节以 `docs/01` 原文和 `docs/02` 为准。摘要如下：

- 每天约 09:00 Asia/Shanghai 扫描，可灵活 ±30 分钟；cron：`CRON_TZ=Asia/Shanghai 0 9 * * *`
- 抓各站 sitemap 与稳定的模板目录，和 `store/` 上次快照对比
- 新站第一次只建基线，不把存量当新增
- 核实 URL 可打开后，更新 store，再发中文日报；文末必须有「多家共有」（或写「今日无多家共有」）
- 目录扩容/回填/照片模板记入库存，不在正文逐条列出；Smew 仅作存量时用脚注，不要抬高主文家数
- 抓取失败不覆盖该站快照；sitemap 消失但页面仍 200 则保留并备注

## 本包仍缺、无法补上的内容

- 磁盘上本来就没有 `competitor-scan-2026-11-06` 至 `2026-11-11` 的工作目录，因此那几天的逐日抓取产物、以及 2026-11-10 为 aiMakeVideo / Try a Trend / Memelry 建基线的当时运行文件，都不在本包。操作口径里记录了那次基线条数（37 / 41 / 270），但没有原始工作目录可核对。
- 2026-11-05 之前的监控历史也不在本包。`store/overlaps-2026-11-07.md` 是保留在 store 里的一份更早撞车报告。
- 本包没有单独的 routine/cron 配置文件，只有文档中写明的调度约定。
- FaceOnTrend 本站 70 个模板里，有 69 个标题来自目录 ItemList，没有在本次逐条再请求页面；只有不在 ItemList 中的 `gta-6-loading-screen-ai` 被单独打开并确认 HTTP 200。详见 `docs/04-FaceOnTrend本站模板.md`。
