# ppt-ultimate-creator · 终极ppt生成

中文 | [English](README.md)

从目录、文档、论文、网页或提纲出发，与用户逐步打磨内容和视觉，生成原生可编辑 PowerPoint 的 Codex 技能。

## 工作流

1. 确认资料范围，核对来源与证据缺口。
2. 澄清受众、目的、风格和逐页大纲；支持用户提供或根据资料自动提案。
3. 通过 HTML 草稿确认内容与大布局。
4. 用 AI 生图制作高保真样张，再生成全套视觉稿并多轮确认。
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
