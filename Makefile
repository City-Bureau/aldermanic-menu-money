YEARS = 2012 2013 2014 2015 2016 2017 2018

URL_2012 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/March2017Update/2012Menu.pdf
URL_2013 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/March2017Update/2013Menu.pdf
URL_2014 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/March2017Update/2014Menu.pdf
URL_2015 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/March2017Update/2015Menu.pdf
URL_2016 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/2016MenuUpdatedMay2018.pdf
URL_2017 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/2017OBMMenu50WardDetailsRpt3Dec2018.pdf
URL_2018 = https://www.chicago.gov/content/dam/city/depts/obm/supp_info/CIP_Archive/Aldermanic%20Menu/2018%20Menu%20Ward%20details%20Report%20as%20of%2013May2019.pdf

PARAMS_2012 = -a 112,14,540,771 -c 290,523,623,711
PARAMS_2013 = -a 112,14,540,771 -c 290,523,623,711
PARAMS_2014 = -a 112,14,540,771 -c 290,523,623,711
PARAMS_2015 = -a 112,14,540,771 -c 290,523,623,711
PARAMS_2016 = -a 56,35,552,720 -c 247,606
PARAMS_2017 = -a 56,35,552,720 -c 258,616
PARAMS_2018 = -a 56,35,552,720 -c 247,606

GENERATED_FILES = $(foreach y, $(YEARS), output/$(y).csv)

.PHONY: all clean

.PRECIOUS: output/%.csv input/%.pdf tabula.jar

all: $(GENERATED_FILES)

clean:
	rm -f input/*.pdf input/*.csv output/*.csv

output/%.csv: input/%.csv
	cat $< | python scripts/process_pdf.py $* > $@

input/%.csv: input/%.pdf tabula.jar
	java -jar tabula.jar -p all -t $(PARAMS_$*) $< > $@

input/%.pdf:
	wget -O $@ $(URL_$*)

tabula.jar:
	wget -O $@ https://github.com/tabulapdf/tabula-java/releases/download/v1.0.2/tabula-1.0.2-jar-with-dependencies.jar
