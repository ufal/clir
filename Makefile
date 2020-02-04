SHELL:=/bin/bash

solr-8.4.1:
	wget http://apache.miloslavbrada.cz/lucene/solr/8.4.1/$@.tgz
	tar -zxvf $@.tgz

milosd:
	wget -r -l 1 https://www.nku.cz/scripts/rka/prehled-kontrol.asp?casovyfiltr=6

# download all de audits
# this probably does not work -- need to go one level deeper and to an
# external website etc
denku:
	for i in `seq 1 28`; do wget -r -l 1 https://www.eurosai.org/en/databases/audits/index.html?page=$i'&filterLanguage16=on'; done

pecina-nku:
	mkdir $@; cd $@; wget http://ufallab.ms.mff.cuni.cz/~rosa/elitr/nku.zip; unzip nku.zip; for f in C*.zip; do unzip $$f; done

kon-zavery.zip:

kon-zavery:
	wget http://ufallab.ms.mff.cuni.cz/~rosa/elitr/$@.zip
	unzip $@.zip
	for f in kon-zavery/*.pdf; do pdftotext $$f; done
	mv kon-zavery/*txt kon-zavery-txt/

kon-zavery-details:
	mkdir $@
	for d in www.nku.cz/scripts/rka/detail*; do p=$${d:44:7}; t=$${p/'%2F'/0}; cp "$$d" $@/K$$t.html; done

