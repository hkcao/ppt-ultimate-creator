# ppt-ultimate-creator · 终极ppt生成

中文 | [English](README.md)

从目录、文档、论文、网页或提纲出发，与用户逐步打磨内容和视觉，生成原生可编辑 PowerPoint 的 Codex 技能。

## 工作流

1. 先理解关键原理，用 ask 类交互澄清范围、深度、受众和目的，再写大纲；实验数据与结论必须来自原文。
2. 澄清受众、目的、风格和逐页大纲；支持用户提供或根据资料自动提案。
3. 通过 HTML 草稿确认内容与大布局。
4. 确认 AI 高保真样张后，自动扩展全套并重建校验；重大偏离再提问。
5. 以原生文字、图形、连接符、图表、表格重建可编辑 PPT。
6. 渲染实际 PPTX，与确认图片及内容规格对比并修复。

优先级为内容准确、语义结构可编辑、视觉还原。少量视觉差异应明确说明；独立图片可移动和替换，不代表其内部可编辑。

## 安装与使用

将 `skills/ppt-ultimate-creator` 复制到 `${CODEX_HOME:-~/.codex}/skills/`，已有自定义版本时先比较，避免覆盖。使用 `$ppt-ultimate-creator` 并提供资料和汇报需求。

这是工作流与参考文档型技能，不是独立生成引擎。执行环境需要提供真实 AI 生图、PPTX 构建库和实际 PPTX 渲染能力。

## 模板文件夹

默认读取 `~/.ppt-ultimate-creator/templates/` 下的 `defaults/` 和 `custom/`。不存在时可创建：

```sh
mkdir -p ~/.ppt-ultimate-creator/templates/{defaults,custom}
```

仓库仅预留对应空文件夹，不附带下载模板或预览。将自己的模板放入上述运行时目录，或在调用时指定其他路径。仓库模板文件夹中的新增文件默认被 Git 忽略。

## 验证与维护

使用带 PyYAML 的 Python，运行 Codex skill-creator 的 `quick_validate.py` 检查 `skills/ppt-ultimate-creator`。结构校验与大纲阶段模拟行为测试已通过；尚未完成真实 AI 生图至可编辑 PPTX 的全流程测试。

[设计方法](skills/ppt-ultimate-creator/references/design-methods.md) 包含五类用途的表达建议与研究来源；维护状态见 [HANDOFF.md](HANDOFF.md)。

## 执行优化

默认中文微软雅黑、英文 Times New Roman；原文实验图表优先沿用截图或提取图片，明确图内不可编辑。多页可由 subagent 并行准备，由主 agent 统一确认和组装。

技能内 `scripts/extract_pdf.py --help` 提供批量 PDF 提取（依赖 PyMuPDF）；`scripts/storyboard.py --help` 从当前草稿 JSON 生成基础内容 HTML（仅标准库）。后者不自动实现任意布局，需完善布局后才交用户确认。脚本测试：`python -m unittest discover -s tests -v`（需 PyMuPDF）。并行收益及完整制作速度尚未进行基准测量。

## 精简交互与外部生图

默认将大纲和 HTML 合并确认，再确认代表性 AI 样张；需求有关键缺口时先加一次合并澄清。全套生成和重建自动推进，支持按需切回详细确认。

Subagent 明确使用 `fork_turns="none"`，只接收页任务包与定点证据；简单相似页合批，纯网络请求用脚本并发，不继承整段聊天。减少重复读取与返回大段代码，但不保证降低总 token。

[外部生图配置](skills/ppt-ultimate-creator/references/image-backend.md) 支持独立设置 endpoint、模型及密钥环境变量。当前适配同步 OpenAI-compatible Images 文生图协议，可用非 GPT 模型；需要 Pillow，不含原生 Gemini、异步 API 或图像编辑适配。已通过模拟协议测试，尚无真实提供商联调。
