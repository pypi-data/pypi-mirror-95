# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LeafletMap(Component):
    """A LeafletMap component.


Keyword arguments:
- id (string; required): The ID of this component, used to identify dash components
in callbacks. The ID needs to be unique across all of the
components in an app.
- layers (list; optional): The layers
- mouseCoords (dict; optional): Mouse properties configuration. mouseCoords has the following type: dict containing keys 'position'.
Those keys have the following types:
  - position (string; optional)
- scaleY (dict; optional): ScaleY is a configuration for creating a slider for scaling the Y-axis. scaleY has the following type: dict containing keys 'scaleY', 'maxScaleY', 'minScaleY', 'position'.
Those keys have the following types:
  - scaleY (number; optional)
  - maxScaleY (number; optional)
  - minScaleY (number; optional)
  - position (string; optional)
- switch (dict; optional): Switch is a configuration for creating a switch-toggle. switch has the following type: dict containing keys 'value', 'disabled', 'position', 'label'.
Those keys have the following types:
  - value (boolean; optional)
  - disabled (boolean; optional)
  - position (string; optional)
  - label (string; optional)
- drawTools (dict; optional): DrawTools is a configuration for enabling drawing of polylines and areas. drawTools has the following type: dict containing keys 'drawMarker', 'drawPolygon', 'drawPolyline', 'position'.
Those keys have the following types:
  - drawMarker (boolean; optional)
  - drawPolygon (boolean; optional)
  - drawPolyline (boolean; optional)
  - position (string; optional)
- colorBar (dict; optional): ColorBar is a box that displays the colorScale. colorBar has the following type: dict containing keys 'position'.
Those keys have the following types:
  - position (string; optional)
- unitScale (dict; optional): UnitScale is a box that displays the the current unit scale on the map. unitScale has the following type: dict containing keys 'position'.
Those keys have the following types:
  - position (string; optional)
- center (list; optional)
- defaultBounds (list; optional)
- zoom (number; optional)
- minZoom (number; optional)
- maxZoom (number; optional)
- crs (string; optional)
- syncedMaps (list; optional): Ids of other LayeredMap instances that should be synced with this instance
- syncDrawings (boolean; optional): Boolean deciding whether or not to sync drawings between maps
- updateMode (string; optional): Allows to choose between replacing the layers or updating them
- autoScaleMap (boolean; optional): autoScaleMap makes the map listen for changes in width and height and automatically recalculates
the map dimensions when changes occur.
- polyline_points (list; optional): Dash provided prop that returns the coordinates of the edited or clicked polyline
- polygon_points (list; optional): Dash provided prop that returns the coordinates of the edited or clicked polygon
- marker_point (list; optional): Dash provided prop that returns the coordinates of the edited or clicked marker
- click_position (list; optional): Map coordinates of a mouse click
- clicked_shape (dict; optional): Shape clicked on JSON format"""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, layers=Component.UNDEFINED, mouseCoords=Component.UNDEFINED, scaleY=Component.UNDEFINED, switch=Component.UNDEFINED, drawTools=Component.UNDEFINED, colorBar=Component.UNDEFINED, unitScale=Component.UNDEFINED, center=Component.UNDEFINED, defaultBounds=Component.UNDEFINED, zoom=Component.UNDEFINED, minZoom=Component.UNDEFINED, maxZoom=Component.UNDEFINED, crs=Component.UNDEFINED, syncedMaps=Component.UNDEFINED, syncDrawings=Component.UNDEFINED, updateMode=Component.UNDEFINED, autoScaleMap=Component.UNDEFINED, polyline_points=Component.UNDEFINED, polygon_points=Component.UNDEFINED, marker_point=Component.UNDEFINED, click_position=Component.UNDEFINED, clicked_shape=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'layers', 'mouseCoords', 'scaleY', 'switch', 'drawTools', 'colorBar', 'unitScale', 'center', 'defaultBounds', 'zoom', 'minZoom', 'maxZoom', 'crs', 'syncedMaps', 'syncDrawings', 'updateMode', 'autoScaleMap', 'polyline_points', 'polygon_points', 'marker_point', 'click_position', 'clicked_shape']
        self._type = 'LeafletMap'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'layers', 'mouseCoords', 'scaleY', 'switch', 'drawTools', 'colorBar', 'unitScale', 'center', 'defaultBounds', 'zoom', 'minZoom', 'maxZoom', 'crs', 'syncedMaps', 'syncDrawings', 'updateMode', 'autoScaleMap', 'polyline_points', 'polygon_points', 'marker_point', 'click_position', 'clicked_shape']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(LeafletMap, self).__init__(**args)
