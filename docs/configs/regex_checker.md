# REGEX CHECKER 配置文件

## 语法

```re
[REGEX PARALLEL FILE]
.*example.*
```
PS: 首行必须是`[REGEX PARALLEL FILE]`或`[REGEX SERIES FILE]`
表示该文件是`并行`还是`串行`匹配
`并行`匹配的文件，正则表达式之间是`或`关系，只要有一个匹配成功，就返回匹配结果
`串行`匹配的文件，正则表达式之间是`与`关系，只有所有正则表达式都匹配成功，才返回匹配结果
之后每行都是一个`正则表达式`
后面的所有表达式使用的都是search模式和findall模式
具体看项目如何使用接口

如果没有任何想要的规则
就至少需要填写文件头
```re
[REGEX SERIES FILE]
```
这样后面由于没有任何规则
在`并行`模式下，会返回一个 True Like Result
在`串行`模式下，会返回一个 False Like Result