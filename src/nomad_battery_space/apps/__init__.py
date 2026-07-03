from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import App, Column, Columns, FilterMenu, FilterMenus

from nomad_battery_space.apps.hzb_bat_search_app import hzb_bat_search_app
from nomad_battery_space.apps.hzb_coincell_search_app import hzb_coincell_search_app

app_entry_point = AppEntryPoint(
    name='NewApp',
    description='New app entry point configuration.',
    app=App(
        label='NewApp',
        path='app',
        category='battery space',
        columns=Columns(
            selected=['entry_id'],
            options={
                'entry_id': Column(),
            },
        ),
        filter_menus=FilterMenus(
            options={
                'material': FilterMenu(label='Material'),
            }
        ),
    ),
)

hzb_bat_search_app_entry_point = AppEntryPoint(
    name='HZB batteries search app',
    description="""
    This app allows you to search HZB battery data within NOMAD.
    """,
    app=hzb_bat_search_app,
)

hzb_coincell_search_app_entry_point = AppEntryPoint(
    name='HZB CoinCell search app',
    description="""
    This app allows you to search HZB CoinCell data within NOMAD.
    """,
    app=hzb_coincell_search_app,
)
