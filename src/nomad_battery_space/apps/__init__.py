from nomad.config.models.plugins import AppEntryPoint

from nomad_battery_space.apps.hzb_bat_search_app import hzb_bat_search_app
from nomad_battery_space.apps.voila_finder_app import voila_finder_app

hzb_bat_search_app_entry_point = AppEntryPoint(
    name='HZB sample search app',
    description="""
    This app allows you to search HZB battery data within NOMAD.
    """,
    app=hzb_bat_search_app,
)

voila_finder_app_entry_point = AppEntryPoint(
    name='Voila',
    description="""
    This app allows you to find and launch Voila tools for battery space data.
    """,
    app=voila_finder_app,
)
