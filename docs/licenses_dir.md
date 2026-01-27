# Licenses Directory

这个目录存放了该项目所依赖第三方库的许可证文件。

该目录有固定结构以方便程序读取，具体结构如下：

```
LICENSE/
└── {PACKAGE_NAME}/
    ├── LICENSES/
    |   ├── {LICENSE_TYPE}.txt
    |   └── ...
    └── index.md
```

其中：

- `LICENSE/`：根目录
- `{PACKAGE_NAME}`：第三方库的名称
- `LICENSES/`：存放该第三方库的许可证文件
- `{LICENSE_TYPE}`：许可证类型，如 `MIT`、`Apache-2.0` 等
- `index.md`：该第三方库的许可证信息汇总文件，通常是文档的一部分，而不参与程序分析