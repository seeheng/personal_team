# Code Execution Skill

## Skill Metadata
```yaml
name: code-execution
version: 1.0.0
description: Executes Python code and manages scripts for the personal assistant
agent: personal-assistant
category: development
status: active
```

## Overview
This skill enables the personal assistant agent to:
- Execute Python code snippets and scripts
- Manage and organize scripts in the scripts folder
- Handle code dependencies and environments
- Capture and display execution output
- Debug and troubleshoot code issues
- Generate and run automated scripts

## Capabilities

### Core Features
- **Script Execution**: Run Python scripts with proper error handling
- **Code Evaluation**: Execute code snippets in isolated environments
- **Script Management**: Create, organize, and version control scripts
- **Output Capture**: Capture stdout, stderr, and return values
- **Environment Management**: Handle virtual environments and dependencies
- **Debugging**: Provide detailed error messages and stack traces
- **Scheduling**: Schedule scripts to run at specific times

### Supported Code Types
- Python 3.8+
- Inline scripts
- Script files
- Notebooks/Jupyter code cells
- Shell commands

## Key Methods

### Execution
- `execute_code(code, language='python', timeout=30)`
- `execute_script(script_path, args=None, timeout=30)`
- `execute_async(code, callback)`
- `execute_in_environment(code, env_name)`

### Script Management
- `create_script(name, code, description)`
- `list_scripts(category=None)`
- `get_script(script_name)`
- `update_script(script_name, code)`
- `delete_script(script_name)`
- `organize_scripts(category, subcategory)`

### Environment
- `list_environments()`
- `create_environment(env_name, python_version)`
- `install_package(package_name, env_name)`
- `list_installed_packages(env_name)`
- `activate_environment(env_name)`

### Output & Debugging
- `capture_output(script_path)`
- `get_execution_history(script_name, limit=10)`
- `debug_script(script_path, breakpoints)`
- `profile_code(code)` # Performance profiling
- `lint_code(code)` # Code quality checks

## Integration Examples

### Usage in Agent
```python
# Execute Python code
result = agent.use_skill("code-execution", "execute_code", {
    "code": """
import json
data = {'name': 'John', 'age': 30}
print(json.dumps(data, indent=2))
""",
    "language": "python"
})

# Run a script
output = agent.use_skill("code-execution", "execute_script", {
    "script_path": "./scripts/analyze_handwriting.py",
    "args": ["--input", "sample.jpg", "--verbose"]
})

# Create and execute a new script
agent.use_skill("code-execution", "create_script", {
    "name": "process_samples",
    "code": "from skills.handwriting_recognition import HandwritingRecognizer\n...",
    "description": "Process handwriting samples for training"
})

# List organized scripts
scripts = agent.use_skill("code-execution", "list_scripts", {
    "category": "handwriting"
})
```

## Script Organization

Scripts are automatically organized:
```
./scripts/
├── handwriting_recognition/
│   ├── __init__.py
│   ├── recognizer.py
│   ├── trainer.py
│   └── utils.py
├── task_management/
├── data_processing/
└── utilities/
```

## Error Handling

```python
# Execution with error handling
result = agent.use_skill("code-execution", "execute_code", {
    "code": code_string,
    "timeout": 30,
    "handle_errors": True
})

if result["status"] == "error":
    print(f"Error: {result['error_message']}")
    print(f"Line: {result['error_line']}")
    print(f"Traceback: {result['traceback']}")
```

## Performance Features

### Async Execution
```python
def on_complete(result):
    print(f"Script completed: {result}")

agent.use_skill("code-execution", "execute_async", {
    "code": long_running_code,
    "callback": on_complete
})
```

### Code Profiling
```python
profile = agent.use_skill("code-execution", "profile_code", {
    "code": code_to_profile
})
# Returns: execution time, memory usage, function calls
```

### Code Quality
```python
quality = agent.use_skill("code-execution", "lint_code", {
    "code": code_to_check
})
# Returns: style violations, unused variables, complexity metrics
```

## Output Format

```json
{
  "status": "success",
  "output": "Script output here",
  "return_value": null,
  "execution_time": 1.234,
  "memory_used": 42.5,
  "errors": [],
  "warnings": []
}
```

## Advanced Features

### Dependencies
Automatically detect and install required packages:
```python
result = agent.use_skill("code-execution", "execute_script", {
    "script_path": "./scripts/analyze.py",
    "auto_install_deps": True  # Auto-install from requirements.txt
})
```

### Environment Isolation
Run code in isolated environments:
```python
result = agent.use_skill("code-execution", "execute_in_environment", {
    "env_name": "ml-env",
    "code": "import tensorflow as tf; ..."
})
```

### Scheduling
Schedule scripts for later execution:
```python
agent.use_skill("code-execution", "schedule_script", {
    "script_path": "./scripts/daily_task.py",
    "schedule": "daily",
    "time": "09:00"
})
```

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: March 6, 2026
