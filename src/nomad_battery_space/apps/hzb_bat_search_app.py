from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Menu,
    MenuItemCustomQuantities,
    MenuItemHistogram,
    MenuItemOptimade,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

from .hzb_bat_search_helper import (
    create_class_filter_menus,
)

# i see a problem here, because it is only referencing one type of batteries. not used currently
schema = 'nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery'


# IDEA: SearchApp Menu's are built directly in schema class by implementing an inherited method. In that method same method of parent class creates parent search menu, and concrete class adds own entries.
# Advantage: smaller search app

# since inherited properties not yet supported (https://gitlab.mpcdf.mpg.de/nomad-lab/nomad-FAIR/-/work_items/2163) to have one common filter we need extra ones for each class. we try it DRY:
class_filter_menus: dict[str, Menu] = create_class_filter_menus()


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
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BS_Chemical'
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
            Menu(
                title='Author',
                items=[
                    MenuItemTerms(
                        search_quantity='authors.name',
                        title='Author',
                        options=10,
                    ),
                ],
            ),
            Menu(
                title='Entry Properties',
                items=[
                    MenuItemTerms(
                        search_quantity='entry_type',
                        title='Entry Type',
                        options=10,
                    ),
                    MenuItemTerms(
                        search_quantity='entry_name',
                        title='Entry Name',
                        options=5,
                    ),
                    MenuItemHistogram(
                        title='Create Time',
                        x=Axis(search_quantity='entry_create_time'),
                    ),
                    MenuItemTerms(
                        search_quantity='results.eln.lab_ids',
                        title='Lab ID',
                        options=5,
                    ),
                ],
            ),
            Menu(
                title='Elements',
                width='36',
                items=[
                    MenuItemPeriodicTable(
                        search_quantity='results.material.elements',
                        title='Elements',
                        width='36',
                    ),
                ],
            ),
            class_filter_menus['ElectrodeSheet'],
            class_filter_menus['ElectrodeSample'],
            class_filter_menus['SeparatorStock'],
            class_filter_menus['SeparatorSample'],
            class_filter_menus['ElectrolyteStock'],
            class_filter_menus['ElectrolyteSample'],
            Menu(
                title='Chemical Properties',
                items=[
                    MenuItemTerms(
                        search_quantity='data.product_info.supplier#nomad_battery_space.schema_packages.hzb_bs_package.BS_Chemical',
                        title='Supplier',
                        options=10,
                    ),
                ],
            ),
            MenuItemOptimade(title='Optimade'),
            MenuItemVisibility(),
            MenuItemCustomQuantities(title='Custom Conditions'),
        ],
    ),
)
