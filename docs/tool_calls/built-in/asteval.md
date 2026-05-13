# Asteval

Asteval 是一个用于执行 Python 表达式的工具。它允许你将 Python 表达式作为字符串传递，并在运行时执行它们。
同时，它会检查 AST 并阻止危险调用行为。

注册名：`asteval`

接受一个参数
``` json
{
  "expression": "" // The Python expression to be executed.
}
```

返回执行结果