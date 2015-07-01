#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement
from PyQt5.QtWidgets import QListWidget, QWidget, QApplication, QPushButton, \
QHBoxLayout, QGridLayout, QAbstractItemView, QMessageBox, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
import os.path
from io import open

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
 
        # Set up the first list (elements that can be used)
        elements = QListWidget()
        elements.viewport().setAcceptDrops(True)
        elements.setDragEnabled(True)
        elements.setDefaultDropAction(Qt.MoveAction)
        elements.setSelectionMode(QAbstractItemView.ExtendedSelection)
        elements.addItem(u"Last Name")
        elements.addItem(u"First Name")
        elements.addItem(u"Middle Initial")
        elements.addItem(u"Full Name")
        elements.addItem(u"DMIS ID")
        elements.addItem(u"SPIN Number")
        elements.addItem(u"SSN Prefix")
        elements.addItem(u"Social Security Number")
        elements.addItem(u"Date of Birth")
        elements.addItem(u"Gender")
        elements.addItem(u"Accession")
        elements.addItem(u"Isolation Date")
        elements.addItem(u"Culture Type")
        elements.addItem(u"Source")
        elements.addItem(u"Location Type")
        elements.addItem(u"Location")
        elements.addItem(u"Isolate Number")
        elements.addItem(u"Organism Name")
        elements.addItem(u"Alternate Organism Name")
        elements.addItem(u"Equipment")
        elements.addItem(u"Drug Info")
        elements.addItem(u"ESBL")
        elements.addItem(u"AMPC")


        # Set up the second list (elements to generate a config file from)
        self.selected_elements = QListWidget()
        self.selected_elements.viewport().setAcceptDrops(True)
        self.selected_elements.setDragEnabled(True)
        self.selected_elements.setDefaultDropAction(Qt.MoveAction)
        self.selected_elements.setSelectionMode(QAbstractItemView.ExtendedSelection)

        ok_button = QPushButton(u"OK")
        cancel_button = QPushButton(u"Cancel")
        about_button = QPushButton(u"About")
        insert_blank_line_button = QPushButton(u"Insert blank line")
        drug_validator = QIntValidator(1, 999)
        self.drugs = QLineEdit("1")
        self.drugs.setValidator(drug_validator)
        drugs_label = QLabel("Number of drugs per line")
        self.drugformat = QLineEdit("MIC,Call")
        drugformat_label = QLabel("Format of the drug information")
        self.date = QLineEdit("MM/dd/yyyy")
        date_label = QLabel("Date format")
        buttons = QHBoxLayout()

        ok_button.clicked.connect(self.export_parser)
        cancel_button.clicked.connect(self.close_program)
        about_button.clicked.connect(self.about)
        insert_blank_line_button.clicked.connect(self.insert_blank_line)
        self.drugs.setMaxLength(3)

        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        buttons.addWidget(about_button)
        buttons.addWidget(insert_blank_line_button)
 
        mainLayout = QGridLayout()
        mainLayout.addWidget(elements, 0, 0)
        mainLayout.addWidget(self.selected_elements, 0, 1)
        mainLayout.addLayout(buttons, 1, 0)
        mainLayout.addWidget(self.drugs, 2, 0)
        mainLayout.addWidget(drugs_label, 2, 1)
        mainLayout.addWidget(self.drugformat, 3, 0)
        mainLayout.addWidget(drugformat_label, 3, 1)
        mainLayout.addWidget(self.date, 4, 0)
        mainLayout.addWidget(date_label, 4, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle(u"RevealerParserWizard")
        
    def export_parser(self):
        u'''
        Extract the text of the elements in selected_elements, then pass them
        to write_output so they can be fully converted and written to a parser
        file.
        '''
        extracted_elements = []
        element_num = self.selected_elements.count()
        if element_num < 1:
            no_entries = QMessageBox()
            no_entries.setIcon(QMessageBox.Warning)
            no_entries.setText(u"No elements selected!")
            no_entries.exec_()
            return
        for i in xrange(0, element_num):
            extracted_elements.append(self.selected_elements.item(i).text())
        
        # Act like a clown and get knocked down
        if int(self.drugs.text()) < 1:
            too_small = QMessageBox()
            too_small.setIcon(QMessageBox.Warning)
            too_small.setText(u"'Drugs per line' must be between 1 and 999")
            too_small.exec_()
            return
        else:
            extracted_elements.append("Drugs per line" + '\t' + self.drugs.text())
            
        if (len(self.drugformat.text()) < 1):
            too_small = QMessageBox()
            too_small.setIcon(QMessageBox.Warning)
            too_small.setText(u"'Drug Info Format' must not be empty")
            too_small.exec_()
            return
        else:
            extracted_elements.append("Drug Info Format" + '\t' + self.drugformat.text())

        extracted_elements.append("Date Format" + '\t' + self.date.text())
            
        
        if os.path.isfile(u"my_parser.txt"):
            output_exists = QMessageBox()
            output_exists.setIcon(QMessageBox.Warning)
            output_exists.setText(u"my_parser.txt already exists! Overwrite?")
            output_exists.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            overwrite = output_exists.exec_()
            if overwrite == QMessageBox.Yes:
                with open(u"my_parser.txt", u'w') as output:
                    self.write_output(output, extracted_elements)
                    return
            else:
                sys.exit()
        else:
            with open(u"my_parser.txt", u'w') as output:
                self.write_output(output, extracted_elements)
                return
            
    def write_output(self, output, elements):
        u'''
        Given a List of strings, convert them into an MDRevealer custom parser
        file and write them to my_parser.txt.
        '''
        i = 0
        for e in elements:
            if not "Drugs per" in e:
                output.write(e + u'\t' + unicode(i) + u'\n')
            else:
                output.write(e + u'\n')
            i += 1
        success = QMessageBox()
        success.setText(u"my_parser.txt written successfully.")
        success.exec_()
        sys.exit()
                
    
    def close_program(self):
        u'''
        Close the program.
        '''
        sys.exit()
        
    def about(self):
        u'''
        Provide information about the program in a QMessageBox.
        '''
        QMessageBox.information(self, u"About RevealerParserWizard", u"aBaJ! I have" +
         u"n't filled this in yet!")
        
    def insert_blank_line(self):
        u'''
        Adds a blank line to selected_elements, for handling fields in the file
        to parse that Revealer doesn't read.
        '''
        self.selected_elements.addItem(u"(skip)")
        
if __name__ == u'__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_())
