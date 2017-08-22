import hashlib
import traceback

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from elasticsearch_dsl import FacetedSearch

from es_settings import *


def create_connection():
    try:
        return connections.create_connection(**DATABASE_CONNECTION_INFO)
    except Exception as e:
        print '-------------------------------'
        print 'Error logged in Activity Log'
        print '-------------------------------'
        print traceback.print_exc()

    raise Exception(e)


def create_index():
    try:
        create_connection()
        db = Index(INDEX_NAME)
        db.settings(**INDEX_SETTINGS)
        db.create()
    except Exception as e:
        print '-------------------------------'
        print 'Error logged in Activity Log'
        print '-------------------------------'
        print traceback.print_exc()
        raise Exception(e)
    else:
        return db


def get_index():
    create_connection()
    db = Index(INDEX_NAME)
    if db.exists():
        return db
    else:
        return create_index()


# def get_mapping_class(source):
#     return locate(
#         SCRAPPER_FOLDER_STRUCTURE[str(source.ds_type)] + '.' + source.es_structure, forceload=1
#     )


def create_mappings():
    index = get_index()
    from es_models import DataHead
    if not index.exists_type(doc_type=DataHead.__name__):
        DataHead.init()
    # for source in Source.objects.all():
    #     try:
    #         klass = get_mapping_class(source)
    #         if not index.exists_type(doc_type=klass.__name__):
    #             klass.init()
    #     except Exception as e:
    #         print '-------------------------------'
    #         print 'Error logged in Activity Log'
    #         print '-------------------------------'
    #         print traceback.print_exc()
    #         raise Exception(e)


# Avoid using following method as ES doesn't handle deletions in a mapping
# def update_mappings():
#     get_index()
#     for source in Source.objects.all():
#         try:
#             klass = get_mapping_class(source)
#             klass.init()
#         except Exception as e:
#             print '-------------------------------'
#             print 'Error logged in Activity Log'
#             print '-------------------------------'
#             print traceback.print_exc()
#
#     ActivityLog.objects.create_log(
#         None, level='W', view_name='data.tasks.update_mappings',
#         message='Forced ElasticSearch mapping update.'
#     )


class CustomSearch(FacetedSearch):
    index = INDEX_NAME


def search(search_arg):
    return CustomSearch(search_arg).execute()


def get_dict_text(d):
    block = ''
    for key in sorted(d):
        if type(d[key]) is dict:
            block += get_dict_text(d[key])
        else:
            block += (d[key])
    return block


def get_hash(d):
    block = get_dict_text(d)
    return hashlib.sha512(block).hexdigest()

