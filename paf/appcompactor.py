# -*- coding: utf-8 -*-

# This file is for App/AppInfo/appinfo.ini validation

import os
import sys
from subprocess import Popen
from orderedset import OrderedSet
import config
from utils import path_windows, get_ini_str
from validator.engine import INIManager, SectionValidator, FileMeta, SectionMeta, ValidatorError, StringMapping


__all__ = ['AppCompactor']


DEFAULT_CUTOFF = 4096


class AppCompactor(INIManager):
    "The manager for the AppCompactor data (appcompactor.ini)."

    module = sys.modules[__name__]

    def path(self):
        return os.path.join('App', 'AppInfo', 'appcompactor.ini')

    class Meta(FileMeta):
        mandatory = OrderedSet(('PortableApps.comAppCompactor',))
        order = OrderedSet(('PortableApps.comAppCompactor',))
        enforce_order = True  # Ha! ha!
        mappings = (
                StringMapping('PortableApps.comAppCompactor', 'Section'),
                )

    def compact(self, block=True):
        """
        Compacts a package with the PortableApps.com AppCompactor. Currently
        this runs the normal GUI (with the path filled in) and the user will
        still need to press "Go".

        Raises an ``OSError`` if run on Linux/OS X and Wine is not installed or
        PortableApps.comAppCompactor.exe does not have mode +x.

        Returns the process handle on success, or False if the PortableApps.com
        AppCompactor was not found. If something went otherwise wrong, you
        probably won't hear about it.

        The parameter ``block`` can be set to ``False`` to make this an
        asynchronous call.
        """

        appcompactor_path = config.get('Main', 'AppCompactorPath')
        if not appcompactor_path or not os.path.isfile(appcompactor_path):
            return False

        proc = Popen([appcompactor_path, path_windows(self.package.path(), True)])
        if block:
            proc.wait()

        return proc

    def load(self, do_reload=True):
        if not do_reload and self.ini:
            return

        super(AppCompactor, self).load(do_reload)

        self.files_excluded = get_ini_str(self.ini,
            'PortableApps.comAppCompactor', 'FilesExcluded', '').split('|')
        if self.files_excluded == ['']:
            del self.files_excluded[0]

        self.additional_extensions_included = get_ini_str(self.ini,
            'PortableApps.comAppCompactor', 'AdditionalExtensionsIncluded', '').split('|')
        if self.additional_extensions_included == ['']:
            del self.additional_extensions_included[0]

        self.additional_extensions_excluded = get_ini_str(self.ini,
            'PortableApps.comAppCompactor', 'AdditionalExtensionsExcluded', '').split('|')
        if self.additional_extensions_excluded == ['']:
            del self.additional_extensions_excluded[0]

        try:
            self.compression_file_size_cut_off = int(get_ini_str(self.ini,
                'PortableApps.comAppCompactor', 'CompressionFileSizeCutOff', DEFAULT_CUTOFF))
        except ValueError:
            self.compression_file_size_cut_off = DEFAULT_CUTOFF

    def save(self):
        # TODO: rethink slightly the INIManager.fix() method which is more what
        # some of this should be. Perhaps def save(self, fix=True)?
        if self.files_excluded:
            self.ini['PortableApps.comAppCompactor'].FilesExcluded = '|'.join(self.files_excluded)
        elif 'FilesExcluded' in self.ini['PortableApps.comAppCompactor']:
            del self.ini['PortableApps.comAppCompactor'].FilesExcluded

        if self.additional_extensions_included:
            self.ini['PortableApps.comAppCompactor'].AdditionalExtensionsIncluded = '|'.join(self.additional_extensions_included)
        elif 'AdditionalExtensionsIncluded' in self.ini['PortableApps.comAppCompactor']:
            del self.ini['PortableApps.comAppCompactor'].AdditionalExtensionsIncluded

        if self.additional_extensions_excluded:
            self.ini['PortableApps.comAppCompactor'].AdditionalExtensionsExcluded = '|'.join(self.additional_extensions_excluded)
        elif 'AdditionalExtensionsExcluded' in self.ini['PortableApps.comAppCompactor']:
            del self.ini['PortableApps.comAppCompactor'].AdditionalExtensionsExcluded

        if self.compression_file_size_cut_off != DEFAULT_CUTOFF:
            self.ini['PortableApps.comAppCompactor'].CompressionFileSizeCutOff = self.compression_file_size_cut_off
        elif 'CompressionFileSizeCutOff' in self.ini['PortableApps.comAppCompactor']:
            del self.ini['PortableApps.comAppCompactor'].CompressionFileSizeCutOff

        if 'PortableApps.comAppCompactor' in self.ini and len(self.ini['PortableApps.comAppCompactor']) == 0:
            del self.ini['PortableApps.comAppCompactor']

        # This is cheating, really. See note at top of method.
        if len(self.ini) == 0:
            self.delete()
        else:
            super(AppCompactor, self).save()


class Section(SectionValidator):
    class Meta(SectionMeta):
        optional = OrderedSet(('FilesExcluded', 'AdditionalExtensionsExcluded',
            'AdditionalExtensionsIncluded', 'CompressionFileSizeCutOff'))
        order = OrderedSet(('FilesExcluded', 'AdditionalExtensionsExcluded',
            'AdditionalExtensionsIncluded', 'CompressionFileSizeCutOff'))

    def CompressionFileSizeCutOff(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError()
        except ValueError:
            return ValidatorError("must be a positive integer")
