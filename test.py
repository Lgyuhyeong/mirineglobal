from elasticsearch import Elasticsearch

es = Elasticsearch()
r = es.indices.get_alias('*')
print(r)