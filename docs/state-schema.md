# 状态与事件 schema（面向模型）

每执行一个操作，返回一个 `StepResult`：本回合发生的**事件**加上**终点状态**。
设计原则：**模型看到的就是人在屏幕上看到的**，不多也不少。

## 1. 两种视图

| 视图 | 用途 | 内容 |
|---|---|---|
| `perceptual`（默认） | 给模型 | 只含人能看到的东西：没有对象编号、不含 HIDE 对象、看不出朝向的对象不给朝向 |
| `full` | 求解器、判等、调试、差分测试 | 引擎完整状态：对象编号、对象列表顺序、全部朝向、隐藏对象、标志位 |

两个状态是否“相同”只按 `full` 判断。`perceptual` 相同不代表状态相同，例如原地重生、看不见的朝向，都会影响之后的走法。

## 2. 坐标

- 只描述可活动区域，不含关卡外框。`size = [w, h]`。
- `pos = [x, y]`，从 0 开始，x 向右，y 向下。

## 3. 规则显示开关 `rules`

| 取值 | 文字方块显示 | 额外提供 |
|---|---|---|
| `none` | 只有单词和位置 | 无。模型自己拼规则，也自己判断哪些在生效 |
| `lit`（默认） | 加 `state`：`lit` 亮（组成生效规则）/ `dim` 暗 / `crossed` 被划掉（规则被 NOT 否定） | 无。和玩家在游戏里看到的一致 |
| `list` | 同 `lit` | 加 `rules`：当前生效的规则列表 |

`list` 默认不列游戏内置的隐含规则（TEXT IS PUSH、LEVEL IS STOP 等）；`base_rules: true` 时才列出。

## 4. 终点状态 `State`

```jsonc
{
  "turn": 12,
  "status": "playing",          // playing | won | infinite_loop
  "size": [24, 14],
  "objects": [                  // 按 (y, x, 绘制顺序) 排序；同一格里先下后上
    {"kind": "object", "name": "baba", "pos": [3, 5], "facing": "right"},
    {"kind": "object", "name": "rock", "pos": [6, 5]},
    {"kind": "object", "name": "rock", "pos": [6, 5], "color": "red"},
    {"kind": "text",   "word": "baba", "class": "noun",     "pos": [1, 1], "state": "lit"},
    {"kind": "text",   "word": "is",   "class": "verb",     "pos": [2, 1], "state": "lit"},
    {"kind": "text",   "word": "you",  "class": "property", "pos": [3, 1], "state": "lit"},
    {"kind": "letter", "letter": "b",  "pos": [9, 9]}
  ],
  "rules": [                    // 仅 rules=list
    {"text": "BABA IS YOU", "tiles": [[1, 1], [2, 1], [3, 1]]}
  ]
}
```

字段规则：

- **对象 `object`**：
  - `facing` 只出现在贴图能看出朝向的对象上：角色类（baba、keke、me…）、有方向的贴图（手、骷髅、鱼…）、带方向的动画（传送带等）。石头、墙、旗子这类看不出朝向的没有这个字段，虽然引擎内部有朝向。
  - `color` 只在颜色和默认不同时出现，比如被 `BABA IS RED` 改过。
  - 被 HIDE 的对象不出现。
- **文字 `text`**：
  - `class` 取值：`noun` / `verb` / `property` / `condition` / `prefix` / `not` / `and`。游戏里不同词类的文字方块外观本来就不同，所以属于可见信息。
  - `state` 只在 `rules` 为 `lit` 或 `list` 时出现。
- **字母 `letter`**：用来拼词的单个字母方块。
- **叠放**：同一格可以有多个对象，逐个列出，不合并。两块相同的石头叠在一起时出现两条，人能从游戏里叠放的样子看出来。

## 5. 事件 `Event`

事件**不用编号**，用“在哪个位置的什么东西”来指代：

```jsonc
// Ref：事件发生时这个东西的样子和位置
{"kind": "object", "name": "rock", "pos": [5, 5]}
{"kind": "text",   "word": "win",  "pos": [6, 3]}
```

每个事件带 `phase`（从 1 开始）：同一个 phase 里的事件同时发生，phase 越大越晚。phase 顺序就是引擎结算的顺序，渲染器也按它安排中间帧。

