# 运行结果说明

## 生成命令

```bash
python code/text_stats.py code/sample.txt --top 12 \
    --out result/word_freq_report.txt \
    --chart result/word_freq_top12.pdf
```

## 文件说明

| 文件 | 说明 |
| --- | --- |
| `word_freq_report.txt` | 程序打印到终端的文本报告，内容与终端输出逐字一致 |
| `word_freq_top12.pdf` | 前 12 个高频词的横向条形图，矢量 PDF（无位图对象，可无损缩放） |

## 结果解读

- 语料共 257 个词（tokens），其中不重复的词 122 个（types），
  类型/词数比约为 0.47，说明短文用词重复率不高。
- 排名前三位是 `a`(18)、`data`(16)、`and`(12)。它们占比较高一方面是因为
  英文冠词、连词本身出现频繁，另一方面说明语料主题集中在 data 上。
- 去掉 `a`/`and`/`the`/`in`/`that` 这类虚词后，实义词排名为
  `data`(16)、`user`(8)、`privacy`(7)、`private`(5)、`system`(5)、
  `security`(4)，与语料“数据安全与隐私保护”的主题一致。
- 程序默认会把 `Data` 与 `data` 合并统计（折叠大小写），
  需要严格区分大小写时加 `--case-sensitive`。
