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

bin/post -p 8989 -host sol2 -c techproducts example/exampledocs/*


curl "http://localhost:8989/solr/techproducts/select?q=\"CAS+latency\""

QUERY_STRING='q=foundation' python3 vystup.py

sol2:8989 ... techproducts






bin/solr create -c konzavery

bin/post -p 8989 -c konzavery ../kon-zavery/*.pdf

...to má nějakej problém
(ale postnout to do ty předchozí kolekce jde, takže jen mam nějakej problém s
vytvářenim tý nový kolůekce asi)


SimplePostTool: WARNING: Solr returned an error #404 (Not Found) for url: http://localhost:8989/solr/konzavery/update/extract?resource.name=%2Flnet%2Fms%2Fprojects%2Felitr%2Fclir%2Fsolr-8.4.1%2F..%2Fkon-zavery%2FK99039.pdf&literal.id=%2Flnet%2Fms%2Fprojects%2Felitr%2Fclir%2Fsolr-8.4.1%2F..%2Fkon-zavery%2FK99039.pdf
SimplePostTool: WARNING: Response: <html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>Error 404 Not Found</title>
</head>
<body><h2>HTTP ERROR 404</h2>
<p>Problem accessing /solr/konzavery/update/extract. Reason:
<pre>    Not Found</pre></p>
</body>
</html>
SimplePostTool: WARNING: IOException while reading response: java.io.FileNotFoundException: http://localhost:8989/solr/konzavery/update/extract?resource.name=%2Flnet%2Fms%2Fprojects%2Felitr%2Fclir%2Fsolr-8.4.1%2F..%2Fkon-zavery%2FK99039.pdf&literal.id=%2Flnet%2Fms%2Fprojects%2Felitr%2Fclir%2Fsolr-8.4.1%2F..%2Fkon-zavery%2FK99039.pdf




    bin/solr start 
    bin/solr create -c files -d example/files/conf
    bin/post -c files ~/Documents















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












TODO převést na txt je asi lepší přes calibre než přes pdftotext -- ale přes
calibre to občas selže a je stejně potřeba pdftotext jako backup; teď pro
jednoduchost jen pdftottext

překlad má nějakej limit

413 REQUEST ENTITY TOO LARGE:
112629 characters

OK:
88186 characters

There is a limitation on the size of the payload (file/request); this is
currently 102400B

asi má smysl tam pro jistotu cpát jen dokument menší než 50k znaků,
a jak se tohle přešvihne tak to tzam poslat a další poslat později

možná se to blbě přeloží když tam jsou řádky blbě, na to by byl lepší ten
calibre konvertor



Postup:

* najít web kde jdou stáhnout reporty
* stáhnout seznamy reportů
* profiltrovat reporty podle jazyka a podle roku
* stáhnout PDFka, zachovat metadata pokud jsou (např. název)
* calibre konverzí dostat text z PDF
* přeložit do angličtiny a následně do dalších jazyků
* nahrát do search tohletoho



překlad: asi 100 slov za sekundu

belgické audity: 20844263 slov, tj. 208442 sekund, tj. 2,5 dne

1997 - 2012 converted by calibre, can translate
start by 2012 and go back in time;
once everything calibred, kill translation and translate new files

maybe skip large files, at least for now?

total now is 10M words
500 files, 16 are > 100kW, 40 are > 50kW
...let's only take those < 50kW,
this leaves out 10% of the files but 50% of words


jeden z dotazů může bejt "bydlení"
nebo "sloučení rodiny"


překlad mi zachovává řádky, takže můžu snadno ukázat tentýž řádek z
různejch jazykovejch verzí téhož fajlu
...když ukazuju výsledek, tak to bych chtěl (pokud ideálně nějak zjistim odkud
ten highlight je)
...chtěl bych ideálně i synchronizované skrolování
...na to určo něco bude, co ukáže čísla řádků a bude je to zobrazovat
synchro a tak, to půjde nějak; minimálně by na to šlo použít HTML
tables....


nku_be 2019: 1.5 MW, z toho 800 kW fajly < 50 kW
100 W / 1 s ... 800 kW za 8 000 s = 133 min

TODO smazat pak prádzné fajly !! ALE OPATRNĚ !! radši nejdřív backup


nku_be: data 2016-2020 (ostatní později) French English Czech German



možnosti:
* buď pro každej jazyk samostatnej solr
* anebo jeden prostě kde je všechno na jedný hromadě -- to má jednodušší
  interface
  * napovědět, které jazyky podporujeme, vlaječkama na vstupní stránce
  * ale pak nevim jak prezentovat výsledky
* takže stejně chci nechat vybrat jazyk, a jestli bude vyhledávadlo jedno
  nmebo jich bude několik už je vedlejší, ale spíš několik

* _default nemá extractor
* sample_techproducts_configs má extractor
* víc tomu nerozumim :-?


* jeden solr pro všechno, 4 nodes 8971 ... 8974
* kolekce eurosaiall
* http://sol2:8971/solr 

    bin/solr create -p 8971 -c eurosaiall -d sample_techproducts_configs -s 4 -rf 4
    bin/post -p 8971 -c eurosaiall ../data/data_cs/source_fr/nku_be/2020/*txt
    bin/post -p 8971 -c eurosaiall ../data/data_cs/source_fr/nku_be/????/*txt

    bin/post -p 8971  -host sol2 -c eurosaiall ../data/data_cs/source_cs/nku_cs/????/*txt


* sloučení rodiny
* family reunification
* Familienzusammenführung
* regroupement familial

DONE??: stránkování výsledků (anebo rovnou zobrazovat všechny)
...zobrazuju 100 výsledků, což by mělo stačit

DONE??: návrty na předchozí stránky
...zrušeno `target=_blank`


DONE: viewdoc i bez metadat

DONE: highligh case insensitive


TODO: metadata cs
...in progress


TODO: rozdělit podle jazyka vyhledávání
- ideálně přidat nějakej parametr do vyhledávání na to


TODO: indexnout nově přeložená data


TODO: vstupní stránky


TODO: připravit tasky


# status

* nku be: 2016-2020
* nku cs: 2019-2013 asi, bude to do 2011 až se to dopřeloži a doindexuje


## solr search

q: query

hl, hl,fl: highlighting

https://lucene.apache.org/solr/guide/8_4/highlighting.html#highlighting

fl=id: only return ids of documents, not whole contents (but still can return
hightlights)
...this might be more efficient for large documents where I only display the
beginning anyway...

rows = how many results to display

fq=id:*data_cs* = filter query to only return documents where id matches *data_cs*


