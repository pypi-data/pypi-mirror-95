# This collation file is for moegirl.org.
# It MIGHT NOT be fit for other wikis.
from ..utils import normalize


def dont_have(string: str, array: [str]):
    for i in array:
        if string.find(i) != -1:
            return False
    return True


def split_and_merge_single(group: [str], spliter: str):
    ret = []
    for i in group:
        for j in i.split(spliter):
            ret.append(j)
    return ret


def tweak_remove_char(char):

    def cb(words):
        return list(map(lambda x: x.replace(char, ""), words))

    return cb


def tweak_len_more_than(length):

    def cb(words):
        return list(filter(lambda x: len(x) > length, words))

    return cb


def tweak_remove_word_includes(items):

    def cb(words):
        return list(filter(lambda x: dont_have(x, items), words))

    return cb


def tweak_split_word_with(spliters):

    def cb(items: [str]):
        ret = items
        for i in spliters:
            tmp = []
            for j in split_and_merge_single(ret, i):
                tmp.append(j)
            ret = tmp
        return ret

    return cb


def tweak_trim_suffix(suffixes):
    def cb(items: [str]):
        ret = []
        for i in items:
            for j in suffixes:
                i = i.removesuffix(j)
            ret.append(i)
        return ret

    return cb


def tweak_remove_regex(regexes):
    from re import compile
    compiled_regexes = list(map(compile, regexes))

    def cb(items: [str]):
        ret = items

        for rgx in compiled_regexes:
            ret = filter(
                lambda x, rgx=rgx: not rgx.match(x), ret
            )
        return list(ret)

    return cb


def tweak_normalize(words):
    ret = []
    for i in words:
        ret.append(normalize(i))
    return ret


tweaks = [
    tweak_remove_word_includes(["○", "〇"]),
    tweak_split_word_with(
        [":", "/", "(", ")", "（", "）", "【", "】", "『", "』", "／", " ", "!", "！"]),
    tweak_len_more_than(1),
    tweak_remove_char("·"),
    tweak_trim_suffix(["系列", "列表", "对照表"]),
    tweak_remove_regex([
        "^第.*(次|话)$"
    ]),
    tweak_normalize
]
