from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuItemVisibility,
    SearchQuantities,
)

from .hzb_bat_search_helper import (
    ClassInfo,
    create_class_filter_menus,
)

# i see a problem here, because it is only referencing one type of batteries. not used currently
schema = 'nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery'


# IDEA: SearchApp Menu's are built directly in schema class by implementing an inherited method. In that method same method of parent class creates parent search menu, and concrete class adds own entries.
# Advantage: smaller search app

classes: list[ClassInfo] = [
    ClassInfo('CoinCellBattery', 'hzb_bs_assembly_package', False, False, False, True),
    ClassInfo('ElectrodeMaterial', 'hzb_bs_package', False, True, True, True),
    ClassInfo('ElectrodeSheet', 'hzb_bs_package', True, False, True, True),
    ClassInfo('ElectrodeSample', 'hzb_bs_package', True, False, True, True),
    ClassInfo('SeparatorStock', 'hzb_bs_package', True, False, True, True),
    ClassInfo('SeparatorSample', 'hzb_bs_package', True, False, False, True),
    ClassInfo('ElectrolyteStock', 'hzb_bs_package', False, True, True, True),
    ClassInfo('ElectrolyteSample', 'hzb_bs_package', False, True, False, True),
    ClassInfo('BS_Chemical', 'hzb_bs_package', False, False, False, True),
]
class_filter_menus: dict[str, Menu] = create_class_filter_menus(classes)


hzb_bat_search_app = App(
    label='BS ELN',
    path='samples',
    category='HZB battery space',
    description='Provides filters to quickly find your samples and experimental data',
    search_quantities=SearchQuantities(
        include=[
            '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.CoinCellBattery',
            # '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.CylindricalCellBattery',
            # '*#nomad_battery_space.schema_packages.hzb_bs_assembly_package.PouchCellBattery',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.Electrode',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSheet',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeSample',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BS_Chemical',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrodeMaterial',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorStock',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.SeparatorSample',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.BatterySample',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteStock',
            '*#nomad_battery_space.schema_packages.hzb_bs_package.ElectrolyteSample',
        ]
    ),
    # filters_locked={'section_defs.definition_qualified_name': [schema]},
    columns=[
        Column(quantity='entry_name', selected=True),
        Column(quantity='entry_type', selected=True),
        Column(quantity='upload_name', selected=True),
        Column(quantity='entry_create_time', selected=True),
    ],
    menu=Menu(
        title='Filter',
        size='sm',
        items=[
            Menu(
                title='Author & Visibilities',
                items=[
                    MenuItemTerms(
                        search_quantity='authors.name',
                        title='Author',
                        options=10,
                    ),
                    MenuItemVisibility(),
                ],
            ),
            Menu(
                title='Entry Properties',
                size='xxl',
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
                size='xxl',
                items=[
                    MenuItemPeriodicTable(
                        search_quantity='results.material.elements',
                        title='Elements',
                        # width='36',
                    ),
                ],
            ),
            class_filter_menus['CoinCellBattery'],
            class_filter_menus['ElectrodeMaterial'],
            class_filter_menus['ElectrodeSheet'],
            class_filter_menus['ElectrodeSample'],
            class_filter_menus['SeparatorStock'],
            class_filter_menus['SeparatorSample'],
            class_filter_menus['ElectrolyteStock'],
            class_filter_menus['ElectrolyteSample'],
            class_filter_menus['BS_Chemical'],
            MenuItemTerms(search_quantity='results.eln.tags'),
            # MenuItemOptimade(title='Optimade'),
            # MenuItemCustomQuantities(title='Custom Conditions'),
        ],
    ),
)
