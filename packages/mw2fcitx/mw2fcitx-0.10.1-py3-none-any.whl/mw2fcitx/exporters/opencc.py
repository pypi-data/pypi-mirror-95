import re
from pypinyin import lazy_pinyin
import opencc
from mw2fcitx.utils import console
from mw2fcitx.utils import manual_fix


def export(words):
    result = ""
    converter = opencc.OpenCC('t2s.json')
    HANZI_RE = re.compile('^[\u4e00-\u9fa5]+$')
    count = 0
    last_word = None
    for line in words:
        line = line.rstrip("\n")
        if not HANZI_RE.match(line):
            continue

        # Skip single character & too long pages
        if len(line) <= 1:
            continue

        # Skip list pages
        if line.endswith(('列表', '对照表')):
            continue

        if last_word and len(last_word) >= 4 and line.startswith(last_word):
            continue

        pinyin = "'".join(lazy_pinyin(line))
        if pinyin == line:
            # print("Failed to convert, ignoring:", pinyin, file=sys.stderr)
            continue

        if manual_fix(line):
            pinyin = manual_fix(line)
            console.debug(f"Fixing {line} to {pinyin}")

        last_word = line

        result += "\t".join((converter.convert(line), pinyin, "0"))
        result += "\n"
        count += 1
        if count % 1000 == 0:
            console.debug(str(count) + " converted")

    if count % 1000 != 0 or count == 0:
        console.debug(str(count) + " converted")
    return result
