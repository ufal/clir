SHELL:=/bin/bash

solr-8.4.1:
	wget http://apache.miloslavbrada.cz/lucene/solr/8.4.1/$@.tgz
	tar -zxvf $@.tgz

ebook-convert:
	sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin

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

kon-zavery-txt-pdftotext:
	for f in kon-zavery/*.pdf; do pdftotext $$f; done
	mkdir $@
	mv kon-zavery/*txt $@/

kon-zavery-txt:
	mkdir -p $@
	for f in kon-zavery/*.pdf; do a=$${f%.pdf}; ebook-convert $$a.pdf $${a/kon-zavery/$@}.txt; done > calibre-conversion.log


kon-zavery-txt-fillmissing:
	for f in kon-zavery/*.pdf; do a=$${f%.pdf}; b=$${a/kon-zavery/kon-zavery-txt}; if [ ! -s $$b.txt ] ; then echo $$a; pdftotext $$a.pdf; mv $$a.txt $$b.txt; fi; done

kon-zavery-details:
	mkdir $@
	for d in www.nku.cz/scripts/rka/detail*; do p=$${d:44:7}; t=$${p/'%2F'/0}; cp "$$d" $@/K$$t.html; done

wmt19-elitr-testsuite:
	git clone git@github.com:ELITR/wmt19-elitr-testsuite.git

data:
	for d in cs de en fr; do for s in cs de en fr; do for n in cs de en fr; do mkdir -p data/data_$$d/source_$$s/nku_$$n;done;done;done

NKU_BE=data/data_fr/source_fr/nku_be

belgium-lists:
	mkdir -p data/data_fr/source_fr/nku_be;
	cd $(NKU_BE); for y in `seq 1997 2020`; do wget https://www.ccrek.be/EN/Publications/ChronologicalOrder.html?year=$$y -O list.$$y.html;done

belgium-linklist:
	cd $(NKU_BE); for y in `seq 1997 2020`; do \
		sed -n '/ LIST/,/ \/LIST/p' list.$$y.html | grep -o '<a[^<]*French[^<]*</a>' > linklist.$$y.html; \
		done

belgium-csv:
	cd $(NKU_BE); for y in `seq 1997 2020`; do \
		sed -e 's/<a href="//' -e 's/" title="/\t/' -e 's/">.*//' linklist.$$y.html |grep pdf > linklist.$$y.csv; \
		done

belgium-files:
	cd $(NKU_BE); for y in `seq 1997 2020`; do \
		mkdir -p $$y; cut -f1 linklist.$$y.csv | wget -i - -P $$y; sleep 15 ; done

belgium-txt:
	cd $(NKU_BE); for y in `seq 1997 2020`; do \
		for f in $$y/*.pdf; do pdftotext $$f; done; done

# TODO skip large files
belgium-txt-calibre:
	cd $(NKU_BE); for y in `seq 1997 2020`; do \
		for f in $$y/*.pdf; do ebook-convert $$f $${f/.pdf/.txt}; done; done > calibre-conversion.log



