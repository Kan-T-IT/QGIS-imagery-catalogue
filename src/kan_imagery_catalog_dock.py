# -*- coding: utf-8 -*-

# KAN Imagery Catalog QGIS plugin
# Satellite image catalog manager

# * Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
# * begin      : 2023-07-14
# * copyright  : (C) 2023 by KAN Territory & IT


# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.


"""KAN Imagery Catalog QGIS plugin dock widget module."""

import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QDate, QSize, Qt, QVariant, pyqtSignal
from PyQt5.QtGui import QIcon, QIntValidator, QMovie
from PyQt5.QtWidgets import QListWidgetItem

from core.catalogs import get_catalog, get_thumbnail
from core.collections import get_collections
from core.settings import PluginSettings
from gui.custom_widgets import CustomWidgetListItem
from gui.form_default_collections import FormDefaultCollections
from gui.form_settings import FormSettings
from gui.helpers import forms
from gui.helpers.worker import WorkerThread
from utils import qgis_helper
from utils.constants import RESULTS_GROUP_NAME, RESULTS_LAYER_NAME
from utils.exceptions import AuthorizationError, DataNotFoundError, HostError, ProviderError, SettingsError
from utils.helpers import tr

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'kan_imagery_catalog_dock.ui'))


class KANImageryCatalogDock(QtWidgets.QDockWidget, FORM_CLASS):
    """KANImageryCatalogDock Dockwidget class."""

    closing_plugin = pyqtSignal()
    error_signal = pyqtSignal(str, str)
    warning_signal = pyqtSignal(str, str)
    info_signal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        """Constructor."""

        super(KANImageryCatalogDock, self).__init__(parent)

        self.parent = parent

        self.setupUi(self)
        forms.set_form_stylesheet(self)

        self.btn_settings.clicked.connect(self.btn_settings_clicked)
        self.btn_get_data.clicked.connect(self.btn_get_data_clicked)
        self.btn_select_catalogs.clicked.connect(self.btn_select_catalogs_clicked)

        self.btn_show_hide_search_area.clicked.connect(self.btn_show_hide_search_area_clicked)
        self.btn_show_hide_catalogs.clicked.connect(self.btn_show_hide_catalogs_clicked)
        self.btn_show_hide_filters.clicked.connect(self.btn_show_hide_filters_clicked)
        self.btn_sort_results.clicked.connect(self.btn_sort_results_clicked)
        # self.btn_sort_results.clicked.connect(lambda: self.sort_list_widget_1(True))

        self.btn_update_layers_list.clicked.connect(self.btn_update_layers_list_clicked)
        self.chk_search_by_dataframe.stateChanged.connect(self.chk_search_by_dataframe_update)
        self.slider_cloud_coverage.valueChanged.connect(self.update_cloud_coverage_label)

        self.btn_select_catalogs.setGraphicsEffect(forms.get_shadow_effect())
        self.btn_get_data.setGraphicsEffect(forms.get_shadow_effect())
        self.btn_get_data.setText(tr('Search'))

        int_validator = QIntValidator()
        self.txt_max_catalog_results.setValidator(int_validator)
        self.txt_max_catalog_results.textChanged.connect(self.txt_max_catalog_results_text_changed)

        self.chk_search_by_dataframe.setChecked(True)
        self.chk_search_by_dataframe_update()

        self.lbl_search_area_tooltip.setToolTip(tr("Dataframe or project layers (only 'single polygon' type layers)."))
        self.lbl_catalogs_tooltip.setToolTip(
            tr('Defines the catalogs of each supplier that will be used for searches.')
        )
        self.lbl_filters_tooltip.setToolTip(tr('Perform the search according to the indicated filters.'))
        # self.cbo_sort_by.setStyleSheet("QComboBox{border : 0px;}")

        sort_by = [
            {'key': 'angle', 'value': 'Angle'},
            {'key': 'date', 'value': 'Date'},
            {'key': 'cloud_coverage', 'value': 'Cloud coverage'},
            {'key': 'name', 'value': 'Name'},
        ]

        forms.load_combobox(self.cbo_sort_by, 'key', 'value', sort_by)
        self.cbo_sort_by.setHidden(True)
        self.lst_data.setSortingEnabled(True)

        self.settings = PluginSettings()

        default_date_to = QDate.currentDate()
        self.dt_date_to.setDate(default_date_to)

        default_date_from = default_date_to.addDays(int(self.settings.back_days) * -1)
        self.dt_date_from.setDate(default_date_from)
        self.slider_cloud_coverage.setValue(int(self.settings.cloud_coverage or 0))
        self.txt_max_catalog_results.setText(str(self.settings.max_catalog_results or 0))
        self.collections = []
        self.sort_ascending = True

        # SPINNER
        self.loading_spinner = QMovie(':/resources/spinner.gif')
        self.lbl_spinner.setMovie(self.loading_spinner)
        self.lbl_spinner.setFixedSize(QSize(25, 25))

        self.thread_get_catalogs = WorkerThread()
        self.thread_get_catalogs.started.connect(lambda: self.set_form_state(is_busy=True, show_spinner=True))
        self.thread_get_catalogs.finished.connect(lambda: self.set_form_state(is_busy=False, show_spinner=False))
        self.thread_get_catalogs.finished.connect(self.get_data_finished)
        self.thread_get_catalogs.progress_updated.connect(self.update_progress)
        self.thread_get_catalogs.error_signal.connect(self.show_error)
        self.thread_get_catalogs.warning_signal.connect(self.show_warning)

        self.thread_get_thumbnails = WorkerThread()
        self.thread_get_thumbnails.progress_updated.connect(self.update_progress)
        self.thread_get_thumbnails.error_signal.connect(self.show_error)
        self.thread_get_thumbnails.warning_signal.connect(self.show_warning)

        self.thread_load_collections_cache = WorkerThread()
        self.thread_load_collections_cache.started.connect(lambda: self.set_form_state(is_busy=True, show_spinner=True))
        self.thread_load_collections_cache.finished.connect(
            lambda: self.set_form_state(is_busy=False, show_spinner=True)
        )
        self.thread_load_collections_cache.finished.connect(self.show_collections_form)
        self.thread_load_collections_cache.error_signal.connect(self.show_error)
        self.thread_load_collections_cache.warning_signal.connect(self.show_warning)

        self.error_signal.connect(self.show_error)
        self.warning_signal.connect(self.show_warning)
        self.info_signal.connect(self.show_info)

        self.show_ended_search_message = True

    def show_info(self, title, message):
        """Show info message."""

        qgis_helper.info_message(title, message)

    def show_warning(self, title, message):
        """Show warning message."""

        qgis_helper.warning_message(title, message)

    def show_error(self, title, message):
        """Show error message."""

        qgis_helper.error_message(title, message)

    def set_form_state(self, is_busy, show_spinner=False):
        """Sets the form state (enabled/disabled) when the process is runnning in a separate thread."""

        self.lbl_logo.setVisible(not show_spinner or (show_spinner and not is_busy))
        self.lbl_spinner.setVisible(show_spinner and is_busy)

        if is_busy:
            if show_spinner:
                self.loading_spinner.start()

            # Disable form controls
            self.frame_catalog.setDisabled(True)
            self.btn_settings.setDisabled(True)
        else:
            if show_spinner:
                self.loading_spinner.stop()

            # Enable form controls
            self.frame_catalog.setDisabled(False)
            self.btn_settings.setDisabled(False)

    def closeEvent(self, event):
        """Run close plugin event."""

        self.closing_plugin.emit()
        event.accept()

    def txt_max_catalog_results_text_changed(self):
        """Event handler for textbox 'txt_max_catalog_results'."""

        forms.check_int_not_empty(self.txt_max_catalog_results)

    def update_cloud_coverage_label(self):
        """Event handler for slider 'slider_cloud_coverage'."""

        max_cloud_coverage_text = tr('Max cloud coverage')
        self.lbl_cloud_coverage.setText(f'{max_cloud_coverage_text} ({self.slider_cloud_coverage.value()} %)')

    def chk_search_by_dataframe_update(self):
        """Event handler for checkbox 'chk_search_by_dataframe'."""

        self.cbo_layer.setHidden(self.chk_search_by_dataframe.isChecked())
        self.btn_update_layers_list.setHidden(self.chk_search_by_dataframe.isChecked())

        if not self.chk_search_by_dataframe.isChecked():
            self.btn_update_layers_list_clicked()

    def btn_update_layers_list_clicked(self):
        """Event handler for button 'btn_update_layers_list'."""

        self.cbo_layer.clear()

        layer_list = ['  -----  ']
        if not self.chk_search_by_dataframe.isChecked():
            layer_list = qgis_helper.get_valid_project_layers_to_search()

        model = QtGui.QStandardItemModel(0, 1)
        for key, value in layer_list:
            item = QtGui.QStandardItem(value)
            item.setData(key, Qt.UserRole)
            model.appendRow(item)

        self.cbo_layer.setModel(model)

    def btn_settings_clicked(self):
        """Event handler for button 'btn_settings'."""

        self.set_form_state(is_busy=True)
        frm = FormSettings(parent=self, closing_plugin=self.closing_plugin)
        frm.exec()
        self.settings = PluginSettings()
        self.set_form_state(is_busy=False)

    def btn_select_catalogs_clicked(self):
        """Event handler for button 'btn_select_catalogs'."""

        self.thread_load_collections_cache.start(self.load_collections_cache, {})

    def load_collections_cache(self):
        """Load collections in caché"""

        for provider in self.settings.get_active_providers():
            try:
                self.collections = get_collections(provider, {})
            except ProviderError as ex:
                self.warning_signal.emit(tr('Warning'), f'{provider}: {ex.message}')
            except (AuthorizationError, HostError) as ex:
                self.warning_signal.emit(tr('Warning'), ex.message)
            except Exception as ex:
                self.warning_signal.emit(tr('Error'), f'{provider}: {ex}')

    def show_collections_form(self):
        """Show form to select collections."""

        if not self.collections:
            return

        self.set_form_state(is_busy=True)
        frm = FormDefaultCollections(parent=self, closing_plugin=self.closing_plugin)
        frm.exec()
        self.set_form_state(is_busy=False)

    def btn_sort_results_clicked(self):
        """Event handler for button 'btn_sort_results'."""

        icon_path = ':/resources/icons/sort-ascending.svg'
        if not self.sort_ascending:
            icon_path = ':/resources/icons/sort-descending.svg'

        self.btn_sort_results.setIcon(QIcon(icon_path))
        self.lst_data.sortItems(Qt.AscendingOrder if self.sort_ascending else Qt.DescendingOrder)
        self.sort_ascending = not self.sort_ascending

    def btn_show_hide_search_area_clicked(self):
        """Event handler for button 'btn_show_hide_search_area'."""

        icon_path = ':/resources/icons/down.svg'
        if not self.frame_search_area.isVisible():
            icon_path = ':/resources/icons/up.svg'

        self.btn_show_hide_search_area.setIcon(QIcon(icon_path))
        self.frame_search_area.setVisible(not self.frame_search_area.isVisible())

    def btn_show_hide_catalogs_clicked(self):
        """Event handler for button 'btn_show_hide_catalogs'."""

        icon_path = ':/resources/icons/down.svg'
        if not self.frame_catalogs.isVisible():
            icon_path = ':/resources/icons/up.svg'

        self.btn_show_hide_catalogs.setIcon(QIcon(icon_path))
        self.frame_catalogs.setVisible(not self.frame_catalogs.isVisible())

    def btn_show_hide_filters_clicked(self):
        """Event handler for button 'btn_show_hide_filters'."""

        icon_path = ':/resources/icons/down.svg'
        if not self.frame_filters.isVisible():
            icon_path = ':/resources/icons/up.svg'

        self.btn_show_hide_filters.setIcon(QIcon(icon_path))
        self.frame_filters.setVisible(not self.frame_filters.isVisible())

    def btn_get_data_clicked(self):
        """Event handler for button 'btn_get_data'."""

        if not self.chk_search_by_dataframe.isChecked() and not self.cbo_layer.currentText():
            raise DataNotFoundError(tr('The project has no layers available to use as a reference for searching.'))

        # Check if there are providers configured...
        if not self.settings.get_active_providers():
            qgis_helper.warning_message(
                tr('Warning'),
                tr('There are no providers defined in the plugin settings.'),
            )
            return

        self.btn_get_data.setText(tr('Getting results...'))
        self.lst_data.clear()

        cloud_coverage = self.slider_cloud_coverage.value()
        date_from = self.dt_date_from.date()
        date_to = self.dt_date_to.date()
        layer_id = None if self.chk_search_by_dataframe.isChecked() else self.cbo_layer.currentData()

        try:
            max_catalog_results = int(self.txt_max_catalog_results.text().strip())
        except Exception:
            max_catalog_results = self.settings.max_catalog_results
            self.txt_max_catalog_results.setText(str(max_catalog_results))

        self.show_ended_search_message = True
        dict_bbox = {}
        try:
            if layer_id:
                dict_bbox = qgis_helper.get_selected_feature_bounding_box(layer_id)
            else:
                dict_bbox = qgis_helper.get_bounding_box_canvas()
        except DataNotFoundError as ex:
            self.show_ended_search_message = False
            qgis_helper.warning_message(
                tr('Information'),
                tr(str(ex)),
            )
            return

        params = {
            'bounding_box': dict_bbox,
            'cloud_coverage': cloud_coverage,
            'date_from': date_from,
            'date_to': date_to,
            'max_catalog_results': max_catalog_results,
        }

        self.thread_get_thumbnails.requestInterruption()
        self.thread_get_catalogs.start(self.get_results, params)

    def get_data_finished(self):
        """Event handler for thread 'thread_get_catalogs' finished."""

        self.btn_get_data.setText(tr('Search'))

        if self.show_ended_search_message:
            qgis_helper.success_message('', tr('The catalog search has ended.'))

    def get_results(self, bounding_box, cloud_coverage, date_from, date_to, max_catalog_results):
        """Get results from selected catalogs with selected filters."""

        limit_features = self.settings.max_features_results

        if not (isinstance(self.settings.selected_collections, list)) or len(self.settings.selected_collections) == 0:
            raise SettingsError(tr('There are no catalogs selected.'))

        catalog_counter = 0

        # Group collections by host
        dict_collections = {}
        collection_aux = {}

        active_providers = self.settings.get_active_providers()

        catalogs_data_result = []

        for collection in self.settings.selected_collections:
            col_provider = collection['provider']

            if col_provider not in active_providers:
                continue

            # Save collection name and title to use in results list
            if col_provider not in collection_aux:
                collection_aux[col_provider] = {}

            if collection['name'] not in collection_aux[col_provider]:
                collection_aux[col_provider][collection['name']] = collection['title']

            host_name = collection['hostName']
            if host_name not in dict_collections:
                dict_collections[host_name] = {'provider': col_provider, 'collections': []}

            dict_collections[host_name]['collections'].append(collection['name'])

        for _host_name, values in dict_collections.items():
            catalogs = []
            provider = values['provider']
            collections = values['collections']

            if catalog_counter >= max_catalog_results:
                break

            datetime_params = f"{date_from.toString('yyyy-MM-ddT00:00:00Z')}/{date_to.toString('yyyy-MM-ddT23:59:59Z')}"
            for collection_name in collections:
                # FIXME: Search collection one by one to avoid errors in Up42 provider
                search_params = {
                    'collections': [collection_name],
                    'bbox': [
                        bounding_box.get('x_min'),
                        bounding_box.get('y_min'),
                        bounding_box.get('x_max'),
                        bounding_box.get('y_max'),
                    ],
                    'datetime': datetime_params,
                    'limit': limit_features,
                }

                try:
                    _catalogs = get_catalog(
                        provider=provider,
                        host_name=_host_name,
                        search_params=search_params,
                        max_cloud_coverage=cloud_coverage,
                        collection_names=collection_aux.get(provider, []),
                    )
                    catalogs += _catalogs
                except AuthorizationError as ex:
                    self.warning_signal.emit(tr('Warning'), str(ex))
                    continue

                except (ProviderError, HostError) as ex:
                    self.error_signal.emit(tr('Error'), str(ex))
                    continue

            features_counter = 0
            for catalog in catalogs:
                if features_counter >= limit_features:
                    break

                thumbnail = None

                dic_result = {
                    'coordinates': catalog['aux_coordinates'],
                    'provider_name': provider,
                    'host_name': _host_name,
                    'collection_name': catalog['aux_collection_name'],
                    'feature_data': catalog,
                    'acquisition_date': catalog['aux_date'],
                    'incidence_angle': catalog['aux_angle'],
                    'cloud_coverage': catalog['aux_cloud_coverage'],
                    'image_id': catalog['aux_image_id'],
                    'feature_index': features_counter,
                    'thumbnail': thumbnail,
                }

                catalogs_data_result.append(
                    {
                        'provider': provider,
                        'host_name': _host_name,
                        'collection_name': catalog['aux_collection_name'],
                        'image_id': catalog['aux_image_id'],
                        'feature_data': catalog,
                        'catalog_result': dic_result,
                    }
                )

                self.thread_get_catalogs.progress_updated.emit(dic_result)
                features_counter += 1

            catalog_counter += 1

        self.thread_get_thumbnails.start(
            self.get_thumbnails_in_background,
            {'catalogs_data': catalogs_data_result},
        )

    def get_thumbnails_in_background(
        self,
        catalogs_data: list,
    ):
        for data in catalogs_data:
            if self.thread_get_thumbnails.isInterruptionRequested():
                break

            thumbnail = get_thumbnail(
                provider=data['provider'],
                host_name=data['host_name'],
                collection_name=data['collection_name'],
                image_id=data['image_id'],
                feature_data=data['feature_data'],
            )
            catalog_result = data['catalog_result']
            catalog_result['thumbnail'] = thumbnail
            self.thread_get_catalogs.progress_updated.emit(catalog_result)

    def update_progress(self, progress_data):
        """Update thread results in Toc and DockWidget."""

        if 'thumbnail' in progress_data and progress_data['thumbnail'] is not None:
            feature_index = progress_data['feature_index']
            for i in range(self.lst_data.count()):
                item = self.lst_data.item(i)
                custom_item = item.data(Qt.UserRole)
                if custom_item.feature_index == feature_index:
                    custom_item.set_thumbnail(progress_data['thumbnail'])
                    break
        else:
            self.add_feature_to_footprints_layer(
                coordinates=progress_data['coordinates'],
                footprint_id=progress_data['image_id'],
            )

            self.add_item_to_results(
                provider_name=progress_data['provider_name'],
                host_name=progress_data['host_name'],
                collection_name=progress_data['collection_name'],
                feature_data=progress_data['feature_data'],
                acquisition_date=progress_data['acquisition_date'],
                incidence_angle=progress_data['incidence_angle'],
                cloud_coverage=progress_data['cloud_coverage'],
                image_id=progress_data['image_id'],
                feature_index=progress_data['feature_index'],
                thumbnail=progress_data['thumbnail'],
            )

    def add_item_to_results(
        self,
        provider_name,
        host_name,
        collection_name,
        feature_data,
        acquisition_date,
        incidence_angle,
        cloud_coverage,
        image_id,
        feature_index,
        thumbnail,
    ):
        """Add item to results list."""

        custom_item = CustomWidgetListItem(
            parent=self.lst_data,
            provider_name=provider_name,
            host_name=host_name,
            collection_name=collection_name,
            feature_data=feature_data,
            thumbnail=thumbnail,
            acquisition_date=acquisition_date,
            incidence_angle=incidence_angle,
            cloud_coverage=cloud_coverage,
            image_id=image_id,
            feature_index=feature_index,
            closing_plugin=self.closing_plugin,
        )

        custom_item.thread_quicklooks.started.connect(lambda: self.set_form_state(is_busy=True, show_spinner=True))
        custom_item.thread_quicklooks.finished.connect(lambda: self.set_form_state(is_busy=False, show_spinner=True))
        custom_item.thread_quicklooks.error_signal.connect(self.show_error)
        custom_item.thread_quicklooks.warning_signal.connect(self.show_warning)

        item = QListWidgetItem(self.lst_data)
        item.setSizeHint(custom_item.sizeHint())
        item.setData(Qt.UserRole, QVariant(custom_item))
        item.setText(acquisition_date or '')
        self.lst_data.addItem(item)
        self.lst_data.setItemWidget(item, custom_item)

    def add_feature_to_footprints_layer(self, coordinates, footprint_id):
        """Add feature to footprints layer."""

        footprints_layer = qgis_helper.get_or_create_footprints_layer(RESULTS_LAYER_NAME, RESULTS_GROUP_NAME)
        qgis_helper.add_feature_to_layer(coordinates, footprint_id, footprints_layer)
