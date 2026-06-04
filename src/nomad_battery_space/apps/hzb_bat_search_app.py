from nomad.config.models.ui import (
    App,
    Column,
    Columns,
    Menu,
    MenuItemTerms,
)

hzb_bat_search_app = App(
    label='HZB Batteries Search App',
    path='search',
    category='battery space',
    menu=Menu(
        items=[
            MenuItemTerms(
                search_quantity='authors.name',
                options=5,
                show_input=True,
            ),
        ]
    ),
    columns=Columns(
        selected=['entry_id'],
        options={
            'entry_id': Column(),
        },
    ),
)
