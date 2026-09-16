# ppt-ultimate-creator · 终极ppt生成

中文 | [English](README.md)

从目录、文档、论文、网页或提纲出发，与用户逐步打磨内容和视觉，生成原生可编辑 PowerPoint 的 Codex 技能。

## 视觉示例

![学术、产品与路线图视觉概念](docs/images/visual-concepts.png)

AI 生成的视觉概念，展示可能的呈现方向；不是实际 PPTX 渲染，也不是内置模板。最终内容、风格和可编辑对象按每次任务生成与检查。

先询问你是否有参考模板；有则沿用，没有再根据学术汇报、产品介绍、方案研讨、课程或技术规划用途给建议。

## 工作流

1. 先理解关键原理，用 ask 类交互澄清范围、深度、受众和目的，再写大纲；实验数据与结论必须来自原文。
2. 澄清受众、目的、风格和逐页大纲；支持用户提供或根据资料自动提案。
3. 通过 HTML 草稿确认内容与大布局。
4. 确认 AI 高保真样张后，自动扩展全套并重建校验；重大偏离再提问。
5. 以原生文字、图形、连接符、图表、表格重建可编辑 PPT。
6. 渲染实际 PPTX，与确认图片及内容规格对比并修复。

优先级为内容准确、语义结构可编辑、视觉还原。少量视觉差异应明确说明；独立图片可移动和替换，不代表其内部可编辑。

## 安装与使用

在支持技能安装的 Agent（例如 Codex）中直接输入：

```text
帮我安装 https://github.com/hkcao/ppt-ultimate-creator 中的技能，
技能目录是 skills/ppt-ultimate-creator。
```

安装后调用示例：

```text
使用 $ppt-ultimate-creator，根据我提供的论文制作 8 页中文汇报，
面向研发团队，重点讲关键机制与实验结果。先问我是否有参考模板，
合并确认启动需求；实验图表可截图或基于核实数据重绘。
```

不同 Agent 的技能目录和发现机制可能不同；本仓库首先面向 Codex。也可手动安装：


将 `skills/ppt-ultimate-creator` 复制到 `${CODEX_HOME:-~/.codex}/skills/`，已有自定义版本时先比较，避免覆盖。使用 `$ppt-ultimate-creator` 并提供资料和汇报需求。

这是工作流与参考文档型技能，不是独立生成引擎。执行环境需要提供真实 AI 生图、PPTX 构建库和实际 PPTX 渲染能力。

## 模板文件夹

默认读取 `~/.ppt-ultimate-creator/templates/` 下的 `defaults/` 和 `custom/`。不存在时可创建：

```sh
mkdir -p ~/.ppt-ultimate-creator/templates/{defaults,custom}
```

仓库预留模板文件夹，不再分发第三方模板原件；工作汇报默认模板按下方官方来源下载到本机库。README 概念示例与模板库分开。将自己的模板放入上述运行时目录，或在调用时指定其他路径。仓库模板文件夹中的新增文件默认被 Git 忽略。

## 验证与维护

使用带 PyYAML 的 Python，运行 Codex skill-creator 的 `quick_validate.py` 检查 `skills/ppt-ultimate-creator`。结构校验与大纲阶段模拟行为测试已通过；尚未完成真实 AI 生图至可编辑 PPTX 的全流程测试。

[设计方法](skills/ppt-ultimate-creator/references/design-methods.md) 包含各类用途的表达建议与研究来源。

## 执行优化

默认中文微软雅黑、英文 Times New Roman；实验图表按可读性保留原图、重标注或基于核实数据重绘，数值必须一致；原图明确图内不可编辑。多页可由 subagent 并行准备，由主 agent 统一确认和组装。

技能内 `scripts/extract_pdf.py --help` 提供批量 PDF 提取（依赖 PyMuPDF）；`scripts/storyboard.py --help` 从当前草稿 JSON 生成基础内容 HTML（仅标准库）。后者不自动实现任意布局，需完善布局后才交用户确认。脚本测试：`python -m unittest discover -s tests -v`（需 PyMuPDF）。并行收益及完整制作速度尚未进行基准测量。

## 精简交互与外部生图

默认先做一次合并启动确认，再将大纲和 HTML 合并确认，最后确认代表性 AI 样张；没有 ask 工具时普通提问并结束本轮等待答复。全套生成和重建自动推进，支持按需切回详细确认。

Subagent 明确使用 `fork_turns="none"`，只接收页任务包与定点证据；简单相似页合批，纯网络请求用脚本并发，不继承整段聊天。减少重复读取与返回大段代码，但不保证降低总 token。

[外部生图配置](skills/ppt-ultimate-creator/references/image-backend.md) 支持独立设置 endpoint、模型及密钥环境变量。当前适配同步 OpenAI-compatible Images 文生图协议，可用非 GPT 模型；需要 Pillow，不含原生 Gemini、异步 API 或图像编辑适配。已通过模拟协议测试，尚无真实提供商联调。

## 分类样式与布局指南

通用原则保留在设计方法中，类别建议独立维护，执行时按需加载。用户模板优先，混合汇报可按章节选用。

- [学术汇报](skills/ppt-ultimate-creator/references/styles/academic.md)
- [产品介绍](skills/ppt-ultimate-creator/references/styles/product.md)
- [方案研讨](skills/ppt-ultimate-creator/references/styles/solution.md)
- [课程授课](skills/ppt-ultimate-creator/references/styles/course.md)
- [技术规划洞察](skills/ppt-ultimate-creator/references/styles/technical-planning.md)

## 非 Codex 与原生多模态

在其他 Agent 中，可直接使用当前模型/宿主已有的视觉识别、图像生成或编辑能力，不强制调用 GPT、OpenAI API 或随附生图脚本。识别、生成、编辑分别检查：仅能看图的模型不等于能生图。只有所需能力缺失时才启用外部 API；具体能力仍以运行环境实际提供的接口为准。

公式需独立检查数学字体与实际渲染，避免用 Unicode 字符拼复杂公式。学术汇报的大纲组织、例子选择和分步讲解方法集中维护在[学术指南](skills/ppt-ultimate-creator/references/styles/academic.md)。

数学表达必须使用可编辑的原生公式对象（相当于插入公式），不以普通文本或图片代替。学术指南补充可跟算例子、表格参数映射核对及内容层级要求；验收同时检查画布和内容容器边界。

## 工作汇报默认模板

工作汇报默认使用[华为 2021 年浅色 16:9 模板](https://e.huawei.com/cn/documents/others/4f951fb72e1944288d3aa73bf40d8a8b)，用户指定的模板优先。文件保存到 `~/.ppt-ultimate-creator/templates/defaults/huawei-work-report/template.pptx`；新环境缺失时按[工作汇报指南](skills/ppt-ultimate-creator/references/styles/work-report.md)从官方来源获取。

原件包含品牌与保密标记，需按实际用途处理；图表配色示意页不作为正式内容保留。原件版权归原权利人，仓库只提供来源与使用指导。
