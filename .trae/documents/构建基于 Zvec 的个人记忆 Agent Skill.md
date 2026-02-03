### 概念对齐：什么是 "Skill"？

在这个项目中，我们将 **Skill** 定义为 **"赋予 Agent 的可插拔能力模块"**。

具体来说，它包含三个层面：
1.  **底层实现 (Python)**：实际干活的代码（例如：操作 Zvec 数据库、读写 Markdown 文件）。
2.  **Agent 接口 (JSON Schema)**：一份标准的"说明书"，告诉 AI Agent 它有哪些新能力（例如：`memory_search`），以及该怎么调用（参数是什么）。这使得任何支持 Function Calling 的 Agent (如 OpenAI, Claude, LangChain) 都能直接使用它。
3.  **用户接口 (CLI/Markdown)**：让你（人类）也能手动管理和查看。

---

### 实施计划：构建 `obsidian-memory-agent` Skill

我们将创建一个符合上述定义的通用 Skill。

#### 第一步：构建核心能力 (Core Implementation)
在 `d:\Project\ObsidianMemory\obsidian-memory-agent` 目录下：
*   **`core/zvec_adapter.py`**: 封装 Zvec 的增删改查。我们会做一个"双模"设计：如果检测到环境中有 `zvec` 库则使用高性能模式，否则降级为本地模拟模式（保证在任何环境不报错）。
*   **`core/markdown_manager.py`**: 管理本地 Markdown 文件，确保它们是"人类可读"的唯一真理源 (Single Source of Truth)。

#### 第二步：定义 Agent 接口 (The Interface)
这是让它成为 "Skill" 的关键。我们将创建一个 `tools_schema.json` 和 `tools.py`：
*   **`remember_event(content, importance)`**: 让 Agent 记录重要信息。
    *   *Agent 行为*：写入 `memory/今日.md` -> 向量化 -> 存入 Zvec。
*   **`recall_context(query)`**: 让 Agent 回忆过去。
    *   *Agent 行为*：Zvec 语义搜索 -> 读取 Markdown 上下文 -> 返回给当前对话。
*   **`sync_memory()`**: 手动触发同步。

#### 第三步：标准化输出 (Standardization)
*   **`SKILL.md`**: 编写标准文档，说明如何将此 Skill 注册到不同的 Agent 框架中。
*   **`requirements.txt`**: 列出依赖。

通过这种方式，这个系统既是你个人的知识库管理工具，也是一个标准的、可移植的 **Agent Skill**。
