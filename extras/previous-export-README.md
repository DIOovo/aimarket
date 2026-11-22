# FaceOnTrend 竞品模板监控归档

**Archive of FaceOnTrend (faceontrend.com) competitor-monitoring records and snapshots**, packed so another AI can continue the same watch without guessing URLs or rules.

- 本归档只包含从磁盘复制的记录与脚本，**没有改动** live store，也没有提交 / 推送 / 修改 FaceOnTrend 代码。
- 截止时点（source of truth：`store/ledger.json`）：**2026-11-22T09:34:26+08:00**（Asia/Shanghai）。上一轮检查：`2026-11-21T09:40:54+08:00`。
- 当时库存合计：**3673** 个模板（`total_templates`），覆盖 **28** 家站点（`sites_count`）。当日 `total_new=34`（其中日报正文 `total_digest_new=32`，仅记库存 `total_inventory_only_new=2`），`total_removed=0`，`baseline=false`。

## 产品与本监控的关系

- 我方产品仓库：https://github.com/DIOovo/faceontrend
- 线上站点：https://faceontrend.com （不是 pioneertemplate.com）
- 本归档监控的是 **28 家竞品模板站** 的 sitemap / 列表页变化，用于每天（有新增时）写中文「竞品模板日报」。

Live inventory 的原始路径（本机 durable store，本归档已复制到 `store/`）：

`/cursor/stores/store-d12ebb47-baec-4976-ab13-5e9017df26fd/competitor-sitemaps/`

每日扫描工作目录的原始路径：

`/workspace/competitor-scan-YYYY-MM-DD/`

## 目录结构

```
competitor-monitoring-export-2026-11-22/
  README.md                          ← 本说明
  store/                             ← 当前库存（source of truth，2026-11-22 09:34 快照）
    ledger.json
    excluded-non-templates.json
    overlaps-2026-11-07.json         ← 更早的撞车全量报告（2026-11-07），不是每日 diffs
    overlaps-2026-11-07.md
    {sitekey}.json                   ← 28 家各自的库存快照
  daily-scans/                       ← 历史每日扫描工作目录（只复制，未移动原目录）
    2026-11-05/                      ← 早期部分站点抓取，尚无中文日报 / scan.py
    2026-11-12/ … 2026-11-22/        ← 完整或接近完整的日报流程
  scripts/                           ← 2026-11-22 工作目录里的现行方法脚本（干净副本）
    scan.py                          ← 28 站 SiteSpec、路径过滤、sitemap 抓取
    scrape_ricebowl.py               ← Ricebowl 只从 /trends/meme ItemList 取真正 meme 模板
    finalize.py                      ← overlap 用的 core_key / strip_suffixes / ALIASES
    finalize_today.py                ← 2026-11-22 实际写 store + 日报的脚本（会扩展 ALIASES）
    finalize_run.py、check_urls.py、classify_hints.py、diff_today.py、…
  extras/
    store-baseline-pre-scan-2026-11-22/  ← 当日扫描开始前的 store 备份（来自 /workspace/competitor-sitemaps-2026-11-22/baseline）
```

- **当前库存请读 `store/`**，不要把某天的 `daily-scans/*/store-backup-pre` 或 `extras/store-baseline-pre-scan-2026-11-22` 当成最新库存。
- 从 2026-11-18 起，多数每日目录里还有 `store-backup-pre/`，那是**当天写入前**的 store 副本，可用来对照历史。
- 打包时排除了 `__pycache__` / `*.pyc` / `.git` / `node_modules`（后两项在源目录中本就不存在）。每日 `raw/` 下的 sitemap XML、列表页 HTML、Remake Your Meme 的 WebFetch 原文都保留了。

## 28 家监控名单（首页 URL 来自 ledger / scan.py，未杜撰）

下列 `file` 即 `store/{file}`。`home` 与当日 `template_count` 来自 `store/ledger.json`（2026-11-22T09:34:26+08:00）。`kind` 来自 `scripts/scan.py` 的 `SITES` / `accept()`。

