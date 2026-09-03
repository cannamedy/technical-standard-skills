# Architecture

上层系统读取 Physical Node 的 Manifest，再用 State 判断当前动作是否可执行。`Manifest`、`State` 和 `Action` 保留为协议对象名。

## Design Spine
Discovery and typed actions keep the boundary explicit.

## Runtime
The consumer observes a fresh State, sends an Action, and records the Operation result.
