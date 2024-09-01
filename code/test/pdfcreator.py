# coding: utf-8
import aspose.pdf as ap

for i in range(8):

    document = ap.Document()

    document.pages.add()

    document.save("generated/output" + str(i) + ".pdf")