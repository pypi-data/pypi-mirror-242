#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh
from FourthDimension.interface.generate_answer import generate_answers
from FourthDimension.interface.upload import upload_entrance
from FourthDimension.interface.query import query_entrance
from FourthDimension.interface.clean import clean_entrance
from FourthDimension.interface.parse import parse_data


def upload(doc_path):
    """
    文档上传接口
    数据格式List[Document]
    :param doc_path: 文档路径
    :return:
    """
    all_contexts = parse_data(doc_path)
    upload_entrance(all_contexts)


def query(question):
    """
    检索增强生成(问答)接口
    :param question: 问题
    :return:
    """
    top_k_contexts = query_entrance(question)
    answer = generate_answers(question, top_k_contexts)
    return answer


def clean():
    """
    清除所有数据
    """
    clean_entrance()
