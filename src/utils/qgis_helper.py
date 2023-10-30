""" QGIS helper functions module. """

import json

from PyQt5.QtCore import QVariant

from utils.exceptions import DataNotFoundError
from utils.general import PLUGIN_NAME

try:
    from qgis.core import (
        Qgis,
        QgsFeature,
        QgsField,
        QgsFields,
        QgsFillSymbol,
        QgsGeometry,
        QgsLayerTreeGroup,
        QgsPointXY,
        QgsProject,
        QgsRasterFillSymbolLayer,
        QgsSettings,
        QgsVectorLayer,
    )
    from qgis.utils import iface
except:  # noqa: E722    pylint: disable=bare-except
    print('No se pudieron importar las librerías de QGIS')


def get_bounding_box_canvas():
    """Get bounding box from canvas."""

    active_layer = iface.activeLayer()
    if not active_layer:
        raise DataNotFoundError('Debe tener al menos una capa activa')

    bbox = iface.mapCanvas().extent()
    xmin = bbox.xMinimum()
    ymin = bbox.yMinimum()
    xmax = bbox.xMaximum()
    ymax = bbox.yMaximum()

    return {'x_min': xmin, 'y_min': ymin, 'x_max': xmax, 'y_max': ymax}


def get_bounding_box_selected_feature(layer_name):
    """Get bounding box from selected feature."""

    layers = QgsProject.instance().mapLayersByName(layer_name)
    if not layers:
        raise DataNotFoundError('Error', 'No se encontró la capa especificada.')

    layer = layers[0]
    if layer.selectedFeatureCount() > 0:
        selected_feature = layer.selectedFeatures()[0]
        bbox = selected_feature.geometry().boundingBox()
        xmin = bbox.xMinimum()
        ymin = bbox.yMinimum()
        xmax = bbox.xMaximum()
        ymax = bbox.yMaximum()

        return {'x_min': xmin, 'y_min': ymin, 'x_max': xmax, 'y_max': ymax}

    raise DataNotFoundError('No hay objetos seleccionados en la capa especificada.')


def get_single_polygon_layers():
    """Get single polygon layers from current project."""

    layer_list = []
    for layer in QgsProject.instance().mapLayers().values():
        if isinstance(layer, QgsVectorLayer) and layer.wkbType() == 3:
            layer_list.append(layer.name())

    return layer_list


def save_setting(setting_name, value):
    """Save setting."""

    settings = QgsSettings()
    settings.setValue(f'{PLUGIN_NAME}/{setting_name}', value)


def read_setting(setting_name, default_value=None):
    """Read setting."""

    settings = QgsSettings()
    return settings.value(f'{PLUGIN_NAME}/{setting_name}', default_value)


def save_json_setting(setting_name, value):
    """Save json setting."""

    json_setting = json.dumps(value)
    settings = QgsSettings()
    settings.setValue(f'{PLUGIN_NAME}/{setting_name}', json_setting)


def read_json_setting(setting_name, default_value=None):
    """Read json setting."""
    settings = QgsSettings()
    json_setting = settings.value(f'{PLUGIN_NAME}/{setting_name}', default_value)

    if json_setting is not None:
        value = json.loads(json_setting)
        return value


# 0: Info
# 1: Warning
# 2: Critical
# 3: Success


def error_message(title, text):
    """Show error message."""

    iface.messageBar().pushMessage(title, text, level=Qgis.Critical)


def warning_message(title, text):
    """Show warning message."""

    iface.messageBar().pushMessage(title, text, level=Qgis.Warning)


def info_message(title, text):
    """Show info message."""

    iface.messageBar().pushMessage(title, text, level=Qgis.Info)


def success_message(title, text):
    """Show success message."""

    iface.messageBar().pushMessage(title, text, level=Qgis.Success)


def get_or_create_group(group_name):
    """Get or create group."""

    root = QgsProject.instance().layerTreeRoot()
    results_group = None
    for child in root.children():
        # Use of casefold is to avoid problems with special characters specially on windows
        if child.name().casefold() == group_name.casefold():
            print(f'{child.name()} {type(child)}')

        if isinstance(child, QgsLayerTreeGroup) and child.name().casefold() == group_name.casefold():
            print('es QgsLayerTreeGroup')
            results_group = child
            break

    if results_group is None:
        results_group = root.insertGroup(0, group_name)

    return results_group


def get_layer_by_name(layer_name):
    """Get layer by name."""

    layers = QgsProject.instance().mapLayersByName(layer_name)
    if layers:
        return layers[0]

    return None


def get_or_create_footprints_layer(layer_name, group_name):
    """Get or create footprints layer."""

    layers = QgsProject.instance().mapLayersByName(layer_name)
    if layers:
        footprints_layer = layers[0]
    else:
        results_group = get_or_create_group(group_name)
        footprints_layer = QgsVectorLayer('Polygon', layer_name, 'memory')

        symbol = QgsFillSymbol.createSimple(
            {
                'color': '155,55,55,15',
                'outline_color': 'dark_gray',
                'outline_width': '0.1',
            }
        )
        footprints_layer.renderer().setSymbol(symbol)

        pr = footprints_layer.dataProvider()
        # Add layer fields
        fields = QgsFields()
        fields.append(QgsField('ID', QVariant.String))
        pr.addAttributes(fields)
        footprints_layer.updateFields()
        footprints_layer.triggerRepaint()

        QgsProject.instance().addMapLayer(footprints_layer, False)
        results_group.addLayer(footprints_layer)

    return footprints_layer


def get_current_crs():
    """Get crs from active layer."""

    return iface.activeLayer().crs().authid()


def create_layer(layer_name, group_name):
    """Create a layer."""

    results_group = get_or_create_group(group_name)
    results_layer = QgsVectorLayer('Polygon', layer_name, 'memory')

    symbol = QgsFillSymbol.createSimple(
        {
            'color': '155,55,55,15',
            'outline_color': 'dark_gray',
            'outline_width': '0.1',
        }
    )
    results_layer.renderer().setSymbol(symbol)
    results_layer.triggerRepaint()

    QgsProject.instance().addMapLayer(results_layer, False)
    results_group.addLayer(results_layer)

    return results_layer


def add_feature_to_layer(coordinates, feature_id, layer):
    """Add feature to layer."""

    pr = layer.dataProvider()
    points = [QgsPointXY(point[0], point[1]) for point in coordinates]
    polygon = QgsGeometry.fromPolygonXY([points])

    feature = QgsFeature()
    feature.setGeometry(polygon)
    feature.setAttributes([feature_id])

    pr.addFeature(feature)
    layer.updateExtents()
    return layer


def create_quicklook_layer(
    layer_name,
    group_name,
    feature,
    crs,
    layer_type='Polygon',
    image_path=None,
):
    """Create a layer with a quicklook image."""

    results_group = get_or_create_group(group_name)

    new_layer = QgsVectorLayer(f'{layer_type}?crs={crs}', layer_name, 'memory')
    new_layer_data_provider = new_layer.dataProvider()
    new_layer_data_provider.addFeatures([feature])

    symbol = QgsFillSymbol.createSimple(
        {
            'color': '255,0,0,0',
            'outline_color': 'transparent',
            'outline_width': '0',
        }
    )

    symbol_layer = QgsRasterFillSymbolLayer(image_path)
    symbol.appendSymbolLayer(symbol_layer)
    new_layer.renderer().setSymbol(symbol)
    new_layer.triggerRepaint()

    QgsProject.instance().addMapLayer(new_layer, False)
    results_group.addLayer(new_layer)
