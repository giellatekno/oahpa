# -*- coding:utf-8 -*-
'''
Script to convert xml into csv.
Usage:
    python3 xml2csv.py <PATH_XML_FILE>
A csv file named <pos>_out.csv is generated in this folder.
<pos> is extracted from <PATH_XML_FILE>, expected name is <pos>_<whatever>.xml
'''

import sys
import csv
import xml.etree.ElementTree as ET

read_file = sys.argv[1]
pos_read_file = read_file.split("/")[len(read_file.split("/"))-1].split("_")[0]
out_file = pos_read_file + "_out.csv"
write_file = open(out_file,"a+")
write_file.write("Lemma" + "\t" + "Attrsuffix" + "\t" + "Diphthong" + "\t" + "Gen_only" + "\t" + "Gradation" + "\t" + "Pos" + "\t" + "Rime" + "\t" + "Soggi" + "\t" + "Stem" + "\t" + "Type" + "\t" + "Dialect" + "\t" + "Books" + "\t" + "Sem_class" + "\t" + "Trans (nob)" + "\t" + "Trans (fin)" + "\t" + "Trans (swe)" + "\t" + "Trans (eng)" + "\n")

tree = ET.parse(read_file)
root = tree.getroot()

for e in root.findall("e"):
    line = ""
    line += e.find("lg/l").text + "\t"
    if e.find("lg/l").get("attrsuffix"):
        line += e.find("lg/l").get("attrsuffix") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("diphthong"):
        line += e.find("lg/l").get("diphthong") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("gen_only"):
        line += e.find("lg/l").get("gen_only") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("gradation"):
        line += e.find("lg/l").get("gradation") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("pos"):
        line += e.find("lg/l").get("pos") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("rime"):
        line += e.find("lg/l").get("rime") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("soggi"):
        line += e.find("lg/l").get("soggi") + "\t"
    if e.find("lg/l").get("stem"):
        line += e.find("lg/l").get("stem") + "\t"
    else: line += " - " + "\t"
    if e.find("lg/l").get("type"):
        line += e.find("lg/l").get("type") + "\t"
    else: line += " - " + "\t"
    if e.find("dialect"):
        line += e.find("dialect").get("class") + "\t"
    else: line += " - " + "\t"
    books = ""
    for book in e.findall("sources/book"):
        books += book.get("name") + ", "
    line += books + "\t"
    if e.find("mg/semantics/sem"):
        line += e.find("mg/semantics/sem").get("class") + "\t"
    else: line += " - " + "\t"
    trans = ""
    for tg in e.findall("mg/tg"):
        trans += tg.find("t").text + "\t"
    line += trans
    write_file.write(line + "\n")

write_file.close()
