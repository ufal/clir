

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


* sloučení rodiny
* family reunification
* Familienzusammenführung
* regroupement familial

DONE??: stránkování výsledků (anebo rovnou zobrazovat všechny)
...zobrazuju 100 výsledků, což by mělo stačit

DONE: návrty na předchozí stránky
...zrušeno `target=_blank` a logo vede na main page

DONE: viewdoc i bez metadat

DONE: highligh case insensitive

DONE: metadata cs

DONE: rozdělit podle jazyka vyhledávání
- ideálně přidat nějakej parametr do vyhledávání na to

DONE: indexnout nově přeložená data

DONE: vstupní stránky


TODO: připravit tasky


# status

* nku be: 2016-2020
* nku cs: 2019-2013 asi, bude to do 2011 až se to dopřeloži a doindexuje


## solr setup

    # solr root directory
    cd solr-8.4.1
    
    # create dir with configs (for each node)
    mkdir -p example/cloud/node1/solr/
    cp server/solr/solr.xml server/solr/zoo.cfg example/cloud/node1/solr/

    # start node at port 8971
    bin/solr start -V -cloud -p 8971 -s example/cloud/node1/solr
    # this also starts zookeeper at port+1000
    # for further nodes you need to specify it
    bin/solr start -V -cloud -p 8972 -s example/cloud/node2/solr -z localhost:9971

    # create a collection called eurosaiall
    bin/solr create -V -p 8971 -c eurosaiall -d sample_techproducts_configs -s 4 -rf 4
    # sample_techproducts_configs is a config which seems to work...
    # s and rf are some parameters that should help with loadbalancing or what...

    # index data by solr
    bin/post -p 8971 -c eurosaiall ../data/data_??/source_??/nku_??/????/*txt
    # it can also index other types of files, and also structured files in XML or JSON or CSV...
    # I am not using any of these capabilities at the moment
    # (but it would make sense to store the metadata somehow so that solr uses them directly)
    # Currently I do create *.meta files with metadata, but I only use them in
    # my scripts, I do not give them to solr

## solr management

    # stop all nodes
    bin/solr stop -all

    # start them again identically to before, e.g.
    bin/solr start -V -cloud -p 8972 -s example/cloud/node2/solr -z localhost:9971

    # delete a created collection
    bin/solr delete -c techproducts

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


