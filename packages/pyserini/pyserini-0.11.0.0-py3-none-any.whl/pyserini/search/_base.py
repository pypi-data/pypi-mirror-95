#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import os
import logging

from ..pyclass import autoclass, JPaths
from pyserini.util import get_cache_home

logger = logging.getLogger(__name__)

# Wrappers around Lucene classes
JQuery = autoclass('org.apache.lucene.search.Query')
JDocument = autoclass('org.apache.lucene.document.Document')

# Wrappers around Anserini classes
JQrels = autoclass('io.anserini.eval.Qrels')
JRelevanceJudgments = autoclass('io.anserini.eval.RelevanceJudgments')
JTopicReader = autoclass('io.anserini.search.topicreader.TopicReader')
JTopics = autoclass('io.anserini.search.topicreader.Topics')
JQueryGenerator = autoclass('io.anserini.search.query.QueryGenerator')
JBagOfWordsQueryGenerator = autoclass('io.anserini.search.query.BagOfWordsQueryGenerator')
JCovid19QueryGenerator = autoclass('io.anserini.search.query.Covid19QueryGenerator')


class Document:
    """Wrapper class for a Lucene ``Document``.

    Parameters
    ----------
    document : JDocument
        Underlying Lucene ``Document``.
    """

    def __init__(self, document):
        if document is None:
            raise ValueError('Cannot create a Document with None.')
        self.object = document

    def docid(self: JDocument) -> str:
        return self.object.getField('id').stringValue()

    def id(self: JDocument) -> str:
        # Convenient alias for docid()
        return self.object.getField('id').stringValue()

    def lucene_document(self: JDocument) -> JDocument:
        return self.object

    def contents(self: JDocument) -> str:
        return self.object.get('contents')

    def raw(self: JDocument) -> str:
        return self.object.get('raw')

    def get(self: JDocument, field: str) -> str:
        return self.object.get(field)


def get_topics(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        Topics as a dictionary
    """
    topics = None
    if collection_name == 'robust04':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST04)
    elif collection_name == 'robust05':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST05)
    elif collection_name == 'core17':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE17)
    elif collection_name == 'core18':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE18)
    elif collection_name == 'car17v1.5-benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V15_BENCHMARK_Y1_TEST)
    elif collection_name == 'car17v2.0-benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V20_BENCHMARK_Y1_TEST)
    elif collection_name == 'dl19-doc':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_DL_DOC)
    elif collection_name == 'dl19-passage':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_DL_PASSAGE)
    elif collection_name == 'msmarco-doc-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_DEV)
    elif collection_name == 'msmarco-passage-dev-subset':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_DEV_SUBSET)
    elif collection_name == 'covid-round1':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1)
    elif collection_name == 'covid-round1-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1_UDEL)
    elif collection_name == 'covid-round2':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2)
    elif collection_name == 'covid-round2-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2_UDEL)
    elif collection_name == 'covid-round3':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3)
    elif collection_name == 'covid-round3-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3_UDEL)
    elif collection_name == 'covid-round4':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND4)
    elif collection_name == 'covid-round4-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND4_UDEL)
    elif collection_name == 'trec2018-bl':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2018_BL)
    elif collection_name == 'trec2019-bl':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_BL)
    elif collection_name == 'dpr-nq-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_NQ_DEV)
    elif collection_name == 'dpr-nq-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_NQ_TEST)
    elif collection_name == 'dpr-trivia-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_TRIVIA_DEV)
    elif collection_name == 'dpr-trivia-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_TRIVIA_TEST)
    elif collection_name == 'dpr-wq-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_WQ_TEST)
    elif collection_name == 'dpr-squad-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_SQUAD_TEST)
    elif collection_name == 'dpr-curated-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_CURATED_TEST)
    else:
        return {}
    t = {}
    for topic in topics.keySet().toArray():
        # Try and parse the keys into integers
        try:
            topic_key = int(topic)
        except ValueError:
            topic_key = topic
        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)
    return t


def get_topics_with_reader(reader_class, file):
    # Yes, this is an insanely ridiculous method name.
    topics = JTopicReader.getTopicsWithStringIdsFromFileWithTopicReaderClass(reader_class, file)
    t = {}
    for topic in topics.keySet().toArray():
        # Try and parse the keys into integers
        try:
            topic_key = int(topic)
        except ValueError:
            topic_key = topic
        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)
    return t


def get_qrels_file(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    path : str
        path of the qrels file
    """
    qrels = None
    if collection_name == 'robust04':
        qrels = JQrels.ROBUST04
    elif collection_name == 'robust05':
        qrels = JQrels.ROBUST05
    elif collection_name == 'core17':
        qrels = JQrels.CORE17
    elif collection_name == 'core18':
        qrels = JQrels.CORE18
    elif collection_name == 'car17v1.5-benchmarkY1test':
        qrels = JQrels.CAR17V15_BENCHMARK_Y1_TEST
    elif collection_name == 'car17v2.0-benchmarkY1test':
        qrels = JQrels.CAR17V20_BENCHMARK_Y1_TEST
    elif collection_name == 'dl19-doc':
        qrels = JQrels.TREC2019_DL_DOC
    elif collection_name == 'dl19-passage':
        qrels = JQrels.TREC2019_DL_PASSAGE
    elif collection_name == 'msmarco-doc-dev':
        qrels = JQrels.MSMARCO_DOC_DEV
    elif collection_name == 'msmarco-passage-dev-subset':
        qrels = JQrels.MSMARCO_PASSAGE_DEV_SUBSET
    elif collection_name == 'covid-round1':
        qrels = JQrels.COVID_ROUND1
    elif collection_name == 'covid-round2':
        qrels = JQrels.COVID_ROUND2
    elif collection_name == 'covid-round3':
        qrels = JQrels.COVID_ROUND3
    elif collection_name == 'covid-round3-cumulative':
        qrels = JQrels.COVID_ROUND3_CUMULATIVE
    elif collection_name == 'covid-round4':
        qrels = JQrels.COVID_ROUND4
    elif collection_name == 'covid-round4-cumulative':
        qrels = JQrels.COVID_ROUND4_CUMULATIVE
    elif collection_name == 'covid-round5':
        qrels = JQrels.COVID_ROUND5
    elif collection_name == 'covid-complete':
        qrels = JQrels.COVID_COMPLETE
    elif collection_name == 'trec2018-bl':
        qrels = JQrels.TREC2018_BL
    elif collection_name == 'trec2019-bl':
        qrels = JQrels.TREC2019_BL
    if qrels:
        target_path = os.path.join(get_cache_home(), qrels.path)
        if os.path.exists(target_path):
            return target_path
        target_dir = os.path.split(target_path)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_path, 'w') as file:
            qrels_content = JRelevanceJudgments.getQrelsResource(qrels)
            file.write(qrels_content)
        return target_path
    raise FileNotFoundError(f'no qrels file for {collection_name}')


def get_qrels(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        qrels as a dictionary
    """
    file_path = get_qrels_file(collection_name)
    qrels = {}
    with open(file_path, 'r') as f:
        for line in f:
            qid, _, docid, judgement = line.rstrip().split()
            try:
                qrels_key = int(qid)
            except ValueError:
                qrels_key = qid
            try:
                doc_key = int(docid)
            except ValueError:
                doc_key = docid
            if qrels_key in qrels:
                qrels[qrels_key][doc_key] = judgement
            else:
                qrels[qrels_key] = {doc_key: judgement}
    return qrels
