# FaceOnTrend 本站模板清单

对照竞品缺页时，以本站公开页面上**实际抓到**的模板为准。机器可读副本：`data/faceontrend-templates.json`。抓取原文：`data/raw/sitemap.xml`、`data/raw/robots.txt`。

抓取时间：**2026-11-22T12:31:22+08:00**（Asia/Shanghai）。本文件不虚构任何 URL。

## 来源

- 正式站：https://faceontrend.com/
- 仓库（只作参考，**未 clone、未改文件、未 push**）：https://github.com/DIOovo/faceontrend
- `robots.txt`（HTTP 200）声明 sitemap 为 https://faceontrend.com/sitemap.xml
- 打开并保存了 https://faceontrend.com/sitemap.xml （HTTP 200，application/xml，共 84 条 `<loc>`）
- 打开了模板目录 https://faceontrend.com/templates （HTTP 200，标题 All AI Video Templates | FaceOnTrend），其中有 ItemList JSON-LD，**69** 条
- 打开了专题页 https://faceontrend.com/gta （HTTP 200），其中链到 3 个模板：`/templates/gta-6-loading-screen-ai`、`/templates/gta-5-goodbye-ai`、`/templates/dropped-truck-gta-6-ai`
- 对 sitemap 有、但目录 ItemList 没有的那一条，单独请求了 https://faceontrend.com/templates/gta-6-loading-screen-ai ，HTTP 200；页面 H1 为 “GTA 6 Loading Screen”，`<title>` / og:title 为 “GTA 6 Loading Screen AI Filter | FaceOnTrend”

## 数量

- **模板页共 70 个**：sitemap 里路径为 `/templates/{slug}` 且不是目录页本身的条目。
- 其中 69 个同时出现在 `/templates` 的 ItemList 中，标题用 ItemList 的 `name`。
- 另外 1 个 `gta-6-loading-screen-ai` 在 sitemap 和 `/gta` 专题页中，页面可打开，但不在当时的目录 ItemList 里；标题用该页 H1。
- 其余 14 条 sitemap URL 不是单模板页（首页、目录、专题、博客、指南、定价与法律页），列在文末，不计入模板数。
- 这 69 个已在 ItemList 中的模板 URL，**没有在本次再逐条发 HTTP 请求**；它们来自当日可打开的 sitemap 与目录页。若需要更强校验，接手后可再逐条核对 200。

本次从本机访问 https://www.faceontrend.com/sitemap.xml 与 https://www.faceontrend.com/robots.txt 时 TLS 失败（`unexpected eof`）。清单全部使用已成功打开的 apex 域名 https://faceontrend.com 。

## 模板列表（70）

