#!/usr/bin/env python3
'''文本词频统计小工具（数据安全和隐私保护 实验一）。

统计一份纯文本中各英文单词出现的次数，并输出出现频率最高的若干词。

用法示例::

    python code/text_stats.py code/sample.txt
    python code/text_stats.py code/sample.txt --top 15
    python code/text_stats.py code/sample.txt --top 10 --case-sensitive
    python code/text_stats.py code/sample.txt --out result/report.txt
    python code/text_stats.py code/sample.txt --top 15 --chart result/top_words.pdf
'''

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

# 英文单词：以字母开头，允许内部出现连字符或撇号（如 multi-party、don't）
WORD_RE = re.compile(r'[A-Za-z]+(?:[\'\-][A-Za-z]+)*')


def tokenize(text: str, ignore_case: bool = True) -> list[str]:
    '''把文本切分成英文单词序列。

    ignore_case 为真时统一转成小写，使 Data 与 data 合并统计。
    '''
    words = WORD_RE.findall(text)
    if ignore_case:
        return [word.lower() for word in words]
    return words


def count_words(words: list[str]) -> Counter:
    '''统计每个单词出现的次数。'''
    return Counter(words)


def build_report(path: Path, counter: Counter, total: int, top: int) -> str:
    '''把统计结果整理成可以直接打印或保存的文本报告。'''
    columns = ('#', 'word', 'count', 'ratio')
    lines = [
        f'input file     : {path}',
        f'total words    : {total}',
        f'distinct words : {len(counter)}',
        '',
        f'top {top} words by frequency:',
        f'{columns[0]:>3}  {columns[1]:<14}{columns[2]:>7}{columns[3]:>9}',
    ]
    for rank, (word, count) in enumerate(counter.most_common(top), start=1):
        lines.append(f'{rank:>3}  {word:<14}{count:>7}{count / total:>8.2%}')
    return '\n'.join(lines)


def write_report(report: str, out: Path) -> bool:
    '''把文本报告写入 out，父目录不存在时自动创建；失败时提示并返回 False。'''
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report + '\n', encoding='utf-8')
    except OSError as exc:
        print(f'error: cannot write report to {out}: {exc}')
        return False
    return True


def build_chart(path: Path, counter: Counter, top: int, chart: Path) -> bool:
    '''把前 top 个高频词画成横向条形图，并保存为矢量 PDF（无界面 Agg 后端）。'''
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('error: --chart needs matplotlib, install it with: pip install matplotlib')
        return False

    items = counter.most_common(top)
    labels = [word for word, _ in items]
    counts = [count for _, count in items]
    positions = list(range(len(items)))

    fig, ax = plt.subplots(figsize=(8, 0.45 * len(items) + 1.6))
    ax.barh(positions, counts, color='#4c72b0')
    ax.set_yticks(positions)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel('count')
    ax.set_title(f'Top {len(items)} words in {path.name}')
    ax.grid(axis='x', color='0.85', linewidth=0.6)
    ax.set_axisbelow(True)
    for position, count in zip(positions, counts):
        ax.text(count, position, f' {count}', va='center', ha='left', fontsize=8)
    fig.tight_layout()
    try:
        chart.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(chart, format='pdf')
    except OSError as exc:
        print(f'error: cannot write chart to {chart}: {exc}')
        return False
    finally:
        plt.close(fig)
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Count the frequency of English words in a plain text file.')
    parser.add_argument('path', type=Path, help='input text file')
    parser.add_argument('--top', type=int, default=10,
                        help='show the top N words (default: 10)')
    parser.add_argument('--case-sensitive', action='store_true',
                        help='keep word case (default: fold everything to lower case)')
    parser.add_argument('--out', type=Path, metavar='FILE', default=None,
                        help='also write the text report to FILE (parent directories are created)')
    parser.add_argument('--chart', type=Path, metavar='FILE', default=None,
                        help='write a bar chart (PDF) of the top N words to FILE')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.path.is_file():
        print(f'error: file not found: {args.path}')
        return 1

    text = args.path.read_text(encoding='utf-8')
    words = tokenize(text, ignore_case=not args.case_sensitive)
    if not words:
        print('error: no English words found in the input file')
        return 1

    counter = count_words(words)
    report = build_report(args.path, counter, len(words), args.top)
    print(report)

    if args.out is not None and not write_report(report, args.out):
        return 1

    if args.chart is not None and not build_chart(args.path, counter, args.top, args.chart):
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