| 显示名 | file（site key） | home | 当日库存 | scan.py kind / 路径规则（摘要） |
|---|---|---|---:|---|
| DoTheTrend | dothetrend.json | https://dothetrend.ai/ | 70 | `templates`：`/templates/{slug}` |
| TrendTemplate | trendtemplate.json | https://trendtemplate.com/ | 43 | `root_ai`：根路径 `/{slug}`（常见 `*-ai`） |
| MemeFX AI | memefxai.json | https://memefxai.com/ | 74 | `memefxai`：根路径，或把 `/templates/{slug}` 规范成根路径 |
| ClipRemake | clipremake.json | https://clipremake.com/ | 70 | `templates`：`/templates/{slug}` |
| Remake Your Meme | remakeyourmeme.json | https://remakeyourmeme.com/ | 44 | `templates`：`/templates/{slug}/`（保留尾斜杠） |
| MakeViral | makeviral.json | https://www.makeviral.ai/ | 602 | `templates`：`/templates/{slug}` |
| Smew AI | smew.json | https://smew.ai/ | 439 | `templates`：`/templates/{slug}` |
| MakeMeme.video | makememe.json | https://makememe.video/ | 165 | `makememe`：根路径 `/{slug}`；忽略 `/trends` 目录页与资源 URL |
| ViralRemake | viralremake.json | https://viralremake.com/ | 37 | `templates`：`/templates/{slug}` |
| MemeClone.ai | memeclone.json | https://memeclone.ai/ | 77 | `templates`：`/templates/{slug}` |
| TrendSwap | trendswap.json | https://trendswap.app/ | 57 | `trendswap`：根路径；`/templates/{slug}` 规范成根路径。另抓 `video-sitemap.xml`、`image-sitemap.xml` |
| Put Me In | putmein.json | https://putmein.app/ | 228 | `templates`：`/templates/{slug}`。另抓 `sitemap-media.xml` |
| SameVid AI | samevid.json | https://samevid.com/ | 342 | `samevid`：规范为 `/template/{slug}`（单数）；分类目录页不算模板 |
| ZapVid | zapvid.json | https://zapvid.ai/ | 44 | `zapvid`：仅根路径且 slug 以 `-ai-video-generator` 结尾 |
| Summrs | summrs.json | https://www.summrs.com/ | 81 | `summrs`：根路径，优先 `*-ai-video-generator` / `*-ai` / `*-ai-trend` |
| Trendify Video | trendify.json | https://trendify.video/ | 14 | `trends`：`/trends/{slug}` |
| Genjutsu AI | genjutsu.json | https://genjutsuai.cc/ | 45 | `genjutsu`：根路径；跳过 `/ai-video-trends` 聚合页 |
| DanceRemake | danceremake.json | https://danceremake.com/ | 21 | `templates`：`/templates/{slug}` |
| Starrd | starrd.json | https://www.getstarrd.app/ | 395 | `starrd`：规范为 `/template/{slug}`；`/templates/viral` 等分类页不算 |
| AI Trend Video | aitrendvideo.json | https://aitrendvideo.net/ | 10 | `aitrendvideo`：根路径 |
| Ricebowl AI | ricebowl.json | https://ricebowl.ai/ | 72 | sitemap 解析 kind 是 `ricebowl`（`/app/{slug}`），**真正入库只走** `/trends/meme` 的 ItemList（见下） |
| Kubflow | kubflow.json | https://kubflow.ai/ | 10 | `kubflow`：`/trends/{slug}` |
| PictureToVideo | picturetovideo.json | https://picturetovideo.org/ | 5 | `picturetovideo`：根路径效果页；跳过 `/ai-video-effects` 本身 |
| Bolly.AI | bolly.json | https://www.bolly.ai/ | 219 | `bolly`：`/template/{slug}` |
| RapVideo.ai | rapvideo.json | https://rapvideo.ai/ | 42 | `rapvideo`：根路径（也可能见到 `/tools|/trends|/templates/{slug}`） |
| aiMakeVideo | aimakevideo.json | https://aimakevideo.com/ | 52 | `aimakevideo`：根路径且 slug 以 `-ai` 结尾 |
| Try a Trend | tryatrend.json | https://tryatrend.com/ | 57 | `tryatrend`：根路径，`*-ai` / `*-ai-trend` / `*-trend` |
| Memelry | memelry.json | https://memelry.com/ | 358 | `memelry`：根路径，多为 `*-ai`；拒绝很长的 SEO 文章（≥10 个 token）及 `*-ai-tools` |

