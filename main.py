#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""
main.py

Main module for translating the document..
Fixed a bit from https://github.com/aquacode/translate-pdf
"""
import time
import argparse
from papago import Papago, check_language
# pdftotext
# apt-get install libpoppler-cpp-dev libpoppler-dev
import pdftotext

def getListOfTextFromPdf(fileinput):
    print("getListOfTextFromPdf for file: {}".format(fileinput))
    with open(fileinput, "rb") as f:
        pagesAsListOfText = pdftotext.PDF(f)
    return pagesAsListOfText


def translateEachTextToTarget(pagesOfText, target, outputfile):
    print("translateEachTextToTarget language: {}".format(target))
    start = time.time()
    index = 1
    total = 0
    result_file = open(outputfile, "w")
    #     print(Papago.translate_text("ja", "ko", "みくる可愛い"))
    for text in pagesOfText:
        print("Page {}".format(index))
        chars = len(text)
        total += chars
        print("Number of characters of current page: {}".format(chars))
        print("Total chars so far (before reaching 100,000): {}".format(total))
        if total >= 100000:
            end = time.time()
            elapsed = end - start
            diff = 100 - elapsed
            print("Reached 100,000 in {} seconds!".format(elapsed))
            if diff > 0:
                print("Waiting {} seconds to continue".format(diff))
                time.sleep(diff)
                start = time.time()
                total = 0
        translated_text = Papago.translate_text("ja", "ko", text)
        print(u"{}".format(translated_text))
        print("\n\n")
        result_file.write("Page {}".format(index))
        result_file.write("\n---------\n")
        result_file.write(u"{}".format(translated_text))
        result_file.write("\n\n")
        index += 1
    result_file.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("fileinput", help="Enter the PDF file name containing the text to translate")
    argparser.add_argument("target", help="Enter the target language to which the text should be translated")
    argparser.add_argument("fileoutput", help="Enter the file name for the translated results")
    args = argparser.parse_args()
    pagesOfText = getListOfTextFromPdf(args.fileinput)
    translateEachTextToTarget(pagesOfText, args.target, args.fileoutput)
