
#Python Web Scraper for Fantasy Football - Jordan Phillips 2023  
#+----------------------------------------------------------------------------------------------------------------------------------------------+                                                                              |
#|    The purpose of this tool is to provide myself with a personal tool which scrapes URLs for fantasy football data.                          |
#|    This app will grant me an advantage in Fantasy Football by seeing player trends, projecting points, and analyzing the yearly player data. |
#+----------------------------------------------------------------------------------------------------------------------------------------------+

#Techniques used:
#+--------------------------------------+
#|    Python             XAML           |
#|    PyQt5              QDesigner      |
#|    Web Scraping       Data Analysis  |
#+--------------------------------------+

#Expect a lot of comments, this is a learning project for me, so I like to have as much documentation as possible :)

#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#Libraries
#-----------------------------

#PyQt UI dependencies
from PyQt5.QtCore import QMetaObject, pyqtSlot, Q_ARG
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *

#Allows reading data from URLs
from urllib.request import urlopen
#Allows transformation of HTML into Python Objects
from bs4 import BeautifulSoup
#Allows access to data manipulation and analysis
import pandas as pd
#Needed for UI setup
import sys
#Needed for path concantenation
import os
#Needed for file paths
from pathlib import Path

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        #load UI file, replace with path to UI file if needed
        uic.loadUi("./Python_FF_UI.ui", self)
        self.show()
        #UI Widget setup
        self.Year_Select = self.findChild(QtWidgets.QComboBox, "year_select")
        self.Year_Select.activated.connect(self.getCurrentText)
        self.BrowseButton = self.findChild(QtWidgets.QPushButton, "Browse_Button")
        self.BrowseButton.clicked.connect(self.open_dir_dialog)
        self.CsvButton = self.findChild(QtWidgets.QPushButton, "CSV_Button")
        self.CsvButton.clicked.connect(self.make_csv)

        #Instantiate main variables used in the program
        self.soup = None
        self.year = ""
        self.csvPath = ""
        self.data = ""

#Functions
#-----------------------------

    #UI Functions
    #-------------------------

    #Get selected year from PyQt ComboBox
    def getCurrentText(self, i):
        global year
        ctext = self.Year_Select.currentText()
        self.year = ctext
        print(self.year)

    #Get selected directory from QFileDialog
    def open_dir_dialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        if dir_name:
            self.csvPath = Path(dir_name)
            print("File Path: ", self.csvPath)

    #Data/Output Functions
    #-------------------------

    #Setup BeautifulSoup object with URL
    #PFR's URLs are the same except for the year field, so:
    #{} is filled with self.year, which allows for simpler URL logic
    def getSoup(self):
        url = "https://www.pro-football-reference.com/years/{}/fantasy.htm".format(self.year)
        html = urlopen(url)
        self.soup = BeautifulSoup(html, "html.parser")

    #Fill "headers" with header data from URL
    def getHeaders(self):
        headers = [th.getText() for th in self.soup.findAll('tr')[1].findAll('th')]
        headers = headers[1:]
        return headers

    #Get data from the table rows in the URL
    def getData(self):
        rows = self.soup.findAll('tr', class_=lambda table_rows: table_rows != "thead")
        player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
        player_stats = player_stats[2:]
        stats = pd.DataFrame(player_stats, columns=self.headers)
        stats = stats.replace(r'', 0, regex=True)
        stats['Year'] = self.year
        return stats

    #Create CSV file using the 3 functions above
    #Directory is obtained from open_dir_dialog(), and self.year is prepended to the file name
    def make_csv(self):
        self.getSoup()
        self.headers = self.getHeaders()
        self.data = self.getData()
        print(self.year)
        name = self.year + '_FF_Player_Stats.csv'

        #try/catch for error handling
        try:
            fullpath = os.path.join(self.csvPath, name)
            self.data.to_csv(fullpath)
            print("CSV File created.")
        except:
            print("Error creating CSV File.")

#runs UI application
app = QApplication(sys.argv)
window = MainWindow()
app.exec_()