`scan.py` 里每站还有 `list_pages` 和部分 `extra_sitemaps`，以脚本为准。另有通用屏蔽：`GENERIC_BLOCK_SLUGS`（pricing / privacy / blog / login 等）以及 `EXTRA_BLOCK` / `store/excluded-non-templates.json`（解析可能误收入但不算模板的 slug）。

## 必须遵守的过滤与入库规则

这些规则写在 `scripts/scan.py`、`scripts/scrape_ricebowl.py`、`scripts/finalize_today.py` 以及往日日报 / `run-summary.json` 的附注里，后续监控应沿用：

1. **Ricebowl AI**：不要把 sitemap 里大量通用 `/app/` 工具页当作新模板。只把 https://ricebowl.ai/trends/meme 页面 ItemList（及对应 `/app/{slug}`）里的真正 meme 模板算库存。2026-11-22 的 `scan.log` 里 sitemap 解析曾得到 338 条，对照昨日库存 72；当日 ledger 附注写明：Meme catalog 相对昨日无新增，Generic `/app` tool pages 未入库。实现见 `scripts/scrape_ricebowl.py`。
2. **Remake Your Meme**：部分出口 IP 会对该站返回 **403**。2026-11-22 `scan.log`：列表页 403，sitemap 0 条，触发 `INCOMPLETE FETCH: got 0 vs previous 44; snapshot not replaced`。当日是用 WebFetch 拉 sitemap（原文在 `daily-scans/2026-11-22/raw/remakeyourmeme-sitemap-webfetch.md`），核对后库存仍为 44、无新增。不要因为 403 就把快照打成空。
3. **整站抓取失败或库存异常塌缩时，不得覆盖该站快照。** `scan.py`：若上一轮 ≥8 条、本轮少于 `max(3, prev*0.5)`，则 `fetch_ok=False` 并注明 `INCOMPLETE FETCH ... snapshot not replaced`。`finalize_today.py` 对许多站点采用「上一轮库存 + 人工核实后的 curated 新增」，而不是把 sitemap 原文整表写进 store（避免静态资源、分类页、SEO 页污染库存）。
4. **新站第一次建基线（baseline）时，不得把当时已有的库存全部当作「今日新增」去通知。** 本轮 `ledger.baseline=false`。历史里 Smew / Put Me In / SameVid 的目录扩容或回填是「入库但不在日报正文逐条列出」。
5. **同一玩法的 slug 改名或旧 URL 重定向到已有模板，不算新模板。** 例：Starrd 在 2026-11-17 快照中去掉 `bro-took-the-whole-bag-ai-video`，附注写明旧 URL 已重定向到已有的 `careless-whisper-car-ai-video`（见 `daily-scans/2026-11-18/store-backup-pre/starrd.json` 的 `note` / `removed_templates`，该备份是 11-17 写入后的状态）。
6. **若某模板从 sitemap 消失，但页面仍返回 200，应保留并在该站 note 里写明。** 2026-11-22 ledger 仍保留：Try a Trend 的 `ai-halloween-costume`、Summrs 的 `bigfoot-vlog`。对应逻辑在 `finalize_today.py` 的 `KEEP_MISSING`。
7. **目录扩容 / 回填 / 照片模板：入库，但不在日报正文里逐条罗列。** 已在日报原文中确认的例子：
   - 2026-11-12：Smew AI 相对昨日一次扩容 147 条（导语说明，不按 147 个全新玩法去膨胀「今日新模板」观感）。
   - 2026-11-16：Put Me In 把 11-15 一次性写入 sitemap 的模板入库 133 条（快照 10→143，lastmod 均为 2026-11-15），不逐条列出。
   - 2026-11-17：Put Me In 继续回填 86 条（快照至 226；其中 3 条为改名替换）。
   - 2026-11-20：SameVid AI 批量上架 82 个（多为他站已有梗的回填），仅记库存。
   - 2026-11-21：SameVid AI 再批量 42 个，仅记库存。
   - 2026-11-22：MakeViral 的 Black and White Wet Look、Starrd 的 AI Christmas Photo 为照片模板，记入库存，不在正文列出（`finalize_today.py` 的 `INV_ONLY`）。
