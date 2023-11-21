#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
from FourthDimension.utils.file_parse import get_all_docx_contexts


def parse_data(doc_path):
    """
    数据解析
    :param doc_path: 文档路径
    :return:
    """
    print('开始文档解析...')
    all_contexts = get_all_docx_contexts(doc_path)
    return all_contexts
