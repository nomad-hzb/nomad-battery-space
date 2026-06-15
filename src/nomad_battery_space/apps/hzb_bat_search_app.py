from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

schema = (
    'nomad_battery_space.schema_packages.battery_cell_assembly_package.CoinCellBattery'
)

hzb_bat_search_app = App(
    label='HZB Batteries Search App',
    path='search',
    category='battery space',
    search_quantities=SearchQuantities(
        include=[
            '*#nomad_battery_space.schema_packages.battery_cell_assembly_package.CoinCellBattery'
        ]
    ),
    filters_locked={'section_defs.definition_qualified_name': [schema]},
    columns=[
        Column(quantity='entry_id', selected=True),
        Column(quantity='entry_name', selected=True),
        Column(quantity=f'data.pressure#{schema}', selected=True),
        Column(
            quantity=f'data.case_crimp#{schema}',
            selected=True,
        ),
    ],
    menu=Menu(
        title='Filter',
        items=[
            # Nach Autor filtern – authors.name ist ein Built-in-Feld
            MenuItemTerms(
                search_quantity='authors.name',
                title='Author',
                options=10,
            ),
            MenuItemVisibility(),
            # Beispiel: nach einem eigenen String-Feld filtern
            # MenuItemTerms(
            #     search_quantity=f'data.anode_material#{schema}',
            #     title='Anode Material',
            # ),
        ],
    ),
)
