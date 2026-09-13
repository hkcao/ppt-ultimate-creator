# 独立生图 API

此文档只用于外部 API 路径，不约束宿主原生多模态能力。用户指定后端优先；否则优先当前模型的原生图像输出或宿主现有生图能力，不要求 GPT/OpenAI，也不要求经过随附脚本。识别图片直接使用已有视觉输入能力；生成、识别、编辑分别判断，不能互相推定。确实缺少所需生图能力时再读取用户独立配置。未知提供商/模型不自动选择付费服务。必要时把 endpoint、模型选择与需求澄清合并询问，密钥让用户在本机环境设置，不要求粘贴到聊天。

## 已实现的适配范围

`scripts/generate_image.py` 支持同步、Bearer 认证的 OpenAI-compatible Images **文生图** API：JSON 请求包含 model/prompt/n，返回 `data[0].b64_json` 或 `data[0].url`。模型名称可为兼容服务的非 GPT 模型；“OpenAI-compatible”描述协议，不要求使用 OpenAI 服务。

协议参考：[Images API](https://developers.openai.com/api/reference/resources/images)。第三方是否兼容、支持哪些尺寸/参数，需要核实该提供商文档；不是任意模型 API 通用适配器。本脚本的 Gemini 原生协议、异步任务轮询和 multipart 图像编辑适配尚未实现；这不限制宿主已有的对应原生能力。需要通过外部 API 调用而非已有能力时，用户指定此类服务时按其官方接口新增窄适配器并测试，不能直接套这个脚本。

此适配器不上传图片，也不支持参考图/局部编辑。将已确认布局转成精确文字提示生成样张，向用户说明参考图约束能力；任务必须精确参考图编辑时更换支持该能力的后端，不能假装已传入图片。原文图表在最终 PPT 嵌回原件。

## 独立配置

默认 `~/.ppt-ultimate-creator/image-api.json`，也可通过 `--config` 指定，配置不写入技能。示例中域名、模型必须替换成用户选定提供商的实际值：

```json
{
  "endpoint": "https://provider.example/v1/images/generations",
  "model": "YOUR_IMAGE_MODEL",
  "api_key_env": "PPT_IMAGE_API_KEY",
  "timeout": 180,
  "parameters": {"size": "1024x1024", "response_format": "b64_json"}
}
```

参数仅为示例，不支持的字段删除。密钥只保存在配置指定的环境变量中；勿写入 JSON、提示词、日志、状态、worker 任务包或 Git。配置位置和环境变量名称可传 worker，密钥本身不可传入模型上下文。

```sh
python scripts/generate_image.py --config ~/.ppt-ultimate-creator/image-api.json --prompt /path/to/prompts/s01.txt --output /path/to/visuals/s01-v1
```

Python 需要 Pillow。输出为 image.png 与无密钥 record.json，提示词保留在项目 prompts 中。输出目录必须不存在。脚本仅发一次生成请求，不自动重试不确定的超时，避免重复计费；先查服务状态/已有结果，再决定是否重试。HTTPS 请求不跟随重定向，图片下载不携带生成 API 密钥。错误不回显提供商响应体。

首次使用只跑需要的代表性样张，不额外生成无用探针。用户配置并选择后端即按该任务使用，发送该页所需最小提示词，勿上传整篇资料或其他页面。先记录样张成功和能力边界，再按提供商实际限额并发；切换后端可能改变风格，应重新核对代表性样张。