8. **解析误伤不计「新模板」**：分类页、聚合页、FAQ、SEO 变体、通用工具页、静态资源、政策页等。屏蔽列表见 `store/excluded-non-templates.json` 与 `scan.py` 的 `GENERIC_BLOCK_SLUGS` / `EXTRA_BLOCK`。
9. **确认页面可打开（通常 HTTP 200）后再写入日报正文。** 用 `check_urls.py` 的结果（`url_checks.json`）人工/脚本核实标题与状态。

## ledger.json 与单站快照结构（以实文件为准）

### `store/ledger.json`

顶层字段（2026-11-22）：

- `checked_at`、`timezone`（Asia/Shanghai）、`previous_checked_at`
- `baseline`（本次为 `false`）
- `total_templates`、`total_new`、`total_digest_new`、`total_inventory_only_new`、`total_removed`
- `sites_count`、`sites_updated`、`sites_left_unchanged`
- `sites`：长度 28 的数组，每项含：
  - `site`（显示名）、`file`、`home`
  - `sitemap_existed`、`sitemap_urls_found`（该站用到的 sitemap URL 列表）
  - `template_count`、`new_count`、`removed_count`、`dropped_dead_count`
  - 可选 `note`（例如 WebFetch、保留失踪但仍 200 的条目、忽略 asset URL、照片模板仅记库存等）

注意：`total_removed` 在若干历史 ledger / run-summary 里可能仍为 0，即使当天某站实际从快照删过死链。例如 2026-11-19 Starrd 从快照去掉 23 个已 404 的旧页面，日报有脚注，但当天 run-summary 的 `ledger.total_removed` 仍为 0。删改细节以该站 snapshot 的 `removed_templates` / `note` 以及 `daily-scans/2026-11-19/run-summary.json` 的 `per_site.starrd.json.notes` 为准。

### `store/{sitekey}.json`

各站结构一致，核心字段：

- `site`、`home`、`checked_at`
- `sitemap_urls_found`、`sitemap_existed`
- `template_count`、`new_count`、`removed_count`
- `new_templates` / `removed_templates` / `templates`：数组，元素为 `{ "id_or_slug", "title", "url" }`
- 可选 `note`

`templates` 是该站当前完整库存。`new_*` / `removed_*` 是相对上一轮的增量。

## 撞车（overlap）怎么算

实现在 `scripts/finalize.py`（`ALIASES`、`SUFFIXES`、`strip_suffixes`、`core_key`、`slugify_words`、`pretty_name`），2026-11-22 当日又在 `scripts/finalize_today.py` 开头对 `fin.ALIASES` 做了增量更新。

计算步骤（不要凭感觉合并）：

1. 取模板 `id_or_slug` 的最后一段，小写、只保留 `[a-z0-9-]`。
2. 用 `strip_suffixes()` 反复去掉**站点风格后缀**，包括：`ai-video-generator`、`ai-character-swap`、`video-generator`、`ai-video`、`ai-trend`、`ai-dance`、`ai-meme`、`ai-filter`、`yapay-zeka`、`trend`、`ai`。也可以去掉开头的 `ai-`。脚本注释写明：**不要**去掉光秃的 `dance` / `video` / `meme` 这类词，否则会把不同玩法（如 christmas-dance 与 christmas-ai-video）折在一起。
3. 也用标题做一次同样的后缀剥离，作为备选。
4. 先对 slug core、再对 title core 查 `ALIASES` 表（例如 `grandpa-handles-dinner` → `fish-cutting`，`gta-ai-filter` → `gta-6-loading-screen`，`boom-clap` → `boom-clap-confetti`）。
5. 若 core 以 `hey-boo-` 开头，去掉此外缀后再查 alias。
6. 相同 `core_key` 出现在 ≥2 家，即算撞车。日报分两块：今日新增之间互相撞车，以及今日新增与他站**存量**撞车。
7. 展示名可用 `NAME_OVERRIDE` 或从标题去掉 “AI Video Generator / AI Trend / AI …” 后缀。

