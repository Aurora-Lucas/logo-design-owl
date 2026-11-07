# 第三方素材与字体说明

本仓库原创部分以 CC BY-NC 4.0 发布，署名为 **Aurora Lucas**，项目地址为 <https://github.com/Aurora-Lucas/logo-design-owl/>。该许可仅覆盖贡献者有权许可的部分；以下第三方素材、字体及依赖保留各自的权利状态。

## Collegium 的纹章猫头鹰

- 素材：*Coa Illustration Elements Animal Owl Close Guardant*。
- 来源：*A Complete Guide to Heraldry*，1909 年，Arthur Charles Fox-Davies，插图 Graham Johnston。
- [Wikimedia Commons 文件页](https://commons.wikimedia.org/wiki/File:Coa_Illustration_Elements_Animal_Owl_Close_Guardant.svg)将该作品标注为公有领域。
- 用法：沿用原项目提取的纹章猫头鹰，结合项目绘制的羽毛笔、纹饰、环带与构图。当前构建所需的猫头鹰组保存在 `collegium-magicarum-scientiarum-logo/assets/owl-source.svg`。

公有领域素材的原有权利状态不因本仓库许可而改变。旧正式 SVG 中关于 `archive/` 的注释是原文件历史说明；为保持正式设计文件字节不变而保留，当前构建路径以脚本及 README 为准。

## Institutum 的版画猫头鹰

- 原作：*The Great White Owl*，1771 年，Anonymous, British, 18th century。
- 馆藏：The Metropolitan Museum of Art，馆藏编号 **1999.291.3**，对象 ID **750817**。
- [馆藏页面](https://www.metmuseum.org/art/collection/search/750817) · [原始图像](https://images.metmuseum.org/CRDImages/dp/original/DP879141.jpg)。项目保存的来源记录注明馆方 API `isPublicDomain: true`。
- 用法：裁切并清理纸张、文字和背景，将猫头鹰刻线转换为单色矢量；去除原树枝，使握爪与项目绘制的圆规衔接。
- 原图、派生矢量、处理材料及来源记录位于 `institutum-scientiae-magicae-logo/assets/`，完整记录见其中 `source.json`。

原始公有领域图像保留其原有权利状态。项目新增的圆规、植物饰边、环带、构图与排版按仓库原创部分许可发布。

## California sun

Collegium 的 `Litt.` 与 `Phil.` 沿用原设计中的 California sun 字形，正式 SVG 和 `assets/lettering.svg` 中均已转为路径。本地原字体的元数据注明：Copyright (c) 2020 by Kong font. All rights reserved.

[设计师的字体发布说明](https://www.dafont.com/california-sun-2.font)将免费 demo 限于个人及非商业使用；其他授权见 [FontKong 许可说明](https://fontkong.com/license/)。当前版本已移除原字体文件，未包含证明该字体字形可以按 CC BY-NC 再许可的授权材料。此前包含原字体和备份的分支历史已由当前版本的单一初始提交替换；当前发布树不含字体二进制、备份或历史稿件。

因此，**现有转曲文字的开放再许可及商业用途授权范围仍待核实**。添加 CC BY-NC 许可和移除字体文件不代表这些第三方权利已被解除。本次整理保持设计原样；重建字形时须通过 `CALIFORNIA_SUN_FONT` 提供自行取得适当授权的字体文件。

## Noto 字体

Institutum 的拉丁环文使用 **Noto Serif Display**；正式版已转为路径，可编辑版仍保留文字。重建时通过 `NOTO_SERIF_DISPLAY_FONT` 指定 Noto Serif Display 字体文件，避免静默替换。展示板使用本机可用的中文 Noto 字体，或由 `PREVIEW_SANS_FONT`、`PREVIEW_SERIF_FONT` 指定的字体。仓库不分发这些字体二进制。

Noto 字体软件采用 SIL Open Font License 1.1；其许可对使用字体制作的文档另有规定。参见 [Noto 官方许可](https://github.com/notofonts/latin-greek-cyrillic/blob/main/OFL.txt)。自行安装或分发字体时应保留相应字体包的许可文件。

## 软件依赖

Pillow、sharp、`@napi-rs/canvas` 及可选的素材提取依赖仍遵循各自许可。它们通过包管理器安装，不将 `node_modules/` 或本机依赖目录纳入仓库；仓库 CC BY-NC 不替代第三方软件许可。
