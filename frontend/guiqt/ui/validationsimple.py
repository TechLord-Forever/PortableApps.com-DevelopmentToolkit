# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/validationsimple.ui'
#

#      by: PySide uic UI code generator
#
# WARNING! All changes made in this file will be lost!

from qt import QtCore, QtGui

class Ui_ValidationDialog(object):
    def setupUi(self, ValidationDialog):
        ValidationDialog.setObjectName("ValidationDialog")
        ValidationDialog.resize(480, 640)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ValidationDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(ValidationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.validationResultsHTML = QtGui.QTextBrowser(ValidationDialog)
        self.validationResultsHTML.setObjectName("validationResultsHTML")
        self.verticalLayout.addWidget(self.validationResultsHTML)
        self.validationResultsArea = QtGui.QPlainTextEdit(ValidationDialog)
        self.validationResultsArea.setObjectName("validationResultsArea")
        self.verticalLayout.addWidget(self.validationResultsArea)

        self.retranslateUi(ValidationDialog)
        QtCore.QMetaObject.connectSlotsByName(ValidationDialog)

    def retranslateUi(self, ValidationDialog):
        ValidationDialog.setWindowTitle(QtGui.QApplication.translate("ValidationDialog", "Validation results", None, QtGui.QApplication.UnicodeUTF8))

import graphics_rc