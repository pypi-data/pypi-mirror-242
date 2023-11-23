# AUTO GENERATED FILE - DO NOT EDIT

export ''_sendresults

"""
    ''_sendresults(;kwargs...)

A SendResults component.
Send a visualization set to a CAD Platform
results must be a valid HBJSON model
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `defaultAction` (a value equal to: 'add', 'delete', 'preview', 'clear', 'subscribe-preview'; optional)
- `defaultKey` (String; optional)
- `delay` (Real; optional)
- `geometryOptions` (optional): . geometryOptions has the following type: lists containing elements 'units'.
Those elements have the following types:
  - `units` (a value equal to: 'Meters', 'Millimeters', 'Feet', 'Inches', 'Centimeters'; optional)
- `optionsConfig` (optional): . optionsConfig has the following type: lists containing elements 'add', 'delete', 'preview', 'clear', 'subscribe-preview'.
Those elements have the following types:
  - `add` (Bool; required)
  - `delete` (Bool; required)
  - `preview` (Bool; required)
  - `clear` (Bool; required)
  - `subscribe-preview` (Bool; required)
- `results` (Bool | Real | String | Dict | Array; optional)
"""
function ''_sendresults(; kwargs...)
        available_props = Symbol[:id, :defaultAction, :defaultKey, :delay, :geometryOptions, :optionsConfig, :results]
        wild_props = Symbol[]
        return Component("''_sendresults", "SendResults", "pollination_dash_io", available_props, wild_props; kwargs...)
end

