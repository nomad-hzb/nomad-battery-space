from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Menu,
    MenuItemCustomQuantities,
    MenuItemHistogram,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

# i see a problem here, because it is only referencing one type of batteries. not used currently
schema = 'nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery'
classes_with_similar_properties: list[str] = [
    'ElectrodeSheet',
    'ElectrodeSample',
    'SeparatorStock',
    'SeparatorSample',
]

# since inherited properties not yet supported (https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR/-/work_items/2163) to have one common filter we need extra ones for each class. we try it DRY:
subclass_filter_menus: dict[str, Menu] = {}
for class_name in classes_with_similar_properties:
    menu = Menu(
        title=f'{class_name} Properties',
        items=[
            MenuItemHistogram(
                title='Thickness',
                x=Axis(
                    search_quantity=f'data.dimensions_and_weights.thickness#nomad_battery_space.schema_packages.hzb_bs_package.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Mass',
                x=Axis(
                    search_quantity=f'data.dimensions_and_weights.mass#nomad_battery_space.schema_packages.hzb_bs_package.{class_name}'
                ),
            ),
        ],
    )

    subclass_filter_menus[class_name] = menu


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
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSample',
            # '*#nomad_battery_space.schema_packages.hzb_bs_package.DimensionsAndWeights',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorStock'
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorSample'
            #'data.aggregated_elements#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BatterySample',
        ]
    ),
    # filters_locked={'section_defs.definition_qualified_name': [schema]},
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
            MenuItemTerms(
                search_quantity='entry_type',
                title='Entry Type',
                show_input=False,
                options=0,
            ),
            subclass_filter_menus['ElectrodeSheet'],
            subclass_filter_menus['ElectrodeSample'],
            subclass_filter_menus['SeparatorStock'],
            subclass_filter_menus['SeparatorSample'],
            MenuItemVisibility(),
            MenuItemCustomQuantities(title='Custom Conditions'),
        ],
    ),
)
