#!/usr/bin/env python
"""
This program is a web scraping robot to obtain data from a web application and save it to an excel datasheet.
"""

# Import necessary modules
import os, time, requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from PyPDF2 import PdfFileReader
import numpy as np

# Infos about the program
__author__ = "Rafael Seicali Malcervelli"

# Globals
counter = 0
url = "https://esaj.tjsp.jus.br/cjpg/"
contador = 0
dicData = {}
listaProcessos = []

# Functions
def extract_information(pdf_path):
    dicProcesso = {}

    pdf_file = open(pdf_path, 'rb')
    read_pdf = PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}:
    """
    listaTexto = []
    for i in range(number_of_pages):
        listaTexto.append(read_pdf.getPage(i).extractText())
    
    dicProcesso["Texto PDF"] = ','.join(listaTexto)
    pdf_file.close()

    return dicProcesso

# Web driver from google chrome. In case of any problems, download the driver
# from this website: https://sites.google.com/a/chromium.org/chromedriver/downloads
# and then put the file in the folder below.
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Requests
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "E:\Documents\internChallenge\pdfs", 
"download.directory_upgrade": True
})
chrome = webdriver.Chrome(PATH, options=options)
chrome.get(url) # 1)

# Script
pesquisa = chrome.find_element_by_id("iddadosConsulta.pesquisaLivre")
classe = chrome.find_element_by_id("classe_selectionText")
livre = chrome.find_element_by_class_name("esajTituloPagina")
dataInicio = chrome.find_element_by_id("iddadosConsulta.dtInicio")
dataFim = chrome.find_element_by_id("iddadosConsulta.dtFim")
pesquisar = chrome.find_element_by_id("pbSubmit")

# Robot actions
# -----------------Pesquisa------------------
pesquisa.send_keys("covid") # 2)

classe.send_keys("Despejo") # 3)
livre.click()
time.sleep(2)
tickItem = chrome.find_element_by_id("classe_tree_node_8554")
tickItem.click()
selecionar = chrome.find_element_by_xpath('//*[@id="classe_treeSelectContainer"]/div[3]/table/tbody/tr/td/input[1]')
selecionar.click()


dataInicio.send_keys("01/01/2020") # 4)
dataFim.send_keys("31/12/2020") # 4)
pesquisar.click()

time.sleep(2)
# -----------------Pesquisa------------------

# -----------Getting data from HTML----------
soupURL = chrome.current_url
page = requests.get(soupURL)
soup = BeautifulSoup(page.content, "html.parser")

tableProcessos = soup.find("td", {"id": "tdResultados"})
itemsTable = tableProcessos.table.find_all("tr", {"class": "fundocinza1"})
firstProcess = itemsTable[0].table.find_all("tr", {"class": "fonte"})

# Filter data
for j in itemsTable:
    process = j.table.find_all("tr", {"class": "fonte"})
    for i in process:
        if contador == 0:
            # Numero do processo
            a = i.td.text.strip()
            dicData["Processo"] = ' '.join(a.split())
            contador += 1
        elif contador > 7:
            pass
        else:
            a = i.td.text.strip()
            dicData[' '.join(a.split()).split(':')[0]] = ' '.join(a.split()).split(':')[1][1:]
            contador += 1
    listaProcessos.append(dicData)
    dicData = {}
    contador = 0
# -----------Getting data from HTML----------

# -------Transfer into an Excel datasheet----
frames = []

for i in range(len(listaProcessos)):
    df = pd.DataFrame.from_dict([listaProcessos[i]])
    frames.append(df)
dfFinal = pd.concat(frames).reset_index(drop=True)


# -------Transfer into an Excel datasheet----

# ---------Downloading PDF files-------------
# Conforme conversado, o downlaod dos pdfs sao realizados manualmente, com um pedido de
# um CAPTCHA ao final pelo terminal. 
captcha = input("[?] Downloaded all PDFs? [y/n] ")

if captcha == "y":
    listPDFs = os.listdir("E:\Documents\internChallenge\pdfs")
    dicProcessosTexto = {}

    for pdf in listPDFs:
        dicionario = extract_information("E:\Documents\internChallenge\pdfs" + "\{}".format(pdf))
        # Changing filename to proccess number
        numeroProcesso = dicionario["Texto PDF"][dicionario["Texto PDF"].find("Processo Digital nº:")+20:dicionario["Texto PDF"].find("Processo Digital nº:")+45]
        if numeroProcesso[0] == "1":
            filename = "E:\Documents\internChallenge\pdfs" + '\{}'.format(pdf)
            newFileName = "\{}.pdf".format(numeroProcesso)

            os.rename(filename, "E:\Documents\internChallenge\pdfs{}".format(newFileName))

            # Adding text from PDF to database
            dicProcessosTexto[numeroProcesso] = dicionario["Texto PDF"]
        else:
            numeroProcesso = dicionario["Texto PDF"][dicionario["Texto PDF"].find("Processo nº:")+12:dicionario["Texto PDF"].find("Processo nº:")+37]

            if numeroProcesso[0] != "1":
                numeroProcesso = dicionario["Texto PDF"][dicionario["Texto PDF"].find("Processo:")+9:dicionario["Texto PDF"].find("Processo:")+34]


                filename = "E:\Documents\internChallenge\pdfs" + '\{}'.format(pdf)
                newFileName = "\{}.pdf".format(numeroProcesso)


                os.rename(filename, "E:\Documents\internChallenge\pdfs{}".format(newFileName))

                # Adding text from PDF to database
                dicProcessosTexto[numeroProcesso] = dicionario["Texto PDF"]
                continue

            filename = "E:\Documents\internChallenge\pdfs" + '\{}'.format(pdf)
            newFileName = "\{}.pdf".format(numeroProcesso)

            os.rename(filename, "E:\Documents\internChallenge\pdfs{}".format(newFileName))

            # Adding text from PDF to database
            dicProcessosTexto[numeroProcesso] = dicionario["Texto PDF"]


dfFinal["PDF"] = dfFinal["Processo"].map(dicProcessosTexto)

dfFinal.to_excel("processos.xlsx") #7)
# ---------Downloading PDF files-------------

chrome.close()
