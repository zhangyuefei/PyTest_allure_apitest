# -*- coding: utf-8 -*-

# @Time    : 2018/11/9 15:06

# @Author  : litao

# @Project : project

# @FileName: GetRelevance.py

# @Software: PyCharm

import operator
import re

import allure

from Common import CheckJson, expectedManage, CustomFail
from main import failureException


def check(test_name, case_data, code, data, relevance, _path):
    """
    校验测试结果
    :param test_name:  测试用例
    :param case_data:  测试用例
    :param code:  HTTP状态
    :param data:  返回的接口json数据
    :param relevance:  关联值对象
    :param _path:  case路径
    :return:
    """
    # 不校验
    if case_data["check_type"] == 'no_check':
        with allure.step("不校验结果"):
            pass

    # 校验json格式
    elif case_data["check_type"] == 'json':
        expected_request = case_data["expected_request"]
        # 判断预期结果格式，如果是字符串，则打开文件路径，提取保存在文件中的期望结果
        if isinstance(case_data["expected_request"], str):
                expected_request = expectedManage.read_json(test_name, expected_request, relevance, _path)
        with allure.step("JSON格式校验"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach('期望data', str(expected_request))
            allure.attach("实际code", str(code))
            allure.attach('实际data', str(data))
        if int(code) == case_data["expected_code"]:
            if not data:
                data = "{}"
            # json校验
            CheckJson.check_json(expected_request, data)
        else:
            if case_data.get("CustomFail"):
                info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                raise failureException(str(info)+"\nhttp状态码错误！\n %s != %s" % (code, case_data["expected_code"]))
            else:
                raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 只校验HTTP状态
    elif case_data["check_type"] == 'only_check_status':
        with allure.step("校验HTTP状态"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach("实际code", str(code))
        if int(code) == case_data["expected_code"]:
            pass
        else:
            if case_data.get("CustomFail"):
                info = CustomFail.custom_manage(case_data.get("CustomFail"), relevance)
                raise failureException(str(info)+"\nhttp状态码错误！\n %s != %s" % (code, case_data["expected_code"]))
            else:
                raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 完全校验
    elif case_data["check_type"] == 'entirely_check':
        expected_request = case_data["expected_request"]
        # 判断预期结果格式，如果是字符串，则打开文件路径，提取保存在文件中的期望结果
        if isinstance(case_data["expected_request"], str):
            expected_request = expectedManage.read_json(test_name, expected_request, relevance, _path)
        with allure.step("完全校验"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach('期望data', str(expected_request))
            allure.attach("实际code", str(code))
            allure.attach('实际data', str(data))
        if int(code) == case_data["expected_code"]:
            result = operator.eq(expected_request, data)
            if result:
                pass
            else:
                raise failureException("完全校验失败！ %s ! = %s" % (expected_request, data))
        else:
            raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 正则校验
    elif case_data["check_type"] == 'Regular_check':
        with allure.step("正则校验"):
            allure.attach("期望code", str(case_data["expected_code"]))
            allure.attach('正则表达式', str(case_data["expected_request"]).replace("\'", "\""))
            allure.attach("实际code", str(code))
            allure.attach('实际data', str(data))
        if int(code) == case_data["expected_code"]:
            try:
                result = ""  # 初始化校验内容
                if isinstance(case_data["expected_request"], list):
                    # 多个正则表达式校验，遍历校验
                    for i in case_data["expected_request"]:
                        result = re.findall(i.replace("\"", "\'"), str(data))
                        allure.attach(i.replace("\"", "\'")+'校验完成结果', str(result))
                else:
                    # 单个正则表达式
                    result = re.findall(case_data["expected_request"].replace("\"", "\'"), str(data))
                    allure.attach(case_data["expected_request"].replace("\"", "\'")+'校验完成结果',
                                  str(result).replace("\'", "\""))
                # 未匹配到校验内容
                if not result:
                    raise failureException("无正则校验内容！ %s" % case_data["expected_request"])
            # 正则表达式为空时
            except KeyError:
                raise failureException("正则校验执行失败！ %s" % case_data["expected_request"])
        else:
            raise failureException("http状态码错误！\n %s != %s" % (code, case_data["expected_code"]))

    # 数据库校验
    elif case_data["check_type"] == "datebase_check":
        pass
    else:
        raise failureException("无该校验方式%s" % case_data["check_type"])
