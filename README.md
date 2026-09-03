# Technical Standard Skills

Reusable, Agent-neutral Skills for technical standard architecture, engineering contracts, machine-contract projection, implementation planning, contract-driven coding, and publication workflows.

包含九个 Skill：

- technical-specification-guide v0.7.0
- engineering-contract-spec v0.3.0
- machine-contract-spec v0.1.0
- conformance-specification v0.1.0
- implementation-design-guide v0.1.0
- contract-implementation-planner v0.2.1
- contract-driven-coding v0.1.1
- technical-document-publisher v0.6.0
- assessment-question-designer v0.2.0

版本：

- technical-specification-guide v0.7.0
- engineering-contract-spec v0.3.0
- machine-contract-spec v0.1.0
- conformance-specification v0.1.0
- implementation-design-guide v0.1.0
- contract-implementation-planner v0.2.1
- contract-driven-coding v0.1.1
- technical-document-publisher v0.6.0
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
