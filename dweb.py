from nturl2path import url2pathname
import tempfile
from turtle import update
from unittest import result
from urllib.parse import urlparse
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
from array import*
from urlextract import URLExtract
from PyQt5.QtWidgets import QToolBar
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pickle
from configparser import ConfigParser

config = ConfigParser()

home = str(Path.home())
temp = tempfile.TemporaryFile()
temp_dir = tempfile.gettempdir()

###settings###########
###settings###########

def load_settings_data():
    config.read(home +"/.dweb/dweb-settings.ini",[DEFAULT_settings])

homepage_url = "https://www.google.com"
default_font_size = 20
style_sheet = """
            background-color: #3b393c;
            color: #f7f7f5;
            font-size:20px;
            """

######################
######################

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok 
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Dustin's Web-Browser")
        font = title.font()
        font.setPointSize(default_font_size)
        title.setFont(font)

        layout.addWidget(title)
        layout.addWidget(QLabel("Version .01.01 1/21/2021"))
        layout.addWidget(QLabel("Copyright 2021 MassConceptZ"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(default_font_size, default_font_size))
        self.addToolBar(navtb)
###BACK
        back_btn = QAction(QIcon(os.path.join('/opt/dweb/images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
###NEXT
        next_btn = QAction(QIcon(os.path.join('/opt/dweb/images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
###RELOAD
        reload_btn = QAction(QIcon(os.path.join('/opt/dweb/images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
###STOP
        stop_btn = QAction(QIcon(os.path.join('/opt/dweb/images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
###HOME
        home_btn = QAction(QIcon(os.path.join('/opt/dweb/images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()
###NEW TAB
        new_tab_action = QAction(QIcon(os.path.join('/opt/dweb/images','ui-tab--plus.png')),"New Tab", self)
        new_tab_action.setStatusTip('New Tab')
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        navtb.addAction(new_tab_action)
        
        navtb.addSeparator()
###NAV BAR
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('/opt/dweb/images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
###BOOKMARKS
        new_tab_action = QAction(QIcon(os.path.join('/opt/dweb/images','bookmark2.png')),"Create Bookmark", self)
        new_tab_action.setStatusTip('Bookmark This Page')
        new_tab_action.triggered.connect(lambda _: self.create_bookmark())
        navtb.addAction(new_tab_action)

        new_tab_action = QAction(QIcon(os.path.join('/opt/dweb/images','bookmark.png')),"Bookmarks", self)
        new_tab_action.setStatusTip('Your Bookmarks')
        new_tab_action.triggered.connect(lambda _: self.bookmark_tab())
        navtb.addAction(new_tab_action)

###
###
###FILE MENU
###
###
        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        settings_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'ui-tab--plus.png')), "Settings", self)
        settings_action.setStatusTip("Settings")
        settings_action.triggered.connect(self.settings)
        file_menu.addAction(settings_action)

        exitButton = QAction('EXIT', self)
        file_menu.addAction(exitButton)
        exitButton.triggered.connect(self.close)

###
###
###HELP MENU
###
###
        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'question.png')), "About Dustin's Web-Browser", self)
        about_action.setStatusTip("Find out more about Dustin's Web-Browser")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_massconceptz_action = QAction(QIcon(os.path.join('/opt/dweb/images', 'massconceptz.png')),
                                            "Massconceptz", self)
        navigate_massconceptz_action.setStatusTip("Go to MassConceptZ Homepage")
        navigate_massconceptz_action.triggered.connect(self.navigate_massconceptz)
        help_menu.addAction(navigate_massconceptz_action)

###
###
###

        navtb.addSeparator()

###
###
###
        self.add_new_tab(QUrl(homepage_url), 'Homepage')

        self.show()

        self.setWindowTitle("Dustin's Web_browser")

        self.setStyleSheet(style_sheet)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl(homepage_url)

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

###
######BOOKMARKS
###

    def bookmark_tab(self, qurl="Bookmarks", label="Bookmarks"):
        import read_bookmarks
        if qurl == "Bookmarks":
            qurl = QUrl("file://" + home +"/.dweb/bookmarks.dat")
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def create_bookmark(self):
        if QUrl(self.urlbar.text()) != 'home +"/.dweb/bookmarks.dat"':
            f = QUrl(self.urlbar.text())
            bookmarked_save = str(f)
            file_object = open(home +"/.dweb/bookmarks.dat",'a')
            file_object.write(bookmarked_save)
            file_object.write("\n") 
            file_object.close()

    def load_settings_data():
        config.read("dweb-settings.ini")

    def settings(x,y):
        import dweb_settings

 ###
                                
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Dustin's Web-Browser" % title)

    def navigate_massconceptz(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.massconceptz.com"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(homepage_url))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('/opt/dweb/images', 'lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('/opt/dweb/images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("Dustin's Web Browser")
app.setOrganizationName("Massconceptz")
app.setOrganizationDomain("massconceptz.com")

window = MainWindow()

app.exec_()
