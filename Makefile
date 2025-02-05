SHELL:=/bin/bash

solr-8.11.1:
	wget https://www.apache.org/dyn/closer.lua/lucene/solr/8.11.1/solr-8.11.1.tgz?action=download -O $@.tgz
	tar -zxvf $@.tgz

SOLR=solr-8.11.1

# 4 solr nodes on ports 8971 8972 8973 8974,
# first node with embedded zookeper at port 9971
C=example/cloud
solr-start:
	cd $(SOLR); z=''; \
	for n in 1 2 3 4; do \
		mkdir -p $C/node$$n/solr; \
		cp server/solr/solr.xml $C/node$$n/solr/; \
		cp server/solr/zoo.cfg $C/node$$n/solr/; \
		bin/solr start -V -cloud -p 897$$n -s $C/node$$n/solr $$z; \
		z='-z localhost:9971'; \
	done;

solr-create:
	cd $(SOLR); \
    bin/solr create -V -p 8971 -c eurosaiall -d sample_techproducts_configs -s 4 -rf 4

solr-post:
	cd $(SOLR); \
	bin/post -p 8971 -c eurosaiall ../data/data_??/source_??/nku_??/????/*txt

solr-status:
	cd $(SOLR); \
	bin/solr status

solr-ports:
	-lsof -Pi :9971 -sTCP:LISTEN -t
	-lsof -Pi :8971 -sTCP:LISTEN -t
	-lsof -Pi :8972 -sTCP:LISTEN -t
	-lsof -Pi :8973 -sTCP:LISTEN -t
	-lsof -Pi :8974 -sTCP:LISTEN -t

solr-lynx:
	lynx http://localhost:8971/solr/

solr-stop:
	cd $(SOLR); \
	bin/solr stop -all

apache-status:
	sudo systemctl status apache2.service

apache-start:
	sudo systemctl start apache2.service

apache-stop:
	sudo systemctl stop apache2.service

# restart = stop and start

# bin/solr delete -c eurosaiall

index.html: webapp/index.py
	cd webapp; python3 index.py | tail -n +3 > index.html

venv:
	cd webapp; python3 -m venv venv

wgetdata:
	wget http://ufallab.ms.mff.cuni.cz/~rosa/elitr/data.tar.gz
	tar -zxvf data.tar.gz

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



#cd kon-zavery-txt; for f in K[01]*.txt; do p=$${f/.txt/.pdf}; y=20$${f:1:2};

NKU_CS=data/data_cs/source_cs/nku_cs
# 1993 .. 2019
nku_cs:
	for y in `seq 93 99`; do \
		d=$(NKU_CS)/19$$y; mkdir -p $$d; \
		cp kon-zavery/K$$y*.pdf $$d; cp kon-zavery-txt/K$$y*.txt $$d; done;
	for y in `seq 0 9`; do \
		d=$(NKU_CS)/200$$y; mkdir -p $$d; \
		cp kon-zavery/K0$$y*.pdf $$d; cp kon-zavery-txt/K0$$y*.txt $$d; done; 
	for y in `seq 10 19`; do \
		d=$(NKU_CS)/20$$y; mkdir -p $$d; \
		cp kon-zavery/K$$y*.pdf $$d; cp kon-zavery-txt/K$$y*.txt $$d; done;

nku_cs_list:
	cd kon-zavery-details; for f in *.html; do \
		n=$$(grep -o '<h2>[^<]*</h2>' $$f | sed -e 's@</*h2>@@g' | head -n 1); \
		m=$${f%.html}; echo -e "$$m\t$$n"; \
		done > ../$(NKU_CS)/namelist.csv

nku_cs_metadata:
	cd $(NKU_CS); for y in `seq 2018 -1 1993`; do \
	../../../../metadata_cs.sh $$y; done

wmt19-elitr-testsuite:
	git clone git@github.com:ELITR/wmt19-elitr-testsuite.git

data:
	for d in cs de en fr; do for s in cs de en fr; do for n in cs de en fr; do mkdir -p data/data_$$d/source_$$s/nku_$$n;done;done;done

NKU_BE=data/data_fr/source_fr/nku_be

# french metadata:
# https://www.ccrek.be/FR/Publications/ApercuChronologique.html?year=2014
# Not clear if the listing of documents is the same or different...

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

belgium-metadata:
	# cd $(NKU_BE); for y in `seq 1998 2020`; do
	cd $(NKU_BE); for y in `seq 1998 2018`; do \
	../../../../metadata.sh $$y; done

