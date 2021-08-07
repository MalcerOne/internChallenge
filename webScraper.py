#!/usr/bin/env python
"""
This program is a web scraping robot to obtain data from a web application and save it to an excel datasheet.
"""

# Import necessary modules
import requests
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

# Infos about the program
__author__ = "Rafael Seicali Malcervelli"

# Globals
counter = 0
url = "https://esaj.tjsp.jus.br/cjpg/"

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
itemsTable = tableProcessos.table.find_all("tr")
print(len(itemsTable))
# -----------Getting data from HTML----------


# Para passar para um excel, usar PANDAS



