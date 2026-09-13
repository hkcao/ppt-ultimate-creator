# ppt-ultimate-creator

[中文](README.zh-CN.md) | English

A Codex skill for creating editable PowerPoint presentations from directories, documents, papers, web pages, or outlines. Display name: **终极ppt生成**.

## Visual examples

![Academic, product and roadmap visual concepts](docs/images/visual-concepts.png)

AI-generated visual concepts illustrating possible directions, not rendered PPTX output or bundled templates. Content, style and editable objects are created and checked for each actual task.

The initial conversation asks whether you have a reference template. If you do, it is used; otherwise the skill suggests directions for academic, product, solution, teaching or technical-planning presentations.

## Workflow

1. Understand the mechanism and ask the user to clarify scope, depth, audience, and purpose before drafting slides. Ground experimental data and conclusions in the original source.
2. Clarify audience, purpose, style, and a slide-by-slide outline, either supplied by the user or proposed from the sources.
3. Review an HTML draft for content and layout.
4. Approve a high-fidelity AI sample, then automatically expand, rebuild and validate; ask again for material deviations.
5. Rebuild the approved design with native editable PowerPoint objects.
6. Render the actual PPTX, compare it with the approved visuals and content specification, and repair discrepancies.

Accuracy and semantic editability take priority over exact visual matching. Disclose small visual differences. Images remain replaceable image objects; they are not internally editable shapes.

## Installation and use

In an agent that supports skill installation (such as Codex), enter:

```text
Install the skill from https://github.com/hkcao/ppt-ultimate-creator.
The skill directory is skills/ppt-ultimate-creator.
```

Then try:

```text
Use $ppt-ultimate-creator to create an 8-slide presentation from my paper
for an engineering audience. Focus on the mechanism and experimental
results. Ask whether I have a reference template before suggesting a style,
and preserve experimental values when reusing or redrawing figures.
```

Skill discovery and installation locations vary between agents; this repository primarily targets Codex. For manual installation:


Copy `skills/ppt-ultimate-creator` into `${CODEX_HOME:-~/.codex}/skills/` without overwriting an existing customized skill. Invoke `$ppt-ultimate-creator` with your materials and presentation requirements.

The skill supplies workflow instructions, not a standalone rendering engine. Execution requires AI image generation, a PPTX construction library, and an actual PPTX renderer available in the environment.

## Templates

The default runtime library is `~/.ppt-ultimate-creator/templates/`, with `defaults/` and `custom/` subdirectories. Create them if needed:

```sh
mkdir -p ~/.ppt-ultimate-creator/templates/{defaults,custom}
```

The repository includes empty matching folders only. No downloaded templates are bundled. README concept artwork is separate from the template library. Put your templates in the runtime library, or specify another directory when invoking the skill. Files added to the repository template folders are ignored by Git by default.

## Validation

Run the Codex skill-creator validator on `skills/ppt-ultimate-creator` using Python with PyYAML installed. Structural validation and an outline-stage behavioral simulation passed. A full AI-image-to-editable-PPTX run has not yet been tested.

Design-method references and their sources are in [design-methods.md](skills/ppt-ultimate-creator/references/design-methods.md). Maintenance state is recorded in [HANDOFF.md](HANDOFF.md).

## Execution helpers

Default fonts are Microsoft YaHei for Chinese and Times New Roman for English. Choose original images, clearer annotations or data-verified redraws for experimental figures/tables. Preserve values exactly and disclose when image contents are not editable. Independent pages can run through subagents with central review and assembly.

The skill includes `scripts/extract_pdf.py --help` for batch PDF extraction (requires PyMuPDF), and `scripts/storyboard.py --help` for basic content HTML from current draft JSON (standard library only). The latter does not implement arbitrary layouts; finish the intended layout before requesting layout approval. Run helper tests with `python -m unittest discover -s tests -v` (requires PyMuPDF). End-to-end speed and parallelization gains have not been benchmarked.

## Fewer checkpoints and external image generation

Start with one combined kickoff confirmation, review the outline and HTML together, then approve a representative AI sample. Without an ask tool, send a plain-text question and end the turn to wait for the answer. Full-deck generation and reconstruction proceed automatically; detailed confirmation remains available.

Subagents use `fork_turns="none"` and receive only bounded page tasks and evidence. Batch similar simple pages, use script concurrency for network calls, and avoid repeatedly reading full documents or returning large code blocks. Total token savings are not guaranteed.

[External image configuration](skills/ppt-ultimate-creator/references/image-backend.md) supports a separate endpoint, model and API-key environment variable. The adapter targets synchronous OpenAI-compatible Images text-to-image APIs, including compatible non-GPT models. It requires Pillow; native Gemini, asynchronous APIs and image editing are not implemented. Protocol tests use mocked responses; a live provider has not been tested.

## Category-specific style and layout guides

Common principles remain shared; category guidance is maintained separately and loaded on demand. User templates take priority, and mixed decks can select guidance per section.

- [Academic](skills/ppt-ultimate-creator/references/styles/academic.md)
- [Product](skills/ppt-ultimate-creator/references/styles/product.md)
- [Solution review](skills/ppt-ultimate-creator/references/styles/solution.md)
- [Teaching](skills/ppt-ultimate-creator/references/styles/course.md)
- [Technical planning](skills/ppt-ultimate-creator/references/styles/technical-planning.md)

## Other agents and native multimodal capabilities

Use the current model or host's available vision, image generation and editing capabilities directly. GPT, OpenAI APIs and the bundled image script are not mandatory. Check each capability separately: image input does not imply image output. External APIs are a fallback for missing capabilities, subject to the host's actual interfaces and rules.

Check mathematical fonts and actual equation rendering separately; do not assemble complex equations from Unicode lookalikes. Follow the step-by-step explanation style of user-provided teaching material: objects, computation, transmission and recovery before general formulas, rather than copying only the final dense diagram.
