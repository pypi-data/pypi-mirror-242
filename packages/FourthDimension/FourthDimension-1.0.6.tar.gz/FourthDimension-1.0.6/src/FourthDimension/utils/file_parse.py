#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh


"""
文件说明：
"""
import json
import os

from FourthDimension.parser.docx_parser import parse_docx


def get_file_paths_and_names(folder_path):
    if '.doc' in folder_path or '.docx' in folder_path or '.json' in folder_path:
        return [(folder_path, os.path.basename(folder_path))]
    else:
        file_paths_and_names = []
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_paths_and_names.append((file_path, file_name))
    return file_paths_and_names


def get_all_docx_contexts(doc_path):
    all_contexts = []
    file_paths_and_names = get_file_paths_and_names(doc_path)
    for i, d in enumerate(file_paths_and_names):
        file_path = d[0]
        file_name = d[1]
        document = parse_docx(file_path, file_name)
        all_contexts.extend(document)
    return all_contexts
