import re
from datetime import datetime


def print_func(func):
    def dec(*args):
        start = datetime.now()
        result = func(*args)
        print('Execute: %s From %s to %s' % (func.__name__, start, datetime.now()))
        return result
    return dec


# @print_func
def re_cut_sentences(text):
    text = re.sub('([。！？\?])([^”’])', r"\1\n\2", text)  # 单字符断句符
    text = re.sub('(\.{6})([^”’])', r"\1\n\2", text)  # 英文省略号
    text = re.sub('(\…{2})([^”’])', r"\1\n\2", text)  # 中文省略号
    text = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', text)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    text = text.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return text.split("\n")


if __name__ == '__main__':
    paragraph = """臣亮言：先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。
    """
    re_cut_sentences(paragraph*1000)