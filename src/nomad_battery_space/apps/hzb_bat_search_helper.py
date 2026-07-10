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
                title='Concentration',
                x=Axis(
                    search_quantity=f'data.chemicals.concentration_mol#nomad_battery_space.schema_packages.{package_name}.{class_name}'
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


class SchemaClassMetaInfo:
    class_name: str
    package_name: str
    dimensions_and_weights: bool
    volume_and_weights: bool
    chemical_reference: bool
    product_info: bool

    def __init__(  # noqa: PLR0913
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


def create_class_filter_menus() -> dict[str, Menu]:

    classes: list[SchemaClassMetaInfo] = [
        SchemaClassMetaInfo(
            'ElectrodeSheet', 'hzb_bs_package', True, False, True, True
        ),
        SchemaClassMetaInfo(
            'ElectrodeSample', 'hzb_bs_package', True, False, True, True
        ),
        SchemaClassMetaInfo(
            'SeparatorStock', 'hzb_bs_package', True, False, True, True
        ),
        SchemaClassMetaInfo(
            'SeparatorSample', 'hzb_bs_package', True, False, True, True
        ),
        SchemaClassMetaInfo(
            'ElectrolyteStock', 'hzb_bs_package', False, True, True, True
        ),
        SchemaClassMetaInfo(
            'ElectrolyteSample', 'hzb_bs_package', False, True, False, True
        ),
    ]

    class_filter_menus: dict[str, Menu] = {}

    for info in classes:
        menu = Menu(title=f'{info.class_name} Properties', items=[])

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

        if info.class_name == 'ElectrodeSheet':
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

        class_filter_menus[info.class_name] = menu

    return class_filter_menus
