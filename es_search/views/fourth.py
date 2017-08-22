from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from elastic_search.es_core_config import create_connection
from django.http.response import JsonResponse, HttpResponse
from elastic_search.es_settings import INDEX_NAME, es_result_size
import csv
import os


@csrf_exempt
def fourth(request):
    return render(request, 'search-para/fourth.html', {})


@csrf_exempt
def search_view_fourth(request):
    print request.GET
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 100))

    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        zone = request.GET.get('zone', None)
        district = request.GET.get('district', None)
        zone_code = request.GET.get('zone_code', None)
        name = request.GET.get('name', None)

        body = {
            "from": start,
            "size": 100,
            "query": {
                "bool": {
                    "must": [
                        {
                            'bool': {
                                'should': [
                                    {
                                         "match": {
                                                "full_name": name,
                                         }
                                    },
                                    {
                                        "fuzzy": {
                                                "full_name": name,
                                        }
                                    }
                                ]
                            }
                        } if name else {},
                        {
                            'bool': {
                                'should': [
                                    {
                                        "multi_match": {
                                            "query": keyword,
                                            "fields": ["supply", "billing_address"],
                                            "fuzziness": "AUTO"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": keyword,
                                            "fields": ["supply", "billing_address"],
                                        }
                                    }
                                ]
                            }

                        },
                    ],

                },
            }
        }

        if any([zone, zone_code, district]):
            body["query"]["bool"]["filter"] = {
                "bool": {
                    "should": [
                        {
                            "terms": {
                                "zone_code": zone_code.split(),
                            }
                        },
                        {
                            "match": {
                                "district": {
                                    "query": district,
                                }
                            }
                        },
                        {
                            "match": {
                                "zone": {
                                    "query": zone,
                                }
                            }
                        },

                    ],
                }
            }

        es = create_connection()
        res = es.search(
            index=INDEX_NAME,
            body=body
        )

        return JsonResponse(res['hits'])

    else:
        return JsonResponse({"status": "No results"}, status=400)


def csv_fourth(request):
    print request.GET
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')
        zone = request.GET.get('zone', None)
        district = request.GET.get('district', None)
        zone_code = request.GET.get('zone_code', None)
        name = request.GET.get('name', None)

        body = {
            "size": 9999,
            "query": {
                "bool": {
                    "must": [
                        {
                            'bool': {
                                'should': [
                                    {
                                         "match": {
                                                "full_name": name,
                                         }
                                    },
                                    {
                                        "fuzzy": {
                                                "full_name": name,
                                        }
                                    }
                                ]
                            }
                        } if name else {},
                        {
                            'bool': {
                                'should': [
                                    {
                                        "multi_match": {
                                            "query": keyword,
                                            "fields": ["supply", "billing_address"],
                                            "fuzziness": "AUTO"
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": keyword,
                                            "fields": ["supply", "billing_address"],
                                        }
                                    }
                                ]
                            }

                        },
                    ],

                },
            }
        }

        if any([zone, zone_code, district]):
            body["query"]["bool"]["filter"] = {
                "bool": {
                    "should": [
                        {
                            "terms": {
                                "zone_code": zone_code.split(),
                            }
                        },
                        {
                            "match": {
                                "district": {
                                    "query": district,
                                }
                            }
                        },
                        {
                            "match": {
                                "zone": {
                                    "query": zone,
                                }
                            }
                        },

                    ],
                }
            }

        es = create_connection()
        res = es.search(
            index=INDEX_NAME,
            body=body
        )

        sample = res['hits']
        print("Got %d Hits:" % res['hits']['total'])
        with open('outputfile.csv', 'wb') as csvfile:   #set name of output file here
            filewriter = csv.writer(csvfile, delimiter=str(u','),  # we use TAB delimited, to handle cases where freeform text may have a comma
                                    quotechar=str(u'|'), quoting=csv.QUOTE_MINIMAL)

            filewriter.writerow(["Match Score", "District", "Zone Code", "Zone", "Full name", "vkont", "instlion", "Supply", "Billing Address"])    #change the column labels here
            for hit in res['hits']['hits']:
                col1 = hit["_score"]
                col2 = hit["_source"]["district"]
                col3 = hit["_source"]["zone_code"]
                col4 = hit["_source"]["zone"]
                col5 = hit["_source"]["full_name"]
                col6 = hit["_source"]["vkont"]
                col7 = hit["_source"]["instlion"]
                col8 = hit["_source"]["supply"]
                col9 = hit["_source"]["billing_address"]
                filewriter.writerow([col1, col2, col3, col4, col5, col6, col7, col8, col9])

        data = open('outputfile.csv', 'r').read()
        resp = HttpResponse(data, content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename=outputfile.csv'
        return resp