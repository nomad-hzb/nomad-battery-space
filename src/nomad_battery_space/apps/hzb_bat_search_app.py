from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

# i see a problem here, because it is only referencing one type of batteries. not used currently
schema = 'nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery'

hzb_bat_search_app = App(
    label='HZB Batteries Search App',
    path='search',
    category='battery space',
    search_quantities=SearchQuantities(
        include=[
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.CylindricalCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.PouchCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.Electrode',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            #'data.aggregated_elements#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BatterySample',
        ]
    ),
    # filters_locked={'section_defs.definition_qualified_name': [schema]},
    columns=[
        Column(quantity='entry_id', selected=True),
        Column(quantity='entry_name', selected=True),
        Column(quantity='entry_type', selected=True),
        # This is CoinCell specific
        # Column(quantity=f'data.pressure#{schema}', selected=True),
        # Column(
        #     quantity=f'data.case_crimp#{schema}',
        #     selected=True,
        # ),
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
            MenuItemTerms(
                search_quantity='entry_type',
                title='Entry Type',
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
    # BatterySample exclusive: move that into extra app
    # dashboard=Dashboard(
    #     widgets=[
    #         WidgetPeriodicTable(
    #             title='Aggregated elements',
    #             layout={
    #                 'sm': Layout(minH=3, minW=3, h=9, w=12, y=0, x=0),
    #                 'md': Layout(minH=3, minW=3, h=9, w=12, y=0, x=0),
    #                 'lg': Layout(minH=3, minW=3, h=9, w=12, y=0, x=0),
    #                 'xl': Layout(minH=3, minW=3, h=10, w=12, y=0, x=0),
    #                 'xxl': Layout(minH=3, minW=3, h=10, w=12, y=0, x=0),
    #             },
    #             search_quantity='data.aggregated_elements#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
    #             scale='linear',
    #         ),
    #     ]
    # ),
)
