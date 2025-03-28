from enum import Enum


class TupleEnum(Enum):
    """枚举基类"""
    def __new__(cls, *args):
        """将定义的属性拆分，不影响 value 的正常使用"""
        obj = object.__new__(cls)
        obj._value_ = args[0]  # 实际值给 value 使用
        args_len = len(args)
        obj.label = args[1] if args_len >= 2 else ''
        obj.des = args[2] if args_len >= 3 else ''
        return obj

    @classmethod
    def to_choices(cls):
        return tuple([(_.value, _.label) for _ in cls])

    @classmethod
    def to_tuple(cls):
        return tuple([(_.value, _.label, _.des) for _ in cls])


class ArticleStatus(TupleEnum):
    display = (0, '公开')
    not_display = (1, '隐藏')


class ArticleActionType(TupleEnum):
    view = (0, '浏览')
    like = (1, '点赞')


class ClipboardPrivacy(TupleEnum):
    private = (0, '私有')
    shared_no_pass = (1, '公开')
    shared_pass = (2, '密码')


class ClipboardContentType(TupleEnum):
    text = (0, '文本')
    file = (1, '文件')


if __name__ == '__main__':
    print(ArticleStatus.to_tuple())
