# Test Agent - Markdown驱动的自动化测试框架

一个基于Markdown的自动化测试Agent，支持PyQt5 UI自动化测试和API测试。

## 特性

- 📝 **Markdown驱动**: 使用Markdown格式编写测试用例，简洁直观
- 🖱️ **UI自动化**: 支持PyQt5应用的自动化操作（点击、输入、拖拽等）
- 🌐 **API测试**: 支持HTTP/REST API调用和验证
- 📊 **多格式报告**: 生成HTML、JSON、Markdown格式的测试报告
- 🔄 **变量传递**: 支持测试步骤间的数据传递
- 📸 **自动截图**: 失败时自动截图，便于问题定位

## 安装

```bash
# 安装依赖
pip install pyyaml requests jinja2 pydantic

# PyQt5（如果测试PyQt5应用）
pip install PyQt5
```

## 快速开始

### 1. 编写测试用例

创建 `test_cases/example_test.md`:

```markdown
# 测试套件示例

## 测试用例 1: 应用启动测试
**ID:** TC001  
**优先级:** P0  
**标签:** smoke, ui

### 测试步骤

#### Step 1: 启动应用
```yaml
action: launch_app
params:
  app: autolabel_gui_pyqt0.3
  timeout: 10
```

#### Step 2: 等待界面加载
```yaml
action: wait
params:
  seconds: 2
```

#### Step 3: 验证主窗口可见
```yaml
action: assert
params:
  type: widget_visible
  widget_type: QMainWindow
  timeout: 5
```

### 清理步骤
```yaml
action: close_app
```
```

### 2. 运行测试

```bash
# 运行测试
python -m test_agent.cli test_cases/example_test.md

# 指定API基础URL
python -m test_agent.cli test_cases/example_test.md --api-base http://localhost:8000

# 只生成HTML报告
python -m test_agent.cli test_cases/example_test.md --format html

# 失败时停止
python -m test_agent.cli test_cases/example_test.md --stop-on-failure

# Dry-run模式（只解析不执行）
python -m test_agent.cli test_cases/example_test.md --dry-run
```

## 支持的Action类型

### UI Actions

| Action | 描述 | 参数 |
|--------|------|------|
| `launch_app` | 启动应用 | `app`: 模块名, `timeout`: 超时时间 |
| `close_app` | 关闭应用 | - |
| `click_widget` | 点击控件 | `widget_type`, `text`, `object_name` |
| `click_menu` | 点击菜单 | `menu`, `item` |
| `mouse_click` | 鼠标点击 | `position`: [x, y], `button`: left/right |
| `mouse_double_click` | 鼠标双击 | `position`: [x, y] |
| `mouse_drag` | 鼠标拖拽 | `start_x`, `start_y`, `end_x`, `end_y` |
| `key_press` | 按键 | `key`: 按键名, `modifier`: 修饰键 |
| `input_text` | 输入文本 | `text`: 文本内容 |
| `file_dialog` | 文件对话框 | `action`: open/save, `file_path` |
| `wait` | 等待 | `seconds`: 秒数 |
| `screenshot` | 截图 | `filename`: 文件名 |

### API Actions

| Action | 描述 | 参数 |
|--------|------|------|
| `api_call` | API调用 | `endpoint`, `method`, `body`, `headers` |
| `api_upload` | 文件上传 | `endpoint`, `file_path`, `field_name` |
| `api_download` | 文件下载 | `endpoint`, `save_path` |

### Assert Actions

| Action | 描述 | 参数 |
|--------|------|------|
| `assert` | 断言 | `type`: 断言类型 |

#### 支持的断言类型

- `widget_visible`: 控件可见
- `widget_enabled`: 控件启用
- `widget_text`: 控件文本匹配
- `widget_count`: 控件数量
- `api_status`: API状态码
- `api_response`: API响应内容
- `variable_equals`: 变量等于
- `variable_contains`: 变量包含

## 测试用例格式

### 基本结构

```markdown
# 测试套件标题

## 测试用例 N: 用例名称
**ID:** TCXXX  
**优先级:** P0/P1/P2/P3  
**标签:** tag1, tag2

### 前置条件
- 条件1
- 条件2

### 测试步骤

#### Step N: 步骤名称
```yaml
action: action_name
params:
  param1: value1
  param2: value2
```

### 预期结果
- 结果1
- 结果2

### 清理步骤
```yaml
action: close_app
```

---
```

### 变量引用

支持在参数中使用 `{{variable}}` 引用上下文变量:

```yaml
action: api_call
params:
  endpoint: /api/users/{{user_id}}
  method: GET
```

### 上下文变量

- `last_api_response`: 最后一次API调用的响应
- 自定义变量通过 `data` 返回

## 命令行参数

```
usage: test-agent [-h] [--api-base API_BASE] [--output-dir OUTPUT_DIR]
                  [--format {html,json,markdown,all}] [--stop-on-failure]
                  [--title TITLE] [--dry-run] [--version]
                  test_file

Markdown驱动的自动化测试Agent

positional arguments:
  test_file             Markdown测试用例文件路径

optional arguments:
  -h, --help            显示帮助信息
  --api-base API_BASE   API基础URL (默认: http://localhost:8000)
  --output-dir OUTPUT_DIR
                        报告输出目录 (默认: test_reports)
  --format {html,json,markdown,all}
                        报告格式 (默认: all)
  --stop-on-failure     失败时停止执行后续用例
  --title TITLE         报告标题
  --dry-run             只解析测试用例，不执行
  --version             显示版本
```

## 项目结构

```
test_agent/
├── __init__.py
├── cli.py                 # 命令行入口
├── parser/                # Markdown解析模块
│   ├── __init__.py
│   ├── markdown_parser.py
│   └── test_schema.py
├── executor/              # 测试执行模块
│   ├── __init__.py
│   ├── test_executor.py
│   ├── ui_driver.py
│   └── api_client.py
├── actions/               # 动作实现
│   ├── __init__.py
│   ├── base_action.py
│   ├── ui_actions.py
│   ├── api_actions.py
│   └── assert_actions.py
└── reporter/              # 报告生成模块
    ├── __init__.py
    └── report_generator.py
```

## 示例

### UI测试示例

```markdown
#### Step 1: 点击按钮
```yaml
action: click_widget
params:
  widget_type: QPushButton
  text: "确定"
  timeout: 5
```

#### Step 2: 输入文本
```yaml
action: input_text
params:
  text: "Hello World"
  widget_type: QLineEdit
```

#### Step 3: 验证结果
```yaml
action: assert
params:
  type: widget_text
  widget_type: QLabel
  expected: "操作成功"
```
```

### API测试示例

```markdown
#### Step 1: 调用API
```yaml
action: api_call
params:
  endpoint: /api/login
  method: POST
  body:
    username: "admin"
    password: "password"
```

#### Step 2: 验证状态码
```yaml
action: assert
params:
  type: api_status
  expected: 200
```

#### Step 3: 验证响应内容
```yaml
action: assert
params:
  type: api_response
  path: "data.token"
  expected: "{{token}}"
  operator: contains
```
```

## 扩展开发

### 自定义Action

```python
from test_agent.actions import BaseAction, ActionResult

class CustomAction(BaseAction):
    def validate_params(self) -> bool:
        return 'required_param' in self.params
    
    def execute(self) -> ActionResult:
        # 实现自定义逻辑
        return self.success_result("执行成功")

# 注册Action
executor.register_action("custom", CustomAction)
```

## 许可证

MIT License
