# ppt-ultimate-creator

[中文](README.zh-CN.md) | English

A Codex skill for creating editable PowerPoint presentations from directories, documents, papers, web pages, or outlines. Display name: **终极ppt生成**.

## Workflow

1. Confirm sources and resolve missing evidence.
2. Clarify audience, purpose, style, and a slide-by-slide outline, either supplied by the user or proposed from the sources.
3. Review an HTML draft for content and layout.
4. Generate a high-fidelity AI image sample, then iterate on the full visual deck with the user.
5. Rebuild the approved design with native editable PowerPoint objects.
6. Render the actual PPTX, compare it with the approved visuals and content specification, and repair discrepancies.

Accuracy and semantic editability take priority over exact visual matching. Disclose small visual differences. Images remain replaceable image objects; they are not internally editable shapes.

## Installation and use

Copy `skills/ppt-ultimate-creator` into `${CODEX_HOME:-~/.codex}/skills/` without overwriting an existing customized skill. Invoke `$ppt-ultimate-creator` with your materials and presentation requirements.

The skill supplies workflow instructions, not a standalone rendering engine. Execution requires AI image generation, a PPTX construction library, and an actual PPTX renderer available in the environment.

## Templates

The default runtime library is `~/.ppt-ultimate-creator/templates/`, with `defaults/` and `custom/` subdirectories. Create them if needed:

```sh
mkdir -p ~/.ppt-ultimate-creator/templates/{defaults,custom}
```

The repository includes empty matching folders only. No downloaded templates or preview assets are bundled. Put your templates in the runtime library, or specify another directory when invoking the skill. Files added to the repository template folders are ignored by Git by default.

## Validation

Run the Codex skill-creator validator on `skills/ppt-ultimate-creator` using Python with PyYAML installed. Structural validation and an outline-stage behavioral simulation passed. A full AI-image-to-editable-PPTX run has not yet been tested.

Design-method references and their sources are in [design-methods.md](skills/ppt-ultimate-creator/references/design-methods.md). Maintenance state is recorded in [HANDOFF.md](HANDOFF.md).
