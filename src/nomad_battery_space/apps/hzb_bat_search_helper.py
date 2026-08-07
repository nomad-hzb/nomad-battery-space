from nomad.config.models.ui import (
    Axis,
    Menu,
    MenuItemCustomQuantities,
    MenuItemDefinitions,
    MenuItemHistogram,
    MenuItemNestedObject,
    MenuItemOptimade,
    MenuItemPeriodicTable,
    MenuItemTerms,
    MenuItemVisibility,
)


def create_chemical_properties_menu(package_name: str, class_name: str) -> Menu:
    return Menu(
        title='Chemical Properties',
        items=[
            MenuItemTerms(
                search_quantity=f'data.chemicals.chemical_name#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Chemical Name',
                options=5,
            ),
            MenuItemTerms(
                search_quantity=f'data.chemicals.role#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Role',
                options=5,
            ),
            MenuItemHistogram(
                title='Volume',
                x=Axis(
                    search_quantity=f'data.chemicals.volume#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Mass',
                x=Axis(
                    search_quantity=f'data.chemicals.mass#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Concentration (Mol)',
                x=Axis(
                    search_quantity=f'data.chemicals.concentration_mol#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Concentration (Mass)',
                x=Axis(
                    search_quantity=f'data.chemicals.concentration_mass#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Fraction',
                x=Axis(
                    search_quantity=f'data.chemicals.fraction#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Mass Fraction',
                x=Axis(
                    search_quantity=f'data.chemicals.mass_fraction#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Volume Fraction',
                x=Axis(
                    search_quantity=f'data.chemicals.volume_fraction#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
        ],
    )


def create_product_info_menu(package_name: str, class_name: str) -> Menu:
    return Menu(
        title='Product Info',
        items=[
            MenuItemTerms(
                search_quantity=f'data.product_info.supplier#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Supplier',
                options=5,
            ),
            MenuItemTerms(
                search_quantity=f'data.product_info.product_number#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Product Number',
                options=5,
            ),
            MenuItemTerms(
                search_quantity=f'data.product_info.lot_number#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='LOT Number',
                options=5,
            ),
            MenuItemHistogram(
                title='Product Volume',
                x=Axis(
                    search_quantity=f'data.product_info.product_volume#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Product Weight',
                x=Axis(
                    search_quantity=f'data.product_info.product_weight#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Shipping Date',
                x=Axis(
                    search_quantity=f'data.product_info.shipping_date#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Opening Date',
                x=Axis(
                    search_quantity=f'data.product_info.opening_date#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Cost',
                x=Axis(
                    search_quantity=f'data.product_info.cost#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
        ],
    )


def create_dimensions_and_weights_items(
    package_name: str, class_name: str
) -> list[
    MenuItemTerms
    | MenuItemHistogram
    | MenuItemPeriodicTable
    | MenuItemNestedObject
    | MenuItemVisibility
    | MenuItemDefinitions
    | MenuItemOptimade
    | MenuItemCustomQuantities
    | Menu
]:
    return [
        MenuItemHistogram(
            title='Thickness',
            x=Axis(
                search_quantity=f'data.dimensions_and_weights.thickness#nomad_battery_space.schema_packages.{package_name}.{class_name}'
            ),
        ),
        MenuItemHistogram(
            title='Mass',
            x=Axis(
                search_quantity=f'data.dimensions_and_weights.mass#nomad_battery_space.schema_packages.{package_name}.{class_name}'
            ),
        ),
    ]


def create_volume_and_weights_items(
    package_name: str, class_name: str
) -> list[
    MenuItemTerms
    | MenuItemHistogram
    | MenuItemPeriodicTable
    | MenuItemNestedObject
    | MenuItemVisibility
    | MenuItemDefinitions
    | MenuItemOptimade
    | MenuItemCustomQuantities
    | Menu
]:
    return [
        MenuItemHistogram(
            title='Volume',
            x=Axis(
                search_quantity=f'data.volume_and_weights.volume#nomad_battery_space.schema_packages.{package_name}.{class_name}'
            ),
        ),
        MenuItemHistogram(
            title='Mass',
            x=Axis(
                search_quantity=f'data.volume_and_weights.mass#nomad_battery_space.schema_packages.{package_name}.{class_name}'
            ),
        ),
    ]


def create_synthesis_menu_for_electrodematerial(
    package_name: str, class_name: str
) -> Menu:
    return Menu(
        title=f'{class_name} synthesis',
        items=[
            # This is not working (path depth to high?)
            MenuItemTerms(
                search_quantity=f'data.synthesis.references.doi#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='DOI',
                options=5,
            ),
            MenuItemTerms(
                search_quantity=f'data.synthesis.references.paper_reference#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='paper URL',
                options=5,
            ),
        ],
    )


def create_activematerialcomponent_menu_for_electrodesheet(
    package_name: str, class_name: str
) -> Menu:
    return Menu(
        title='Material Properties',
        items=[
            MenuItemTerms(
                search_quantity=f'data.electrode_materials.material_name#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Material Name',
                options=5,
            ),
            MenuItemTerms(
                search_quantity=f'data.electrode_materials.role#nomad_battery_space.schema_packages.{package_name}.{class_name}',
                title='Role',
                options=5,
            ),
            MenuItemHistogram(
                title='Mass',
                x=Axis(
                    search_quantity=f'data.electrode_materials.mass#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
            MenuItemHistogram(
                title='Weight Percent',
                x=Axis(
                    search_quantity=f'data.electrode_materials.wt_percent#nomad_battery_space.schema_packages.{package_name}.{class_name}'
                ),
            ),
        ],
    )


class ClassInfo:
    class_name: str
    package_name: str
    dimensions_and_weights: bool
    volume_and_weights: bool
    chemical_reference: bool
    product_info: bool

    def __init__(  # noqa: PLR0913, PLR0917
        self,
        class_name: str,
        package_name: str,
        dimensions_and_weights: bool,
        volume_and_weights: bool,
        chemical_reference: bool,
        product_info: bool,
    ):
        self.class_name = class_name
        self.package_name = package_name
        self.dimensions_and_weights = dimensions_and_weights
        self.volume_and_weights = volume_and_weights
        self.chemical_reference = chemical_reference
        self.product_info = product_info


def create_class_filter_menus(classes: list[ClassInfo]) -> dict[str, Menu]:
    """
    This function creates filter menus for all classes

    Suggestion of a redesign:
    To have less "if"s in the code, it would be better to redesign the class ingeritance
    structure and let each class and parent class create their own search app filters
    by calling an inherited method and the parents one.
    Then, this method is no longer needed.
    """

    class_filter_menus: dict[str, Menu] = {}

    for info in classes:
        menu = Menu(title=f'{info.class_name} Properties', items=[])

        ### adding common filters for the classes:

        if info.chemical_reference:
            menu.items.append(
                create_chemical_properties_menu(info.package_name, info.class_name)
            )

        if info.product_info:
            menu.items.append(
                create_product_info_menu(info.package_name, info.class_name)
            )

        if info.dimensions_and_weights:
            menu.items += create_dimensions_and_weights_items(
                info.package_name, info.class_name
            )

        if info.volume_and_weights:
            menu.items += create_volume_and_weights_items(
                info.package_name, info.class_name
            )

        ###  adding custom filter for the different classes:

        if info.class_name == 'ElectrodeSheet':
            menu.items.append(
                create_activematerialcomponent_menu_for_electrodesheet(
                    info.package_name, info.class_name
                )
            )
            menu.items.append(
                MenuItemTerms(
                    search_quantity=f'data.casting_procedure#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}',
                    title='Casting Procedure',
                    options=10,
                ),
            )

        if info.class_name == 'ElectrolyteStock':
            menu.items.append(
                MenuItemTerms(
                    search_quantity=f'data.state#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}',
                    title='State',
                    options=5,
                ),
            )

        if info.class_name == 'CoinCellBattery':
            menu.items += [
                MenuItemTerms(
                    search_quantity=f'data.case_id#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}',
                    title='Case ID',
                    options=5,
                ),
                MenuItemTerms(
                    search_quantity=f'data.case_crimp#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}',
                    title='Case Crimp',
                    options=5,
                ),
                MenuItemHistogram(
                    title='Pressure',
                    x=Axis(
                        search_quantity=f'data.pressure#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}'
                    ),
                ),
            ]

        if info.class_name == 'ElectrodeMaterial':
            menu.items += [
                # not working
                # create_synthesis_menu_for_electrodematerial(
                #     info.package_name, info.class_name
                # ),
                MenuItemHistogram(
                    title='Yield',
                    x=Axis(
                        search_quantity=f'data.yield_percent#nomad_battery_space.schema_packages.{info.package_name}.{info.class_name}'
                    ),
                ),
            ]

        class_filter_menus[info.class_name] = menu

    return class_filter_menus
