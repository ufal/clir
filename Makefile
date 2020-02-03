
solr-8.4.1:
	wget http://apache.miloslavbrada.cz/lucene/solr/8.4.1/$@.tgz
	tar -zxvf $@.tgz

milosd:
	cd milos
	wget -r -l 1 https://www.nku.cz/scripts/rka/prehled-kontrol.asp?casovyfiltr=6