| # | 标题 | slug | URL | sitemap lastmod (Asia/Shanghai 偏移已写在值内) | 标题来源 |
|---|---|---|---|---|---|
| 1 | Coffee Making AI | `coffee-making-ai` | https://faceontrend.com/templates/coffee-making-ai | 2026-11-01T22:31:07+08:00 | 目录 ItemList |
| 2 | AI Arrest | `ai-arrest-ai` | https://faceontrend.com/templates/ai-arrest-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 3 | BadTimes AI | `bad-times-ai` | https://faceontrend.com/templates/bad-times-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 4 | Bulin 47 | `bulin-47-ai` | https://faceontrend.com/templates/bulin-47-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 5 | Damon Salvatore AI | `damon-salvatore-ai` | https://faceontrend.com/templates/damon-salvatore-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 6 | Dime Dime Baby | `dime-dime-baby-ai` | https://faceontrend.com/templates/dime-dime-baby-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 7 | Halloween Dance | `halloween-dance-ai` | https://faceontrend.com/templates/halloween-dance-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 8 | Millionaire AI | `millionaire-ai` | https://faceontrend.com/templates/millionaire-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 9 | WindowPeeper | `window-peeper-ai` | https://faceontrend.com/templates/window-peeper-ai | 2026-11-02T12:50:00+08:00 | 目录 ItemList |
| 10 | Fancy Cafe | `first-time-in-a-fancy-cafe-ai` | https://faceontrend.com/templates/first-time-in-a-fancy-cafe-ai | 2026-11-03T21:15:00+08:00 | 目录 ItemList |
| 11 | Jisoo Addicted Dance | `jisoo-addicted-dance-ai` | https://faceontrend.com/templates/jisoo-addicted-dance-ai | 2026-11-03T22:00:00+08:00 | 目录 ItemList |
| 12 | End of Watch AI | `end-of-watch-ai` | https://faceontrend.com/templates/end-of-watch-ai | 2026-11-04T17:35:00+08:00 | 目录 ItemList |
| 13 | Chipmunks Dance AI | `chipmunks-dance-ai` | https://faceontrend.com/templates/chipmunks-dance-ai | 2026-11-04T21:03:00+08:00 | 目录 ItemList |
| 14 | Flamingo Float AI | `flamingo-float-ai` | https://faceontrend.com/templates/flamingo-float-ai | 2026-11-04T22:06:00+08:00 | 目录 ItemList |
| 15 | 58th Floor AI | `58th-floor-ai` | https://faceontrend.com/templates/58th-floor-ai | 2026-11-05T12:00:00+08:00 | 目录 ItemList |
| 16 | 2027 New Year AI | `2027-new-year-ai-trend` | https://faceontrend.com/templates/2027-new-year-ai-trend | 2026-11-05T16:20:15+08:00 | 目录 ItemList |
| 17 | Hop Hop Hop AI | `hop-hop-hop-ai` | https://faceontrend.com/templates/hop-hop-hop-ai | 2026-11-06T12:35:05+08:00 | 目录 ItemList |
| 18 | Fancy Restaurant | `first-time-at-a-fancy-restaurant-ai` | https://faceontrend.com/templates/first-time-at-a-fancy-restaurant-ai | 2026-11-06T15:37:09+08:00 | 目录 ItemList |
| 19 | Money Flex AI | `money-flex-ai` | https://faceontrend.com/templates/money-flex-ai | 2026-11-06T16:12:17+08:00 | 目录 ItemList |
| 20 | Bicep Heart AI | `bicep-heart-ai` | https://faceontrend.com/templates/bicep-heart-ai | 2026-11-07T14:27:51+08:00 | 目录 ItemList |
| 21 | Closing Door Prank AI | `closing-door-prank-ai` | https://faceontrend.com/templates/closing-door-prank-ai | 2026-11-07T14:36:32+08:00 | 目录 ItemList |
| 22 | Toc Toc Dance AI | `toc-toc-dance-ai` | https://faceontrend.com/templates/toc-toc-dance-ai | 2026-11-07T15:03:17+08:00 | 目录 ItemList |
| 23 | Wassup in a Minute AI | `wassup-in-a-minute-ai` | https://faceontrend.com/templates/wassup-in-a-minute-ai | 2026-11-07T15:35:24+08:00 | 目录 ItemList |
| 24 | My Ride Is Here AI | `my-ride-is-here-ai` | https://faceontrend.com/templates/my-ride-is-here-ai | 2026-11-07T17:18:33+08:00 | 目录 ItemList |
| 25 | Epic Dunk AI | `epic-dunk-ai` | https://faceontrend.com/templates/epic-dunk-ai | 2026-11-07T17:26:21+08:00 | 目录 ItemList |
| 26 | Burning Bridges AI | `burning-bridges-ai` | https://faceontrend.com/templates/burning-bridges-ai | 2026-11-07T17:46:26+08:00 | 目录 ItemList |
| 27 | Dame Hombro AI | `dame-hombro-ai` | https://faceontrend.com/templates/dame-hombro-ai | 2026-11-07T19:39:29+08:00 | 目录 ItemList |
| 28 | Tiny Desk AI | `tiny-desk-ai` | https://faceontrend.com/templates/tiny-desk-ai | 2026-11-07T20:05:34+08:00 | 目录 ItemList |
| 29 | Fish Cutting Meme AI | `fish-cutting-meme-ai` | https://faceontrend.com/templates/fish-cutting-meme-ai | 2026-11-08T14:10:33+08:00 | 目录 ItemList |
| 30 | Vossi Bop AI | `vossi-bop-ai` | https://faceontrend.com/templates/vossi-bop-ai | 2026-11-08T15:33:16+08:00 | 目录 ItemList |
| 31 | Shoulder Carry AI | `shoulder-carry-ai` | https://faceontrend.com/templates/shoulder-carry-ai | 2026-11-08T16:41:46+08:00 | 目录 ItemList |
| 32 | JME AI Video | `jme-ai-video` | https://faceontrend.com/templates/jme-ai-video | 2026-11-09T10:11:34+08:00 | 目录 ItemList |
| 33 | I Love The Smiths AI | `i-love-the-smiths-ai` | https://faceontrend.com/templates/i-love-the-smiths-ai | 2026-11-09T11:05:11+08:00 | 目录 ItemList |
| 34 | Can I Ride Dance AI | `can-i-ride-dance-ai` | https://faceontrend.com/templates/can-i-ride-dance-ai | 2026-11-09T12:46:19+08:00 | 目录 ItemList |
| 35 | Schooling Seniors AI | `schooling-seniors-ai` | https://faceontrend.com/templates/schooling-seniors-ai | 2026-11-09T21:06:18+08:00 | 目录 ItemList |
| 36 | Shut Up Stormzy AI | `shut-up-stormzy-ai` | https://faceontrend.com/templates/shut-up-stormzy-ai | 2026-11-10T14:52:42+08:00 | 目录 ItemList |
| 37 | Ain’t You My Gangsta B AI | `aint-you-my-gangsta-b-ai` | https://faceontrend.com/templates/aint-you-my-gangsta-b-ai | 2026-11-11T11:09:22+08:00 | 目录 ItemList |
| 38 | Dito Ang Tingin AI | `dito-ang-tingin-ai` | https://faceontrend.com/templates/dito-ang-tingin-ai | 2026-11-11T11:26:44+08:00 | 目录 ItemList |
| 39 | No Scrubs AI | `no-scrubs-ai` | https://faceontrend.com/templates/no-scrubs-ai | 2026-11-11T12:14:09+08:00 | 目录 ItemList |
| 40 | Drake Hotline Bling AI | `drake-hotline-bling-ai` | https://faceontrend.com/templates/drake-hotline-bling-ai | 2026-11-11T14:54:47+08:00 | 目录 ItemList |
| 41 | Dancing Dog Pool Party AI | `dancing-dog-pool-party-ai` | https://faceontrend.com/templates/dancing-dog-pool-party-ai | 2026-11-11T15:57:32+08:00 | 目录 ItemList |
| 42 | Celebrity Red Carpet AI | `celebrity-red-carpet-ai` | https://faceontrend.com/templates/celebrity-red-carpet-ai | 2026-11-11T19:51:29+08:00 | 目录 ItemList |
| 43 | Hey Boo Come Slide With Me AI | `hey-boo-come-slide-with-me-ai` | https://faceontrend.com/templates/hey-boo-come-slide-with-me-ai | 2026-11-12T11:08:25+08:00 | 目录 ItemList |
| 44 | Careless Whisper Car AI | `careless-whisper-car-ai` | https://faceontrend.com/templates/careless-whisper-car-ai | 2026-11-12T16:52:06+08:00 | 目录 ItemList |
| 45 | Husband Emporium AI | `husband-emporium-ai` | https://faceontrend.com/templates/husband-emporium-ai | 2026-11-12T19:42:54+08:00 | 目录 ItemList |
| 46 | Spin That Coupe Like What AI | `manchester-united-locker-room-ai` | https://faceontrend.com/templates/manchester-united-locker-room-ai | 2026-11-13T09:41:13+08:00 | 目录 ItemList |
| 47 | Gangsta's Paradise AI | `gangstas-paradise-ai` | https://faceontrend.com/templates/gangstas-paradise-ai | 2026-11-13T09:56:50+08:00 | 目录 ItemList |
| 48 | Christmas Pajama Dance AI | `christmas-pajama-dance-ai` | https://faceontrend.com/templates/christmas-pajama-dance-ai | 2026-11-13T10:00:14+08:00 | 目录 ItemList |
| 49 | Misanthropy Meme AI | `misanthropy-meme-ai` | https://faceontrend.com/templates/misanthropy-meme-ai | 2026-11-13T10:33:46+08:00 | 目录 ItemList |
| 50 | Dog Grooming Time AI | `dog-grooming-time-ai` | https://faceontrend.com/templates/dog-grooming-time-ai | 2026-11-13T11:09:44+08:00 | 目录 ItemList |
| 51 | La Mujer del Pelotero AI | `la-mujer-del-pelotero-ai` | https://faceontrend.com/templates/la-mujer-del-pelotero-ai | 2026-11-13T11:09:44+08:00 | 目录 ItemList |
| 52 | BigXthaPlug Give It All AI | `bigxthaplug-give-it-all-ai` | https://faceontrend.com/templates/bigxthaplug-give-it-all-ai | 2026-11-14T14:28:20+08:00 | 目录 ItemList |
| 53 | Need for Speed AI | `need-for-speed-ai` | https://faceontrend.com/templates/need-for-speed-ai | 2026-11-16T11:00:00+08:00 | 目录 ItemList |
| 54 | Babydoll Dance AI | `babydoll-dance-ai` | https://faceontrend.com/templates/babydoll-dance-ai | 2026-11-16T11:10:00+08:00 | 目录 ItemList |
| 55 | Pimpwalk Entrance AI | `pimpwalk-entrance-ai` | https://faceontrend.com/templates/pimpwalk-entrance-ai | 2026-11-16T11:30:00+08:00 | 目录 ItemList |
| 56 | Pretend Drive AI | `pretend-drive-ai` | https://faceontrend.com/templates/pretend-drive-ai | 2026-11-16T11:45:00+08:00 | 目录 ItemList |
| 57 | King Jin AI | `king-jin-ai` | https://faceontrend.com/templates/king-jin-ai | 2026-11-16T12:00:00+08:00 | 目录 ItemList |
| 58 | Dancing with Santa AI | `dancing-with-santa-ai` | https://faceontrend.com/templates/dancing-with-santa-ai | 2026-11-17T12:00:00+08:00 | 目录 ItemList |
| 59 | Never Let Her Pay AI | `never-let-her-pay-ai` | https://faceontrend.com/templates/never-let-her-pay-ai | 2026-11-17T12:10:00+08:00 | 目录 ItemList |
| 60 | Te He Perdido AI | `te-he-perdido-ai` | https://faceontrend.com/templates/te-he-perdido-ai | 2026-11-17T13:00:00+08:00 | 目录 ItemList |
| 61 | Jingle Bell Brazil Dance AI | `jingle-bell-brazil-dance-ai` | https://faceontrend.com/templates/jingle-bell-brazil-dance-ai | 2026-11-17T13:30:00+08:00 | 目录 ItemList |
| 62 | Lil Yachty Walkout AI | `lil-yachty-walkout-ai` | https://faceontrend.com/templates/lil-yachty-walkout-ai | 2026-11-17T14:00:00+08:00 | 目录 ItemList |
| 63 | GTA 5 Goodbye AI | `gta-5-goodbye-ai` | https://faceontrend.com/templates/gta-5-goodbye-ai | 2026-11-18T11:34:10+08:00 | 目录 ItemList |
| 64 | Skibidi Babidi Boo Freestyle AI | `skibidi-babidi-boo-freestyle-ai` | https://faceontrend.com/templates/skibidi-babidi-boo-freestyle-ai | 2026-11-18T11:34:10+08:00 | 目录 ItemList |
| 65 | James Bond Reveal AI | `james-bond-reveal-ai` | https://faceontrend.com/templates/james-bond-reveal-ai | 2026-11-19T10:50:16+08:00 | 目录 ItemList |
| 66 | Pet Taxi AI | `pet-taxi-ai` | https://faceontrend.com/templates/pet-taxi-ai | 2026-11-19T16:50:51+08:00 | 目录 ItemList |
| 67 | Oh My Carne Asada AI | `oh-my-carne-asada-ai` | https://faceontrend.com/templates/oh-my-carne-asada-ai | 2026-11-20T12:35:33+08:00 | 目录 ItemList |
| 68 | Riding Lion AI | `riding-lion-ai` | https://faceontrend.com/templates/riding-lion-ai | 2026-11-20T16:56:52+08:00 | 目录 ItemList |
| 69 | GTA 6 Loading Screen | `gta-6-loading-screen-ai` | https://faceontrend.com/templates/gta-6-loading-screen-ai | 2026-11-21T18:47:00+08:00 | 模板页 H1（不在目录 ItemList） |
| 70 | Dropped Truck GTA 6 AI | `dropped-truck-gta-6-ai` | https://faceontrend.com/templates/dropped-truck-gta-6-ai | 2026-11-21T19:55:33+08:00 | 目录 ItemList |

