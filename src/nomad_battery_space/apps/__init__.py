from nomad.config.models.plugins import AppEntryPoint

from nomad_battery_space.apps.hzb_bat_search_app import hzb_bat_search_app

hzb_bat_search_app_entry_point = AppEntryPoint(
    name='HZB batteries search app',
    description="""
    This app allows you to search HZB battery data within NOMAD.
    """,
    app=hzb_bat_search_app,
)
