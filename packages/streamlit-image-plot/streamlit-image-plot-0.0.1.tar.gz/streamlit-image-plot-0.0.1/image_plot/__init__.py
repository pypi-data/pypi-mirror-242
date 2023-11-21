import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _image_plot = components.declare_component(
        "image_plot",
        url="http://localhost:3001",
    )
else:
   
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _image_plot = components.declare_component("image_plot", path=build_dir)

def image_plot(data=None, styles=None, key=None):
   
    component_value = _image_plot(data=data, styles=styles, key=key, default=0)

    return component_value