| `type` | 字段 | 说明 |
|---|---|---|
| `move` | `what`, `from`, `to` | 一次移动。一回合里同一个东西移动多次，就有多条 `move`。FALL 一次滑多格也是一条 |
| `teleport` | `what`, `from`, `to` | TELE 的瞬移，和走路在视觉上不同，单列 |
| `turn` | `what`, `from`, `to` | 朝向变化，只对看得出朝向的对象出现 |
| `destroy` | `what` | 被消灭，游戏里会有消散效果 |
| `create` | `what` | 新出现（HAS、MAKE、MORE 等） |
| `transform` | `pos`, `from`, `to` | 原地变形，`from` 和 `to` 是不带 `pos` 的外观描述 |
| `hide` / `reveal` | `what` | 被 HIDE 隐藏或重新显示 |
| `recolor` | `what`, `from`, `to` | 颜色改变 |
| `text_state` | `what`, `from`, `to` | 文字亮、暗、划掉的变化，仅 `rules` 为 `lit` 或 `list` |
| `rule_on` / `rule_off` | `rule` | 规则成立或失效，仅 `rules=list` |
| `win` | — | 胜利 |
| `infinite_loop` | — | 规则造成死循环，关卡被摧毁 |

可选开关 `causes`（默认关）：给 `move`、`destroy`、`create`、`transform` 加上 `cause`，例如 `push`、`sink`、`defeat`、`melt`、`open_shut`、`weak`、`eat`、`has`、`make`。默认不给，因为玩家看到的是“发生了什么”，“为什么”要自己推断。

## 6. 一步的返回值 `StepResult`

```jsonc
{
  "action": "right",            // up | down | left | right | wait（另有 undo、restart）
  "events": [
    {"phase": 1, "type": "move", "what": {"kind": "object", "name": "baba", "pos": [4, 5]}, "from": [4, 5], "to": [5, 5]},
    {"phase": 1, "type": "move", "what": {"kind": "object", "name": "rock", "pos": [5, 5]}, "from": [5, 5], "to": [6, 5]},
    {"phase": 3, "type": "destroy", "what": {"kind": "object", "name": "rock",  "pos": [6, 5]}},
    {"phase": 3, "type": "destroy", "what": {"kind": "object", "name": "water", "pos": [6, 5]}}
  ],
  "state": { /* 终点 State */ }
}
```

- `events` 为空：这一步什么都没发生，比如撞墙，而且撞墙的对象看不出朝向。
- 起点和终点外观完全一样，但 `events` 不为空，比如原地重生：文本格式里会额外写一句“终点与起点外观相同”。

## 7. 文本格式（给大模型读）

由上面的 JSON 直接生成，内容一一对应：

```
第 12 回合 · 进行中 · 场地 24×14（x 0–23 向右，y 0–13 向下）
物体：
  baba  (3,5) 朝右
  rock  (6,5) (7,5)
  wall  (0–23,0) (0,1–12) (23,1–12) (0–23,13)
文字（亮：组成生效规则 / 暗：未组成 / 划掉：被否定）：
  BABA (1,1) 亮 · IS (2,1) 亮 · YOU (3,1) 亮
  ROCK (10,2) 暗 · IS (11,2) 暗 · WIN (12,4) 暗

本回合（→）：
  1. baba (4,5)→(5,5)；rock (5,5)→(6,5)
  2. (6,5) 的 rock 和 water 一起消失
```

- 同名对象合并成一行，连续的坐标压缩成范围，比如墙。
- 可选附加一张带坐标轴的字符网格，作为辅助视图。

## 8. 纯图像模式（`obs="image"`）

完全不给文字状态，只给渲染图：起点、中间动画帧、终点。画面就是信息的全部，和人玩游戏时看到的一样。

### 返回值

```jsonc
{
  "action": "right",
  "frames": [                      // 按时间排序；t ∈ [0, 1]
    {"t": 0.0,  "image": "<PNG>"},  // 起点
    {"t": 0.25, "image": "<PNG>"},
    {"t": 0.5,  "image": "<PNG>"},
    {"t": 0.75, "image": "<PNG>"},
    {"t": 1.0,  "image": "<PNG>"}   // 终点
  ]
}
```

发给模型时就是一串图片；默认不加任何说明文字，只保证按时间顺序排列。模型自己选的动作它本来就知道，所以不另外告诉它。

### 取帧方式 `frames`

| 取值 | 帧 | 用途 |
|---|---|---|
| `endpoints` | 只有起点和终点 | 最省；但起点终点一样时，看不出中间发生了什么 |
| `phases`（默认） | 起点、每个阶段的中点和结束点、终点 | 每个阶段至少有一张图，原地重生这类“前后一样”的变化也能看到 |
| 整数 `n` | 在 [0,1] 上均匀取 n 帧 | 固定帧数，便于批量训练 |
| `video` | GIF 或 MP4 | 给能读视频的模型 |

