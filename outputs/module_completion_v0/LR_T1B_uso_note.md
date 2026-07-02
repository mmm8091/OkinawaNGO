# LR T1-B USO Okinawa 赞助与服务网络 note v0

日期：2026-07-03

线上可完成部分（公开官网 + 基地社区报），无需当地协作者。守口径：USO 是美军社区服务组织，按观察到的功能编码，不预设亲/反基地立场。

## 服务对象

USO Okinawa 服务现役军人、预备役 / 国民警卫队、军属配偶及家属（S097）。**服务对象是美军人员与军属家庭，不是冲绳平民社会**——按功能编码为 base_community_service / military_family_service。

## 中心 / 场域（8 处，site-presence）

USO Camp Kinser、USO Camp Hansen、USO Kadena、USO Camp Foster、USO Kadena AMC Terminal、USO Okinawa Area Office、USO Futenma、USO Camp Schwab（S097）。

现表已有 site-presence 边 F003（Camp Schwab）、F004（Camp Foster）、F005（Kadena）；其余 5 处见本 note，暂不逐一建边。

## 赞助方（sponsor → USO Okinawa）

USO Okinawa sponsors 页（S097）公开分层：

| 层级 | 赞助方 | 边 |
|---|---|---|
| Silver | American Engineering Corporation（AEC, X003） | **F002（升 E4）** |
| Platinum | Mediatti Broadband（MBC） | F034 |
| Mission Partner | Matson、University of Maryland Global Campus（UMGC） | F035（Matson）；UMGC 见 note |
| Community Partner | AIG Auto Insurance | note |
| Bronze | Billabong | note |
| 其他 | AK Kogyo American Finance Service、Domino's Pizza Japan | note |
| （本地企业捐赠） | Phoenix Park Hotel（¥1,000,000） | F001（既有） |

**AEC（F002 升 E4）**：52 年老伙伴；建 USO Camp Schwab 中心（2022）、Indo-Pacific 办公室搬迁（2022）；最近一次 16,000 美元捐赠（Stripes S098）。

## 口径与缺口

- 多数赞助方（UMGC/AIG/Billabong/AK Kogyo/Domino's）未入 actor registry，作为企业赞助节点记在本 note；只有金额 / 年份明确的（AEC、Phoenix）建 E4 边，其余 E3。
- 未确认金额的 sponsor 一律标 E3，不写具体数额。
- USO 是服务组织不是运动 actor（现表 X001 已如此编码）。
