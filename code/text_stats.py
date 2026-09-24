#!/usr/bin/env python3
'''文本词频统计小工具（数据安全和隐私保护 实验一）。

统计一份纯文本中各英文单词出现的次数，并输出出现频率最高的若干词。

用法示例::

    python code/text_stats.py code/sample.txt
    python code/text_stats.py code/sample.txt --top 15
    python code/text_stats.py code/sample.txt --top 10 --case-sensitive
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Count the frequency of English words in a plain text file.')
    parser.add_argument('path', type=Path, help='input text file')
    parser.add_argument('--top', type=int, default=10,
                        help='show the top N words (default: 10)')
    parser.add_argument('--case-sensitive', action='store_true',
                        help='keep word case (default: fold everything to lower case)')
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
    print(build_report(args.path, counter, len(words), args.top))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
