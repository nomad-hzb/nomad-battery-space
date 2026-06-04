from nomad.config.models.ui import App, Column, Columns, FilterMenu, FilterMenus

hzb_bat_search_app = App(
    label='HZB Batteries Search App',
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
)