完整 alias 表以脚本为准，不要只靠本 README 复述。每日结果在 `daily-scans/YYYY-MM-DD/overlaps-today.json`，中文列表通常在日报文末「多家共有」，以及（11-12 至 11-21）`多家共有-不含Smew-YYYY-MM-DD.md`。把 Smew 从主计数里拆出去，是为了避免 Smew 目录扩容把「有几家在做同一玩法」刷得虚高；主文 overlap 里 Smew 常常写成「另有 Smew AI」。

2026-11-22 的 `run-summary.json`：`overlap_count=12`（当日互相撞车 5 组 + 与存量撞车 7 组）。

## 每日流程（观察自工作目录与 ledger，本归档里没有单独的 routine 配置文件）

从已有 `checked_at` 看，扫描通常在 **Asia/Shanghai 上午约 09:12–10:14** 完成，11-18 之后多数落在 **09:34–09:43** 附近（11-15 曾到 10:14，11-16 到 09:51）。意图是每天这个时段跑一轮；**只有确认有新的视频模板时才发中文日报**；无新增日应保持安静、不要为「扫描已完成」打扰。

建议步骤（与 11-22 脚本一致）：

1. 备份当前 `store/`（历史做法：工作目录下的 `store-backup-pre/`）。
2. 跑 `scan.py`，写出 `fetch_results.json` 和 `raw/` 下的 sitemap / 列表页。
3. Remake Your Meme 若 403，改用 WebFetch（或同等不依赖本机出口 IP 的方式）拉取 sitemap，再比对；失败则保持旧快照。
4. 跑 `scrape_ricebowl.py`，只接受 `/trends/meme` ItemList。
5. 跑 `diff_today.py` / `classify_hints.py`，再对候选 URL 跑 `check_urls.py`。
6. 人工（或按 `finalize_today.py` 的 DIGEST / INV_ONLY / KEEP_MISSING）裁定：哪些是正文新模板、哪些仅记库存、哪些是解析误伤、哪些失踪但仍 200 要保留。
7. 写回 `store/{site}.json` 与 `store/ledger.json`，生成 `竞品模板日报-YYYY-MM-DD.md`、`overlaps-today.json`、`run-summary.json`。
8. 日报家数与「今日共 N 个新模板」应以 **digest 新模板** 为准，不要把 Smew / Put Me In lastmod 批量 / SameVid 回填 / 照片模板算进正文条数。这些项可以写在导语或脚注。

历史日报与合计（有 ledger 或 run-summary 的天数）：

| 日期 | checked_at (Asia/Shanghai) | store 总库存 | ledger/run-summary 的 total_new | 日报正文宣称的新模板数（如有） |
|---|---|---:|---:|---|
| 2026-11-05 | （早期抓取，无 ledger / 无日报） | — | — | 无 |
| 2026-11-12 | （有日报与 scan.py；当日 run-summary 未按后来的 ledger 格式保存总库存） | — | — | 228（导语同时说明 Smew 扩容 147） |
| 2026-11-13 | 2026-11-13T09:18:30+08:00 | 2865 | 80 | 80 |
| 2026-11-14 | 2026-11-14T09:12:48+08:00 | 2918 | 53 | 53 |
| 2026-11-15 | 2026-11-15T10:14:26+08:00 | 3012 | 94 | 94 |
| 2026-11-16 | 2026-11-16T09:51:46+08:00 | 3190 | 46 | 46（另：Put Me In 入库 133，不逐条） |
| 2026-11-17 | 2026-11-17T09:39:00+08:00 | 3343 | 156 | 70（另：Put Me In 再回填 86） |
| 2026-11-18 | 2026-11-18T09:43:11+08:00 | 3403 | 60 | 59 |
| 2026-11-19 | 2026-11-19T09:40:27+08:00 | 3454 | 74 | 73（另：Starrd 去掉 23 个 404 页） |
| 2026-11-20 | 2026-11-20T09:39:28+08:00 | 3563 | 109 | 27（另：SameVid 回填 82） |
| 2026-11-21 | 2026-11-21T09:40:54+08:00 | 3639 | 76 | 34（另：SameVid 回填 42） |
| 2026-11-22 | 2026-11-22T09:34:26+08:00 | 3673 | 34 | 32（另：2 个照片模板仅记库存） |

