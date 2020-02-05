TODO jak spustim znova něco kde už mam vytvořenou kolekci a tak ???


    cd solr-8.4.1
    bin/solr start -e cloud
    bin/post -c techproducts example/exampledocs/*


"/home/rosa/elitr/clir/solr-8.4.1/bin/solr" start -cloud -p 8983 -s
"/home/rosa/elitr/clir/solr-8.4.1/example/cloud/node1/solr"

"/home/rosa/elitr/clir/solr-8.4.1/bin/solr" start -cloud -p 7574 -s
"/home/rosa/elitr/clir/solr-8.4.1/example/cloud/node2/solr" -z localhost:9983

http://localhost:8983/solr/admin/collections?action=CREATE&name=techproducts&numShards=2&replicationFactor=2&maxShardsPerNode=2&collection.configName=techproducts



"/home/rosa/elitr/clir/solr-8.4.1/bin/solr" start -cloud -p 8989 -s
"/home/rosa/elitr/clir/solr-8.4.1/example/cloud/node1/solr"

http://localhost:8989/solr/admin/collections?action=CREATE&name=techproducts&numShards=1&replicationFactor=1&maxShardsPerNode=1&collection.configName=techproducts

POSTing request to Config API: http://localhost:8989/solr/techproducts/config
{"set-property":{"updateHandler.autoSoftCommit.maxTime":"3000"}}



bin/post -p 8989 -c techproducts example/exampledocs/*


curl "http://localhost:8989/solr/techproducts/select?q=\"CAS+latency\""

QUERY_STRING='q=foundation' python3 vystup.py

sol2:8989 ... techproducts



    bin/solr stop -all


    bin/solr delete -c techproducts




    bin/solr create -c <yourCollection> -s 2 -rf 2




asi to umí i PDFka takže asi tam můžu narvat ty audity tak jak jsou

snadno můžu napsat klienta v pythonu a volat to přes REST API

asi pak budu chtít rozjet víc těch uzlů aby to load balancovalo ale 2 možná
stačej, uviudíme

asi budu chtít používat nějaký metadata, to musim zjistit jak vybuduju data
takový který obsahujou jak PDF tak metadata k němu ... 


asi budu nakonec chtít zkonvertovat ty audity a jejich metadata do nějakejch
JSOn nebo něco dokumentů a ty pak mít v tý kolekci...


