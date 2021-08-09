#!/usr/bin/env python
"""
This program is a web scraping robot to obtain data from a web application and save it to an excel datasheet.
"""

# Import necessary modules
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# Infos about the program
__author__ = "Rafael Seicali Malcervelli"

# Globals
counter = 0
url = "https://esaj.tjsp.jus.br/cjpg/"
contador = 0
dicData = {}
listaProcessos = []

# Web driver from google chrome. In case of any problems, download the driver
# from this website: https://sites.google.com/a/chromium.org/chromedriver/downloads
# and then put the file in the folder below.
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Requests
chrome = webdriver.Chrome(PATH)
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

dfFinal.to_excel("processos.xlsx") #7)
chrome.close()
# -------Transfer into an Excel datasheet----

# ---------Downloading PDF files-------------
# chrome.find_element_by_xpath('//*[@id="divDadosResultado"]/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/a[2]').click()
# chrome.switch_to.window(chrome.window_handles[1])
# new = chrome.current_url
# options = webdriver.ChromeOptions()
# options.add_experimental_option('prefs', {
# "download.default_directory": "E:\Documents\internChallenge\files", #Change default directory for downloads
# "download.directory_upgrade": True, 'profile.managed_default_content_settings.javascript': 2
# })

# chrome = webdriver.Chrome(PATH, options=options)

# chrome.get(new)
# time.sleep(5)
# chrome.find_element_by_id("download").click()

# ---------Downloading PDF files-------------


