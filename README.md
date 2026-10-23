# TSP

**Typesetting Profiles（排版配置）**。

排版方式集中在 `technical-document-publisher/profiles/`，技能调用名称仍为
`technical-document-publisher`。本仓库同时保留现有技术写作、工程契约、实现规划和验证技能。

| 编号 | 排版方式 | 入口 |
|---|---|---|
| 01 | 技术白皮书 | [profiles/01](technical-document-publisher/profiles/01/profile.md) |
| 02 | 中文技术报告横线表版 | [profiles/02](technical-document-publisher/profiles/02/profile.md) |

后续实际增加版式时按 `03`、`04` 依次编号，目录名使用两位数字。
示例：使用 technical-document-publisher，按 02 排版这份设备选型报告。

包含九个 Skill：

- technical-specification-guide v0.7.0
- engineering-contract-spec v0.3.0
- machine-contract-spec v0.1.0
- conformance-specification v0.1.0
- implementation-design-guide v0.1.0
- contract-implementation-planner v0.2.1
- contract-driven-coding v0.1.1
- technical-document-publisher v0.9.0
- assessment-question-designer v0.2.0

版本：

- technical-specification-guide v0.7.0
- engineering-contract-spec v0.3.0
- machine-contract-spec v0.1.0
- conformance-specification v0.1.0
- implementation-design-guide v0.1.0
- contract-implementation-planner v0.2.1
- contract-driven-coding v0.1.1
- technical-document-publisher v0.9.0
- assessment-question-designer v0.2.0

推荐工程链：

```text
Architecture / Design
        ↓
Engineering Contract
        ↓
Implementation Planning
        ↓
Contract-Driven Coding
        ↓
Verification
```

Publication 是旁路能力：approved technical content 可以交给
`technical-document-publisher` 发布为 DOCX/PDF，不是 Coding 的必经步骤。

本版本增加 Reader-first Architecture Writing、Anti-AI Language review 与 Human Readability Gate，确保复杂技术指南在保留深度的同时，先建立读者地图、设计主线和连续运行故事。

最终文档一键调用：

```text
使用 technical-document-publisher，把这份 Markdown 生成最终可发布 DOCX 和 PDF。
```

该请求默认进入 FINAL RELEASE MODE，自动编排源文档审计、题目审计、冻结、DOCX/PDF、三层
Fidelity Gate、逐页 Visual QA 和可修复缺陷的重建闭环；明确说“严格按冻结 Markdown 发布，不修改源文档”
才进入 STRICT PUBLISH MODE。

推荐安装方式：

```text
clone repository
→ run install.sh
→ symlink into ~/.agents/skills/
```