`total_new` 与日报正文条数不必相等：前者常含回填 / 仅记库存，后者是要发给人看的「今日新视频模板」。

## 已在文件中确认的注意事项

- **Remake Your Meme 403**：2026-11-22 及此前多日 `scan.log` / ledger `note` 均写明本机（box）IP 对该站 403；sitemap 经 WebFetch 取得；库存保持 44。
- **Starrd 2026-11-19 下架 23 个 404 页面**：日报脚注「Starrd 有 23 个旧模板页今日已 404，已从快照去掉，不在此逐条列出。」完整 slug 列表见 `daily-scans/2026-11-19/run-summary.json` → `per_site.starrd.json.notes`，以及次日备份 `daily-scans/2026-11-20/store-backup-pre/starrd.json` 的 `removed_templates`（该文件 `checked_at` 为 2026-11-19T09:40:27+08:00）。被去掉的包括 `ai-personal-trainer-prank`、`tokyo-drift-ai-dance`、`zombie-love-story-ai-video` 等 23 条（同时新增的 Need for Speed Extended 只记库存、不单独上日报）。
- **Starrd 分类路径 404 不入库**：2026-11-22 快照 note：「Category paths that 404 were not added。」
- **SameVid 分类列表路径不入库**：2026-11-22 note：「Category listing paths from sitemap not added。」当日只新增 1 个真正模板（The Last Dance 单人版，与已有双人 Last Dance 不是同一个；alias 里刻意保持 `the-last-dance` 独立）。
- **MakeMeme / TrendTemplate sitemap 里的静态资源 URL 要忽略**（2026-11-22 ledger notes：「Asset URLs in sitemap ignored.」）。
- **Memelry / Summrs / Ricebowl**：SEO 卫星页、照片教程、通用工具页、helper 页不入库。
- 磁盘上 **没有** `competitor-scan-2026-11-06` 至 `2026-11-11` 的工作目录；11-05 是早期、不完整的抓取（约 7 站的 sitemap / `*.new.json`，无中文日报）。若需要 11-07 的全量撞车快照，见 `store/overlaps-2026-11-07.md`。

## 历史每日目录里常见文件

完整日（尤其 11-15 之后）通常包括：

- 脚本：`scan.py`、`finalize.py` / `finalize_today.py` / `finalize_run.py`、`scrape_ricebowl.py`、`check_urls.py`、`classify_hints.py`、`diff_today.py`
- 数据：`fetch_results.json`、`diff_raw.json`、`curated_new.json` / `curated_source.json`、`inventory_only.json`、`filtered_out.json`、`url_checks.json`、`ricebowl_catalog.json`、`overlaps-today.json`、`run-summary.json`、有时还有当天的 `ledger.json`
- 日报：`竞品模板日报-YYYY-MM-DD.md`、`notice-zh.txt`（内容往往与日报相同或接近）、`多家共有-不含Smew-YYYY-MM-DD.md`（11-22 没有单独出这份，撞车写在日报文末）
- `raw/`：各站 sitemap / robots / 列表 HTML；Remake Your Meme 的 `remakeyourmeme-sitemap-webfetch.md`
- 11-18 起常见 `store-backup-pre/`

继续监控时：把 `scripts/` 拷到新的 `/workspace/competitor-scan-YYYY-MM-DD/`，把脚本内部的 `STORE` / `OUTDIR` / `CHECKED_AT` / `PREV_CHECKED_AT` 改成当天路径（注意：`scripts/finalize.py` 里仍留着旧的 `OUTDIR=.../competitor-scan-2026-11-21` 和更早的 `PREV_CHECKED_AT`，2026-11-22 实际写盘用的是 `finalize_today.py`）。**先对照 `store/` 再写回 live store。**

## 不要做的事

- 不要把 sitemap 原文或工具页/SEO 页未经核实就整表覆盖库存。
- 不要发明或改写本 README 里没有出现、且文件中也没有的竞品 URL。
- 不要把 https://faceontrend.com 写成其他域名。
- 不要在未得到用户明确授权时修改 FaceOnTrend 产品仓库或推送代码。