- **阶段依次播放**：在图像模式下，回合里各阶段按先后顺序依次展开在时间轴上，每个阶段占一段。这样“先被推进水里、再一起沉下去”“先碎掉、再原地重新出现”都能在画面上分开看到。
- **无事发生**：仍然按同样的方式取帧，所有帧都一样，由模型自己看出来。`dedupe: true` 时只返回一张。

### 画面里包含什么

- 只画人能看到的东西，取舍和 `perceptual` 视图一致：被 HIDE 的对象不画；朝向画在本来就有朝向的贴图上；颜色按规则改变后的颜色画。
- 文字方块直接写单词，不同词类用不同外观区分。
- `rules` 开关在图像里的效果：
  - `none`：所有文字一样亮。
  - `lit`：生效规则的文字亮，未生效的暗，被否定的打叉。
  - `list`：在地图旁边加一栏，列出当前规则。
- 胜利、死循环有明显的画面提示，例如整屏特效，不用文字说明。
- 中间帧：移动的对象画在两格之间，消失的逐渐变淡，新出现的逐渐显现，变形的从旧样子过渡到新样子，插值是平滑的。

### 可选项（默认关）

- `axes`：在图边上画坐标刻度，方便模型说出具体位置。
- `motion_hints`：在中间帧上画运动轨迹或箭头。
- `tile_px`：每格的像素数，默认 32，保证文字方块上的单词看得清。
- 图像格式：PNG，同一状态每次渲染结果完全一样，可以复现。

### 和文本模式的关系

两种模式来自同一份事件记录和终点状态，只是输出方式不同。也可以同时打开：图像加文本，或图像加 `rules=list`，用来做消融实验，比较模型在不同信息量下的表现。

## 9. 一次提交多个操作

引擎的基本单位始终是一步 `step(state, action)`；一次多个操作只是接口层依次执行再合并结果。

### 协议参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `max_actions_per_call` | 32 | `1` = 严格闭环；`N` = 一次最多 N 步；`null` = 不限（一次交完整解法） |
| `stop_on` | `["win", "infinite_loop"]` | 遇到这些情况提前停，后面的操作不执行。可选再加 `rule_change`、`no_you`、`no_op` |

`undo` 和 `restart` 也可以写在序列里，`undo` 一次撤一步；另提供 `undo(n)`。

### 返回值

```jsonc
{
  "actions": ["right", "right", "up"],
  "executed": 3,                 // 实际执行了几步；提前停时小于 actions 的长度
  "stopped_by": null,            // 或 "win" 等
  "steps": [                     // 每一步的事件；文本模式
    {"action": "right", "events": [ /* … */ ]},
    {"action": "right", "events": []},
    {"action": "up",    "events": [ /* … */ ]}
  ],
  "state": { /* 只给最后的终点状态 */ }
}
```

- 图像模式默认给每一步结束时的一张图，共 `executed + 1` 张，不含步内的中间动画；`per_step: "phases"` 时每一步再展开中间帧，`video` 时整段输出成一个视频。

### 评测统计

调用次数和实际执行步数分开记录。

## 10. 实现状态（2026-11-19）

已实现（`babasim.api.Game`、`babasim.text`、`babasim.render.Renderer`、`python -m babasim`）：

- 两种视图、`rules` 三档、`base_rules`、State、StepResult、多步 `play`（`stop_on` 含 `rule_change` / `no_you` / `no_op`）、`undo(n)`、`restart`。
- 事件：`move`、`teleport`、`turn`、`destroy`、`create`、`transform`、`text_state`、`rule_on`、`rule_off`、`win`、`infinite_loop`，另有 `too_complex`、`destroyed`（关卡被 LEVEL IS WEAK 等摧毁）。事件来自引擎自己的撤销记录，phase 按结算阶段划分；同一阶段里同一个东西再次变化时另起一个 phase。
- `undo` / `restart` 的事件是前后状态的差，只有一个 phase。
- 文本格式和字符网格。
- 图像：任意时刻 `frame(t)`、`frames("endpoints" | "phases" | n)`、`dedupe`、GIF、`axes`、`motion_hints`、`tile_px`、规则栏、胜利和摧毁的边框提示。

还没实现：

- `color` 字段和 `recolor`、`hide`、`reveal` 事件（被 HIDE 的对象已经不出现在感知视图里，但隐藏和显示的瞬间没有事件）。
- `causes` 开关。
- MP4 输出；`play` 里按步出图需要调用方在每步后自己取帧。
- 朝向为 4（无朝向）的对象在完整视图里记为 `none`。
