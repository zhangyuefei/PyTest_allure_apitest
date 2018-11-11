# -*- coding: utf-8 -*-

# @Time    : 2018/11/9 15:06

# @Author  : litao

# @Project : project

# @FileName: GetRelevance.py

# @Software: PyCharm
from main import failureException

result = 'success'  # 初始化结果结果为success


def check_json(src_data, dst_data):
    """
    校验的json
    :param src_data:  校验内容
    :param dst_data:  接口返回的数据（被校验的内容
    :return:
    """
    global result
    if isinstance(src_data, dict):
        # 若为dict格式
        for key in src_data:
            if key not in dst_data:
                raise failureException("JSON格式校验，关键字 %s 不在返回结果 %s" % (key, dst_data))
            else:
                this_key = key
                # 递归
                if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                    check_json(src_data[this_key], dst_data[this_key])
                elif isinstance(type(src_data[this_key]), type(dst_data[this_key])):
                    raise failureException("JSON格式校验，关键字 %s 与 %s 类型不符" % (src_data[this_key], dst_data[this_key]))
                else:
                    pass
    else:
        raise failureException("JSON校验内容非dict格式")
