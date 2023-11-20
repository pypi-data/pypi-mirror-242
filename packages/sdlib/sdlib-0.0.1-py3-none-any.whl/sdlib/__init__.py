from . import sd_webui, plugin_system
from .function_params import *


def register_plugin(name: str) -> plugin_system.Plugin:
    return sd_webui.api_impl.webui_api.register_plugin(name)
