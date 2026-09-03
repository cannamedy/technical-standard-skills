# Architecture

机器人报告当前位置，但相机看到的位置和控制器报告的位置可能不同。上层必须知道哪一个来源负责声明 `current_pose`，这就是 State Authority。

## Runtime
The authority is checked before the action.
