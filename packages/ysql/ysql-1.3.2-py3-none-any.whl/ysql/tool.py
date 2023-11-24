# -*- coding: utf-8 -*-
import logging
import os
import shutil


def get_example():
    """复制本文件的工具函数"""
    # 获取当前文件的路径
    src = os.path.join(os.path.dirname(__file__), 'example_simple.py')
    dst = "ysql_example_simple.py"
    shutil.copy(src, dst)
    print('已生成示例文件：ysql_example_simple.py')

    src = os.path.join(os.path.dirname(__file__), 'example_detailed.py')
    dst = "ysql_example_detailed.py"
    shutil.copy(src, dst)
    print('已生成示例文件：ysql_example_detailed.py')


# ====================================================================================================================
# 模块级别的日志记录器
log = logging.getLogger(__name__)


# 默认日志配置
def setup_logging(debug=False):
    log.setLevel(logging.DEBUG if debug else logging.CRITICAL)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)


# 在初始化时进行一次日志配置
setup_logging(debug=False)
