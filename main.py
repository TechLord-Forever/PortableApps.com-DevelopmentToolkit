#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from qt import QtCore, QtGui
from ui.mainwindow import Ui_MainWindow
from utils import _, center_window
import paf
import paf.validate_gui
import paf.validate_cli
import config
import warnings
import warn
import appinfo
from functools import wraps


def assert_valid_package_path(func):
    """Decorator to make sure that something which shouldn't ever happen
    doesn't cause a crash, and to provide a code indication of what's
    happening."""
    @wraps(func)
    def decorate(self, *args, **kwargs):
        if not paf.valid_package(unicode(self.ui.packageText.text())):
            raise Exception("The package is not valid.")

        func(self, *args, **kwargs)
    return decorate


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.packageText.setFocus()

    @QtCore.Slot(bool)
    def on_packageButton_clicked(self, checked):
        "Select a package."
        text_box = self.ui.packageText
        current_path = text_box.text()
        text_box.setText(QtGui.QFileDialog.getExistingDirectory(None,
            _("Select a portable app package"), current_path) or current_path)

    @QtCore.Slot(bool)
    def on_createButton_clicked(self, checked):
        "Create a package."
        self.ui.statusBar.showMessage(_("Creating package..."))
        text_box = self.ui.packageText
        current_path = text_box.text()
        while True:
            package = QtGui.QFileDialog.getExistingDirectory(None,
                    _("Create a directory for the package"))
            if package:
                try:
                    paf.create_package(unicode(package))
                except paf.PAFException as e:
                    QtGui.QMessageBox.critical(self,
                            _('PortableApps.com Development Toolkit'),
                            unicode(e), QtGui.QMessageBox.Ok)
                    continue

                text_box.setText(package)
                self.ui.statusBar.showMessage(
                        _("Package created successfully."), 2000)
                self.on_detailsButton_clicked(False)
            else:
                self.ui.statusBar.clearMessage()
            break

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_detailsButton_clicked(self, checked):
        "Edit PortableApps.com Format details."
        appinfo_dialog = appinfo.AppInfoDialog()
        center_window(appinfo_dialog)
        appinfo_dialog.load_package(paf.Package(
            unicode(self.ui.packageText.text())))
        appinfo_dialog.setModal(True)
        appinfo_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self.dialog = appinfo_dialog

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_validateButton_clicked(self, checked=None):
        "Validate the app."
        validate_dialog = paf.validate_gui.validate(self.ui.packageText.text())
        center_window(validate_dialog)
        validate_dialog.setModal(True)
        validate_dialog.show()
        # Keep a reference to it so it doesn't get cleaned up
        self.dialog = validate_dialog

    @QtCore.Slot(bool)
    @assert_valid_package_path
    def on_installerButton_clicked(self, checked=None):
        "Edit PortableApps.com Installer details."
        not_implemented()

    def on_packageText_textChanged(self, string):
        """
        Enable or disable the buttons below based on whether the text is a
        valid directory. This is used instead of a validator so it can do
        something without being overly hacky.
        """
        valid = paf.valid_package(unicode(string))
        self.ui.detailsButton.setEnabled(valid)
        self.ui.validateButton.setEnabled(valid)
        self.ui.installerButton.setEnabled(valid)


def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()

    window.ui.packageText.setText(config.get('Main', 'Package', ''))

    center_window(window)
    window.show()
    warn.set_warnings_qt()
    exit_code = app.exec_()

    prepare_quit(window)

    return exit_code


def prepare_quit(window):
    config.settings.Main.Package = window.ui.packageText.text()
    config.save()


def cli_help():
    print "PortableApps.com Development Toolkit"
    print "Launch without command line arguments to run normally."
    print
    print 'Validate a package (GUI):'
    print '  %s validate <package>' % sys.argv[0]
    print
    print 'Validate a package (command line):'
    print '  %s validate-cli <package>' % sys.argv[0]
    return 0


def validate_gui():
    app = QtGui.QApplication(sys.argv)
    window = paf.validate_gui.validate(sys.argv[2])
    exit_code = app.exec_()

    return exit_code


def validate_cli():
    return paf.validate_cli.validate(sys.argv[2])


def not_implemented():
    warnings.warn('Sorry, this is not implemented yet.',
            UserWarning, stacklevel=2)


if len(sys.argv) > 1:
    if sys.argv[1] == 'help':
        action = cli_help
    elif sys.argv[1] == 'validate':
        action = len(sys.argv) == 3 and validate_gui or cli_help
    elif sys.argv[1] == 'validate-cli':
        action = len(sys.argv) == 3 and validate_cli or cli_help
    else:
        action = main
else:
    action = main

if __name__ == "__main__":
    sys.exit(action())
