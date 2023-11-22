# -*- coding: utf-8 -*-

from typing import Union


def Entity(check_type: bool = False):
    """数据类dataclass的装饰器。

    在定义dataclass时，同时将约束条件和默认值赋予类属性。通过改造原生dataclass的init方法和getattribute方法，实现sql建表时约束条件的
    解析，以及正常使用被装饰dataclass时属性值的获取。

    Args:
        check_type(bool): True -> 实例化dataclass时检查属性值和类型注释是否一致，不一致将触发类型错误。

    """

    def decorator(cls):
        orig_getattribute = cls.__getattribute__
        orig_init = cls.__init__

        def getattribute(self, name):
            """重写被装饰dataclass的取值方法"""
            # 只有访问定义的属性时才进一步处理
            if name in set(attr_name for attr_name, attr_type in cls.__annotations__.items()):
                return parse_attr_value(orig_getattribute(self, name))
            # 访问内部属性则返回原始值
            return orig_getattribute(self, name)

        def init_and_check_type(self, *args, **kwargs):
            """重写被装饰dataclass的初始化方法"""
            orig_init(self, *args, **kwargs)

            for attr_name, attr_type in cls.__annotations__.items():
                # 先检查类型注解是否是允许的数据类型
                if attr_type not in {int, str, float, bytes}:
                    raise TypeError(
                        f"定义'{cls.__name__}'类时，"
                        f"'{attr_name}'属性的类型应该属于: 'int'、'str'、'float'、'bytes'，"
                        f"但得到的是'{attr_type.__name__}'")

                # 再检查属性值的类型与类型注解是否一致
                attr_value = getattribute(self, attr_name)
                # 不检查默认值为None的属性
                if attr_value is None:
                    continue
                elif not isinstance(attr_value, attr_type):
                    raise TypeError(
                        f"实例化'{cls.__name__}'类时,"
                        f"'{attr_name}'属性的类型应该是'{attr_type.__name__}',"
                        f"但得到的是'{type(attr_value).__name__}'")

        # 由于无参装饰器的特性，在无参使用该装饰器时，check_type的值被覆盖为cls，因此必须显式的与True进行判断
        if check_type == True:  # noqa
            cls.__init__ = init_and_check_type
        cls.__getattribute__ = getattribute
        return cls

    # 无参使用该装饰器时
    if callable(check_type):
        return decorator(cls=check_type)

    return decorator


class Constant:
    """维护常用的sql约束字符串，并不直接对外开放。"""
    PRIMARY_KEY = ("PRIMARY KEY",)
    AUTO_PRIMARY_KEY = ("PRIMARY KEY AUTOINCREMENT",)
    NOT_NULL = ("NOT NULL",)
    UNIQUE = ("UNIQUE",)

    NO_ACTION = 'NO ACTION'
    RESTRICT = 'RESTRICT'
    CASCADE = 'CASCADE'
    SET_NULL = 'SET NULL'
    SET_DEFAULT = 'SET DEFAULT'


class Constraint:
    """对外开放的各种字段约束"""

    # =================================================================================================================
    # 1.可直接使用的约束常量
    primary_key = Constant.PRIMARY_KEY  # 主键
    auto_primary_key = Constant.AUTO_PRIMARY_KEY  # 自增主键
    not_null = Constant.NOT_NULL  # 非空
    unique = Constant.UNIQUE  # 唯一

    # 针对外键的约束
    no_action = Constant.NO_ACTION
    cascade = Constant.CASCADE
    set_null = Constant.SET_NULL
    restrict = Constant.RESTRICT
    set_default = Constant.SET_DEFAULT

    # =================================================================================================================
    # 2.需要外部传值的约束
    @staticmethod
    def default(default_value: Union[int, str, float, bytes]):
        """默认值约束"""
        if type(default_value) in {int, str, float, bytes}:
            return (f'DEFAULT {default_value}',)  # noqa
        raise TypeError(
            f"dataclass属性默认值允许的数据类型: 'int', 'str', 'float', 'bytes',"
            f"但得到的是'{type(default_value).__name__}'"
        )

    @staticmethod
    def check(check_condition: str):
        """条件约束"""
        if type(check_condition) in {str}:
            return (f'CHECK({check_condition})',)  # noqa
        raise TypeError(
            f"对dataclass属性使用条件约束时，允许的数据类型: 'str',"
            f"但得到的是'{type(check_condition).__name__}'")

    @staticmethod
    def foreign_key(entity, field, delete_link=None, update_link=None):
        """外键约束

        Args:
            entity: 外键所在的数据类（父表）
            field: 外键对应的数据类属性
            delete_link: 级联删除方式
            update_link: 级联更新方式

        """
        return ((entity.__name__, field, delete_link, update_link),)  # noqa

    @staticmethod
    def comment(comment: str):
        """字段注释"""
        if type(comment) in {str}:
            # 目前仅支持sqlite的注释格式
            return (f'-- {comment}\n',)  # noqa
        raise TypeError(
            f"对dataclass属性使用sql注释时，允许的数据类型: 'str',"
            f"但得到的是'{type(comment).__name__}'")


def parse_constraints(attr_value):
    """从原始属性值中解析出约束条件"""
    if not isinstance(attr_value, tuple):
        return []

    # 单元素元组
    if len(attr_value) == 1:
        return list(attr_value)

    # 多元素元组
    elif len(attr_value) > 1:
        constraints = []

        for item in attr_value:
            if not isinstance(item, tuple):
                continue
            # 元素也是元组，说明是约束条件
            if len(item) == 1:
                constraints.append(item[0])
            else:
                raise TypeError(f'约束条件必须为长度为1的元组，错误的数据: {item}')

        return constraints

    else:
        raise TypeError(f'属性值的数据结构不满足要求，无法解析出sql约束\n传入的值: {attr_value}')


def parse_attr_value(attr_value):
    """从原始属性值中解析出默认值或者是实例化时传入的属性值"""
    # 原始值满足类型要求，直接返回该值
    if isinstance(attr_value, (int, str, float, bytes)) or attr_value is None:
        return attr_value

    # 首先排除非元组情况
    if not isinstance(attr_value, tuple):
        raise TypeError('数据类的属性值不满足要求，只允许基本类型和Constraint类约束')

    # 元组长度为1，内容为约束条件，即原始值为一个约束。
    constraints = [value for key, value in vars(Constant).items() if not key.startswith('__')]
    if len(attr_value) == 1:
        if attr_value in constraints:
            return None
        else:
            TypeError('数据类的属性值不满足要求，只允许基本类型和Constraint类约束')
    # 多元素元组，1.同时包含属性值与约束。2.包含多个约束
    else:
        # 用列表保存匹配到的基本属性值，用来进一步检验该值是否唯一
        value_list = [value for value in attr_value
                      if isinstance(value, (int, str, float, bytes))]

        constraint_list = [value for value in attr_value
                           if value in constraints]

        # 有唯一的默认值
        if len(value_list) == 1 and len(constraint_list) == len(attr_value) - 1:
            return value_list[0]
        # 没有默认值
        elif len(constraint_list) == len(attr_value):
            return None
        else:
            raise TypeError('数据类的属性值不满足要求，只允许基本类型和Constraint类约束')
