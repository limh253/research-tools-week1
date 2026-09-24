# research-tools-week1

数据安全和隐私保护 课程 第一次实验《实验基础工具使用》的代码与实验报告仓库。

本仓库用于练习科研过程中的基础工具链：

- **Git / GitHub**：工作区 -> 暂存区 -> 本地仓库 -> 远程仓库的完整流程（创建、克隆、提交、上传、更新）。
- **LaTeX**：使用 `figures/` 统一存放插图，用 `\includegraphics` 插入图片，用 `\caption` + `\label` + `\ref` 建立图题与正文引用。
- **Codex + CC Switch**：AI 辅助编程工具的安装配置、供应商切换，以及「阅读 -> 修改 -> 复核」的可靠使用流程。

## 目录结构

```
research-tools-week1/
├── README.md          仓库说明
├── code/              可运行的程序
│   ├── text_stats.py  文本词频统计程序
│   └── sample.txt     程序输入样例（英文文本）
├── result/            程序的运行结果
└── report/            LaTeX 实验报告（main.tex 及插图）
```

## 运行方法

要求 Python 3.9 及以上版本，基础功能只依赖标准库。

```bash
# 统计 sample.txt 中出现次数最多的 10 个单词
python code/text_stats.py code/sample.txt --top 10
```

## 实验报告

报告源码位于 `report/main.tex`，使用 XeLaTeX 编译（`ctexart` 文档类，中文支持）。
本机未安装 LaTeX 发行版，报告在 TexPage / Overleaf 在线编译。

## 作者

李明昊（24347051），中山大学网络空间安全学院，2026 年 9 月。