## 未计入模板的 sitemap 页面（14）

| 类型 | URL | lastmod |
|---|---|---|
| home | https://faceontrend.com | 2026-11-06T16:12:17+08:00 |
| guide | https://faceontrend.com/ai-video-guide | 2026-11-06T16:12:17+08:00 |
| blog_index | https://faceontrend.com/blog | 2026-11-21T21:08:35+08:00 |
| blog_post | https://faceontrend.com/blog/gta-6-ai-car-loading-screen | 2026-11-21T21:08:35+08:00 |
| blog_post | https://faceontrend.com/blog/gta-ai-images-and-videos | 2026-11-21T21:04:53+08:00 |
| templates_index | https://faceontrend.com/templates | 2026-11-06T16:12:17+08:00 |
| gta_hub | https://faceontrend.com/gta | 2026-11-21T18:47:00+08:00 |
| marketing | https://faceontrend.com/pricing | 2026-11-06T16:12:17+08:00 |
| marketing | https://faceontrend.com/ai-models | 2026-10-27T20:53:55+08:00 |
| marketing | https://faceontrend.com/about | 2026-10-27T20:53:55+08:00 |
| legal | https://faceontrend.com/privacy | 2026-11-01T21:49:16+08:00 |
| legal | https://faceontrend.com/terms | 2026-10-27T20:53:55+08:00 |
| legal | https://faceontrend.com/acceptable-use-policy | 2026-10-27T20:53:55+08:00 |
| legal | https://faceontrend.com/refund | 2026-10-27T20:53:55+08:00 |

## 未做或做不到的事情

- 没有 clone https://github.com/DIOovo/faceontrend，因此本清单不是仓库内文件的导出，而是线上公开页的抓取结果。若仓库与线上不一致，以这次抓到的线上页为准，并应再核对仓库，而不是猜测。
- 没有发明未出现在 sitemap / 目录 ItemList / `/gta` 或已打开模板页上的 URL。
