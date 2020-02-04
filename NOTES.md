
    cd solr-8.4.1
    bin/solr start -e cloud
    bin/post -c techproducts example/exampledocs/*

    bin/solr stop -all


    bin/solr delete -c techproducts




    bin/solr create -c <yourCollection> -s 2 -rf 2




asi to umí i PDFka takže asi tam můžu narvat ty audity tak jak jsou

snadno můžu napsat klienta v pythonu a volat to přes REST API

asi pak budu chtít rozjet víc těch uzlů aby to load balancovalo ale 2 možná
stačej, uviudíme

asi budu chtít používat nějaký metadata, to musim zjistit jak vybuduju data
takový který obsahujou jak PDF tak metadata k němu ... 



