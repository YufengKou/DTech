# -*- coding: utf-8 -*-
"""
Created on Wed May 17 13:49:42 2017

@author: ykou
"""

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert(fname, pages=None):
   if not pages:
      pagenums = set()
   else:
      pagenums = set(pages)

   output = StringIO()
   manager = PDFResourceManager()
   converter = TextConverter(manager, output, laparams=LAParams())
   interpreter = PDFPageInterpreter(manager, converter)
   infile = open(fname, 'rb')

   for page in PDFPage.get_pages(infile, pagenums):
      interpreter.process_page(page)

   infile.close()
   converter.close()
   text = output.getvalue()
   output.close()

   return text 

def pdf_to_text(pdf_file, text_file):
    text = convert(pdf_file)
    with open(text_file, 'w') as f:
        f.write(text)
        
def test():
    pdf_file = "../../documents/chapter_7.pdf"
    text_file = "../../documents/chapter_7.txt"
    pdf_to_text(pdf_file, text_file)


if __name__ == "__main__":
    test()
    