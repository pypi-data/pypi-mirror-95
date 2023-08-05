# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FreeDraw(Component):
    """A FreeDraw component.
LayerGroup is a wrapper of LayerGroup in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Attribution
- modes (list of a value equal to: "CREATE", "EDIT", "DELETE", "APPEND", "ALL"s; default ["ALL"]): Attribution
- options (dict; optional): Options to https://github.com/Wildhoney/Leaflet.FreeDraw
- className (string; optional): A custom class name to assign to the image. Empty by default.
- id (string; optional): The ID used to identify this component in Dash callbacks"""
    @_explicitize_args
    def __init__(self, children=None, modes=Component.UNDEFINED, options=Component.UNDEFINED, className=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'modes', 'options', 'className', 'id']
        self._type = 'FreeDraw'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'modes', 'options', 'className', 'id']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FreeDraw, self).__init__(children=children, **args)
