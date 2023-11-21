#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
from FourthDimension.model.chatGPT import answer_generate


def generate_answers(question, data):
    """
    答案生成
    :param question: 问题
    :param data: 召回结果
    :return:
    """
    if data is not None:
        print('答案生成中...')
        answer = answer_generate(question, data)
        return answer
    else:
        print('无结果，请确认是否上传文档')
