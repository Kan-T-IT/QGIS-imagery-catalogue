# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# KAN Imagery Catalog QGIS plugin
# Satellite image catalog manager

# * Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
# * begin      : 2023-07-14
# * copyright  : (C) 2023 by Fernando D. Gómez :: KAN Territory & IT
# * email      : fgomezdev@gmail.com
# * git sha    : $Format:%H$


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


import os.path

from PyQt5.QtCore import QSettings

try:
    from qgis.PyQt.QtCore import QCoreApplication, Qt, QTranslator
    from qgis.PyQt.QtGui import QIcon
    from qgis.PyQt.QtWidgets import QAction
except:  # noqa: E722    # pylint: disable=bare-except
    pass

from core.settings import PluginSettings
from kan_imagery_catalog_dock import KANImageryCatalogDock

# Initialize Qt resources from file resources.py
from resources import *  # noqa: F403, F401  # pylint: disable=wildcard-import
from utils.general import get_plugin_dir


class KANImageryCatalog:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = get_plugin_dir()  # os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'KANImageryCatalog_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&KAN Imagery Catalog')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar('KANImageryCatalog')
        self.toolbar.setObjectName('KANImageryCatalog')

        # print "** INITIALIZING KANImageryCatalog"

        self.pluginIsActive = False
        self.dockwidget = None

        ##########################
        # self.first_start = None
        self.frm_settings = None
        self.frm_collection_settings = None
        ##########################

        settings = PluginSettings()
        settings.clean_temporary_files_if_needed()

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """

        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('KANImageryCatalog', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # icon_path = ':/plugins/kan_imagery_catalog/icon.png'
        icon_path = ':/resources/brand/logo_mini.png'
        # self.add_action(icon_path, text=self.tr(''), callback=self.run, parent=self.iface.mainWindow())
        self.add_action(
            icon_path,
            text=self.tr('KAN Imagery Catalog'),
            callback=self.run,
            parent=self.iface.mainWindow(),
        )

        # self.first_start = True

        # icon_path = ':/resources/icon.png'
        # self.add_action(
        #     icon_path,
        #     text=self.tr(u'Catastro CDMX'),
        #     callback=self.run,
        #     parent=self.iface.mainWindow())

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # print "** CLOSING KANImageryCatalog"

        # disconnects
        self.dockwidget.closing_plugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        # print "** UNLOAD KANImageryCatalog"

        for action in self.actions:
            self.iface.removePluginMenu(self.tr('&KAN Imagery Catalog'), action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    # --------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # print "** STARTING KANImageryCatalog"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = KANImageryCatalogDock()

            # if self.frm_settings is None:
            #     self.frm_settings = FormSettings()

            # if self.frm_collection_settings is None:
            #     self.frm_collection_settings = FormDefaultCollections()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closing_plugin.connect(self.onClosePlugin)
            # self.dockwidget.open_settings_signal.connect(self.open_settings)
            # self.dockwidget.open_collection_settings_signal.connect(self.open_collection_settings)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)

            self.dockwidget.show()

    # def open_settings(self):
    #     """Open the settings dialog."""
    #     # frm = FormSettings(parent=, closing_plugin=None) #self.onClosePlugin)
    #     # frm = FormSettings()
    #     # self.frm_settings.show()
    #     # self.frm_settings.setWindowFlags(Qt.WindowStaysOnTopHint)
    #     result = self.frm_settings.exec_()
    #     if result:
    #         pass

    # def open_collection_settings(self):
    #     # frm = FormDefaultCollections()
    #     # # frm = FormDefaultCollections(parent=self, closing_plugin=None) #self.onClosePlugin)
    #     # if frm.exec() == QDialog.accepted:
    #     # self.frm_collection_settings.show()
    #     # self.frm_collection_settings.setWindowFlags(Qt.WindowStaysOnTopHint)
    #     result = self.frm_collection_settings.exec_()
    #     if result:
    #         pass
