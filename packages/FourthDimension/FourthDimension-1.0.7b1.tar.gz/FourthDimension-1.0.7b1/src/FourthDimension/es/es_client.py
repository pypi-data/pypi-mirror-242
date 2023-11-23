#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 
# @Author   : wgh

from elasticsearch import Elasticsearch

from FourthDimension.config.config import config_setting
from FourthDimension.es.es_sort import (
    question_analysis,
    getDetailResult
)

"""
文件说明：
"""
# Elasticsearch连接信息
host = config_setting['elasticsearch_setting']['host']
port = config_setting['elasticsearch_setting']['port']
username = config_setting['elasticsearch_setting']['username']
password = config_setting['elasticsearch_setting']['password']
index_name = config_setting['elasticsearch_setting']['index_name']
analyzer = config_setting['elasticsearch_setting']['analyzer']


class DocQAAnswerEntity:
    def init(self, content, question, fuzz_score, words_ratio):
        self.content = content
        self.question = question
        self.fuzz_score = fuzz_score
        self.words_ratio = words_ratio


class ElasticsearchClient:
    def __init__(self, host=host, port=port, username=username, password=password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = Elasticsearch(
            [self.host],
            http_auth=(self.username, self.password),
            port=self.port,
            use_ssl=False,
            verify_certs=False,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )

    def create_index(self):
        index_exists = self.client.indices.exists(index=index_name)
        if index_exists:
            # print(f"索引 '{index_name}' 已存在")
            pass
        else:
            # 创建索引
            settings = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "index.lifecycle.name": "default_index",
                    "index.lifecycle.rollover_alias": "index"
                },
                "mappings": {
                    "dynamic": "strict",
                    "properties": {
                        "file_name": {
                            "type": "keyword"
                        },
                        "type": {
                            "type": "keyword"
                        },
                        "text": {
                            "type": "text",
                            "analyzer": analyzer,
                            "search_analyzer": analyzer
                        }
                    }
                }
            }
            self.client.indices.create(index=index_name, ignore=400, body=settings)
            if self.client.indices.exists(index=index_name):
                print(f"索引 '{index_name}' 创建成功")
            else:
                print(f"索引 '{index_name}' 创建失败，请检查es设置")

    def insert_data(self, all_context):
        self.create_index()
        file_names = self.search_filename()
        for i, d in enumerate(all_context):
            filename = d.metadata['source']
            if filename not in file_names:
                context = d.page_content
                self.client.index(index=index_name, doc_type='_doc', body={
                    'file_name': filename,
                    'type': 'part',
                    'text': context})
        return all_context

    def search_filename(self):
        # 构建查询语句
        query = {
            "size": 10000,
            "_source": ["file_name"],
            "query": {
                "match_all": {}
            }
        }
        # 执行查询
        result = self.client.search(index=index_name, body=query)

        # 从查询结果中提取文件名
        file_names = [hit["_source"]["file_name"] for hit in result["hits"]["hits"]]

        # 去重文件名列表
        unique_file_names = list(set(file_names))
        return unique_file_names

    def clean_data(self):
        """
        清除数据
        """
        self.create_index()
        self.client.delete_by_query(index=index_name, body={"query": {"match_all": {}}})

    def es_search(self, question):
        self.create_index()
        question_anal = question_analysis(question)
        searchHits = []
        try:
            # es查询
            sourceBuilder = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                "text": {
                                                    "query": question,
                                                    "boost": 1,
                                                    "analyzer": analyzer
                                                }
                                            }
                                        },
                                        {
                                            "match": {
                                                "text": {
                                                    "query": question_anal,
                                                    "boost": 3,
                                                    "analyzer": analyzer
                                                }
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "term": {
                                    "type": "part"
                                }
                            }
                        ],
                        "filter": [
                            {
                                "term": {
                                    "type": "part"
                                }
                            }
                        ]
                    }
                },
                "size": 10
            }
            response = self.client.search(index=index_name, body=sourceBuilder)
            hits = response["hits"]["hits"]
            searchHits = hits
        except Exception as e:
            print(e)

        esResponses = []

        # 获取es查询命中结果
        for hit in searchHits:
            esResponse = DocQAAnswerEntity()
            hitString = hit["_source"]
            content = hitString['text']
            esResponse.question = question
            esResponse.content = content
            esResponses.append(esResponse)
        sorted_es_response = getDetailResult(esResponses, question, question_anal)
        top_k_content = []
        for i, d in enumerate(sorted_es_response):
            top_k_content.append(d.content)
        return top_k_content
