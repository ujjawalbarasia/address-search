from elasticsearch.helpers import bulk
from elasticsearch_dsl import DocType, Text, Keyword
from elastic_search.es_core_config import create_connection
from elastic_search.es_settings import INDEX_NAME


class DataHead(DocType):
    inhash = Keyword()
    district = Text()
    zone_code = Keyword()
    zone = Text()
    vkont = Keyword()
    instlion = Keyword()
    full_name = Text()
    supply = Text()
    billing_address = Text()

    class Meta:
        index = INDEX_NAME

    @staticmethod
    def bulk_create(docs):
        bulk(create_connection(), (d.to_dict(True) for d in docs))
