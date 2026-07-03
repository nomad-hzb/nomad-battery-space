from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemCustomQuantities,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

# i see a problem here, because it is only referencing one type of batteries. not used currently
schema = 'nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery'


hzb_coincell_search_app = App(
    label='HZB CoinCell Search App',
    path='search_coincell',
    category='battery space',
    search_quantities=SearchQuantities(
        include=[
            f'*#{schema}',
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.CylindricalCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.PouchCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.Electrode',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSample',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.DimensionsAndWeights',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorStock'
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorSample'
            #'data.aggregated_elements#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BatterySample',
        ]
    ),
    filters_locked={'section_defs.definition_qualified_name': [schema]},
    columns=[
        Column(quantity='entry_id', selected=True),
        Column(quantity='entry_name', selected=True),
        Column(quantity='entry_type', selected=True),
    ],
    menu=Menu(
        title='Filter',
        size='sm',
        items=[
            # Nach Autor filtern – authors.name ist ein Built-in-Feld
            MenuItemTerms(
                search_quantity='authors.name',
                title='Author',
                options=0,
                show_input=False,
            ),
            # MenuItemHistogram(
            #     title='WorkerElectrode Thickness',
            #     x=Axis(
            #         search_quantity=f'data.working_electrode.dimensions_and_weights.thickness#{schema}'
            #     ),
            # ),
            MenuItemVisibility(),
            MenuItemCustomQuantities(title='Custom Conditions'),
        ],
    ),
)
