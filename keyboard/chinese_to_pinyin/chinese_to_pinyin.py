#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

"""
汉字->拼音, 汉字的简繁转换
学习github: https://github.com/letiantian/ChineseTone
            https://github.com/overtrue/pinyin
"""

import os
from collections import namedtuple

__all__ = ("convert_to_str", "PinyinResource", "PinyinHelper", "ChineseHelper")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chinese_to_pinyin_data')

# 值     类型             含义
# 1  WITH_TONE_MARK   带声调的拼音
# 2  WITHOUT_TONE     无声调的拼音
# 3  WITH_TONE_NUMBER 将声调转换为1~4, 紧跟在拼音后
PinyinFormat = namedtuple('PinyinFormat', ['WITH_TONE_MARK', 'WITHOUT_TONE', 'WITH_TONE_NUMBER'])(1, 2, 3)


def convert_to_str(v) -> str:
    if isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    if isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))


class PinyinResource(object):
    PHRASE_MAX_LEN = 1

    @classmethod
    def __read(cls, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        for line in open(file_path, encoding='utf8'):
            line = convert_to_str(line.strip())
            if '=' not in line:
                continue
            yield line

    @classmethod
    def get_pinyin_resource(cls) -> dict:
        """
        :return: dict, k=单个汉字; v=可能的拼音(小写), list
        """
        resource = {}
        path = os.path.join(DATA_DIR, 'pinyin.db')
        for line in cls.__read(path):
            hanzi, pinyins = line.split('=')
            pinyins = pinyins.lower()
            resource[hanzi] = pinyins.split(',')
        return resource

    @classmethod
    def get_phrase_pinyin_resource(cls) -> dict:
        """
        :return: dict, k=词组; v=对应的拼音(小写), list
        """
        resource = {}
        wordFiles = ['mutil_pinyin.db', 'phrase.db']
        wordFiles = [os.path.join(DATA_DIR, i) for i in wordFiles]

        for path in wordFiles:
            for line in cls.__read(path):
                line = convert_to_str(line.strip())
                word, pinyins = line.split('=')
                pinyins = pinyins.lower()
                resource[word] = pinyins.split(',')
                cls.PHRASE_MAX_LEN = max(cls.PHRASE_MAX_LEN, len(word))
        return resource

    @classmethod
    def get_chinese_resource(cls)->(dict, dict):
        """
        读取简->繁体转换文件
        :return: dict(k=繁体, v=简体), dict(k=简体, v=繁体)
        """
        fan2jian = {}
        jian2fan = {}
        path = os.path.join(DATA_DIR, 'chinese.db')
        for line in cls .__read(path):
            traditional, simplified = line.split('=')
            fan2jian[traditional] = simplified
            jian2fan[simplified] = traditional
        return fan2jian, jian2fan


class PinyinException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class PinyinHelper(object):
    """ 汉字->拼音 """
    __inited = False

    # dict 汉字->拼音(list)
    PINYIN_TABLE = {}
    # dict 词组->拼音
    PHRASE_PINYIN_TABLE = {}

    # marked: 标注的
    # vowel:  元音
    # 未标注声调的元音
    ALL_UNMARKED_VOWEL = "aeiouv"
    # 标注声调的元音
    ALL_MARKED_VOWEL = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
    # 标注声调的元音-> 未标注声调的元音
    MARKED_VOWEL_TO_UNMARKED = {
        'ā': 'a',
        'á': 'a',
        'ǎ': 'a',
        'à': 'a',
        'ē': 'e',
        'é': 'e',
        'ě': 'e',
        'è': 'e',
        'ī': 'i',
        'í': 'i',
        'ǐ': 'i',
        'ì': 'i',
        'ō': 'o',
        'ó': 'o',
        'ǒ': 'o',
        'ò': 'o',
        'ū': 'u',
        'ú': 'u',
        'ǔ': 'u',
        'ù': 'u',
        'ü': 'v',
        'ǖ': 'v',
        'ǘ': 'v',
        'ǚ': 'v',
        'ǜ': 'v',
        'ń': 'n',
        'ň': 'n',
        '': 'm',
    }

    # 声调范围 1->4
    MARKED_VOWEL_TO_TONE_NUMBER = {
        'ā': '1',
        'á': '2',
        'ǎ': '3',
        'à': '4',
        'ē': '1',
        'é': '2',
        'ě': '3',
        'è': '4',
        'ī': '1',
        'í': '2',
        'ǐ': '3',
        'ì': '4',
        'ō': '1',
        'ó': '2',
        'ǒ': '3',
        'ò': '4',
        'ū': '1',
        'ú': '2',
        'ǔ': '3',
        'ù': '4',
        'ǖ': '1',
        'ǘ': '2',
        'ǚ': '3',
        'ǜ': '4',
        'ń': '2',
        'ň': '3',
    }

    SHENGMU = ('b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x', 'zh', 'ch', 'sh', 'r', 'z', 'c',
               's')
    SHENGMU = set(SHENGMU)

    @classmethod
    def init(cls, reload=False):
        if not cls.__inited or reload:
            cls.PINYIN_TABLE = PinyinResource.get_pinyin_resource()
            cls.PHRASE_PINYIN_TABLE = PinyinResource.get_phrase_pinyin_resource()
            cls.__inited = True

    @classmethod
    def convert_with_tone_number(cls, pinyin) -> str:
        """
        将带声调格式的拼音转换为数字代表声调格式的拼音, 如hà -> ha4
        :param pinyin: 带声调的拼音
        :return: 将声调转换为对应的数字
        """
        pinyin = convert_to_str(pinyin)
        pinyin = pinyin.replace('ü', 'v')
        ans = ''
        for c in pinyin:
            if c in cls.MARKED_VOWEL_TO_UNMARKED:
                ans += cls.MARKED_VOWEL_TO_UNMARKED[c]
                ans += cls.MARKED_VOWEL_TO_TONE_NUMBER[c]
            else:
                ans += c
        return ans

    @classmethod
    def convert_with_tone(cls, pinyin) -> str:
        """
        将带声调格式的拼音转换为不带声调的拼音, 如hà -> ha
        :param pinyin: 带声调的拼音
        :return: 不带声调的拼音
        """
        pinyin = convert_to_str(pinyin)
        pinyin = pinyin.replace('ü', 'v')
        return ''.join([cls.MARKED_VOWEL_TO_UNMARKED.get(c, c) for c in pinyin])

    @classmethod
    def format_pinyin(cls, pinyin, pinyinFormat=PinyinFormat.WITHOUT_TONE) -> str:
        """
        将带声调的拼音格式化为相应格式的拼音
        :param pinyin:        拼音
        :param pinyinFormat:  拼音格式
               1  WITH_TONE_MARK   带声调的拼音
               2  WITHOUT_TONE     无声调的拼音
               3  WITH_TONE_NUMBER 将声调转换为1~4, 紧跟在拼音后
        :return: 转化后的拼音
        """
        pinyin = convert_to_str(pinyin)
        if pinyinFormat == PinyinFormat.WITH_TONE_MARK:
            return pinyin
        if pinyinFormat == PinyinFormat.WITH_TONE_NUMBER:
            return cls.convert_with_tone_number(pinyin)
        if pinyinFormat == PinyinFormat.WITHOUT_TONE:
            return cls.convert_with_tone(pinyin)
        return pinyin

    @classmethod
    def convert_to_pinyin_from_char(cls, chinese_char, pinyinFormat=PinyinFormat.WITHOUT_TONE) -> str:
        """
        将单个汉字转化为对应的拼音
        :param chinese_char:  单个汉字
        :param pinyinFormat:  返回的拼音格式
               1  WITH_TONE_MARK   带声调的拼音
               2  WITHOUT_TONE     无声调的拼音
               3  WITH_TONE_NUMBER 将声调转换为1~4, 紧跟在拼音后
        :return: 返回汉字对应的拼音
        """
        cls.init()
        chinese_char = convert_to_str(chinese_char)
        return ''.join([cls.format_pinyin(i, pinyinFormat) for i in cls.PINYIN_TABLE.get(chinese_char, [chinese_char])])

    @classmethod
    def convert_to_pinyin_from_sentence(cls, chinese_chars, pinyinFormat=PinyinFormat.WITHOUT_TONE, segment=None) \
            -> str:
        """
        将句子转化为对应的拼音
        :param chinese_chars:  由汉字组成的句子
        :param pinyinFormat:  返回的拼音格式
               1  WITH_TONE_MARK   带声调的拼音
               2  WITHOUT_TONE     无声调的拼音
               3  WITH_TONE_NUMBER 将声调转换为1~4, 紧跟在拼音后
        :param segment: 分词函数, 默认为None, segment=function(str)->str
        :return: 返回汉字对应的拼音
        """
        def _help(s):
            cls.init()
            s = convert_to_str(s)
            result = []
            idx = 0
            length = len(s)
            while idx < length:
                hit = False
                # 查找词组
                for step in range(PinyinResource.PHRASE_MAX_LEN, 1, -1):
                    temp_word = s[idx: idx + step]
                    if temp_word in cls.PHRASE_PINYIN_TABLE:
                        result += cls.PHRASE_PINYIN_TABLE[temp_word]
                        idx += step
                        hit = True
                        break
                    # end if
                # end for
                if hit:
                    continue
                # 查找单个汉字
                char = s[idx]
                result.append(cls.PINYIN_TABLE.get(char, [char])[0])
                idx += 1
            # end while
            return [cls.format_pinyin(pinyin, pinyinFormat) for pinyin in result]

        data = [chinese_chars] if not segment else segment(chinese_chars)
        return ''.join([''.join(_help(i)) for i in data])

    @classmethod
    def add_phrase_pinyin(cls, w, pinyinList):
        cls.init()
        cls.PHRASE_PINYIN_TABLE[w] = pinyinList

    @classmethod
    def add_char_pinyin(cls, c, pinyinList):
        cls.init()
        cls.PINYIN_TABLE[c] = pinyinList

    @classmethod
    def has_multi_pinyin(cls, c) -> bool:
        cls.init()
        c = convert_to_str(c)
        return True if len(cls.PINYIN_TABLE[c]) > 1 else False


class ChineseHelper(object):
    """ 汉字简繁转换 """
    __inited = False
    # 繁体 -> 简体
    FAN2JIAN_TABLE = {}
    # 简体 -> 繁体
    JIAN2FAN_TABLE = {}

    @classmethod
    def is_chinese(cls, s):
        s = convert_to_str(s)
        return all(u'\u4e00' <= c <= u'\u9fff' or c == u'〇' for c in s)

    @classmethod
    def init(cls, reload=False):
        if not cls.__inited or reload:
            cls.FAN2JIAN_TABLE, cls.JIAN2FAN_TABLE = PinyinResource.get_chinese_resource()
            cls.__inited = True

    @classmethod
    def convert_to_traditional_chinese(cls, chars) -> str:
        cls.init()
        s = convert_to_str(chars)
        return ''.join([cls.JIAN2FAN_TABLE.get(c, c) for c in s])

    @classmethod
    def convert_to_simplified_chinese(cls, chars) -> str:
        cls.init()
        s = convert_to_str(chars)
        return ''.join([cls.FAN2JIAN_TABLE.get(c, c) for c in s])


def __help():
    """生成不带声调的拼音文件"""
    from itertools import chain
    d1 = PinyinResource.get_pinyin_resource()
    d2 = PinyinResource.get_phrase_pinyin_resource()
    pinyins = []
    for i in chain(d1.values(), d2.values()):
        pinyins.extend(i)
    pinyins = list(set([PinyinHelper.format_pinyin(i) + '\n' for i in pinyins if i and all(['a' <= c <= 'z' for c in i])]))
    pinyins.sort()
    with open("chinese_to_pinyin_data/pinyins.txt", 'w', encoding='utf-8') as f:
        f.writelines(pinyins)


if __name__ == '__main__':
    print(PinyinHelper.format_pinyin('à'))
    # print(PinyinHelper.convert_to_pinyin_from_sentence("你 好 啊 美 女"))
    # print(PinyinHelper.convert_to_pinyin_from_sentence("你 好 啊 美 女", PinyinFormat.WITH_TONE_MARK))
    # print(ChineseHelper.convert_to_traditional_chinese("你 丑 啊 美 女").encode("utf-8"))
    __help()
