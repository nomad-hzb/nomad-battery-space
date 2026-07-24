from nomad.config.models.ui import (
    App,
    Column,
    FilterMenu,
    FilterMenus,
    FilterMenuSizeEnum,
    Filters,
    Format,
    ModeEnum,
    RowActionNorth,
    RowActions,
    RowDetails,
    Rows,
    RowSelection,
)

schema_name = (
    'nomad_battery_space.schema_packages.utilities.voila_notebook.BS_VoilaNotebook'
)
voila_finder_app = App(
    label='Voilá',
    path='voila-battery-space',
    category='HZB battery space',
    description='Find and launch your Voilá Tools',
    filters=Filters(
        include=[
            f'*#{schema_name}',
        ]
    ),
    filters_locked={'section_defs.definition_qualified_name': f'{schema_name}'},
    filter_menus=FilterMenus(
        options={
            'custom_quantities': FilterMenu(
                label='Notebooks', size=FilterMenuSizeEnum.L
            ),
            'author': FilterMenu(label='Author', size=FilterMenuSizeEnum.M),
            'metadata': FilterMenu(label='Visibility / IDs'),
        }
    ),
    columns=[
        Column(quantity=f'data.name#{schema_name}', selected=True),
        Column(
            quantity='entry_type',
            label='Entry type',
            align='left',
            selected=False,
        ),
        Column(
            quantity='entry_create_time',
            label='Entry time',
            align='left',
            selected=True,
            format=Format(mode=ModeEnum.DATE),
        ),
        Column(
            quantity='upload_name',
            label='Upload name',
            align='left',
            selected=True,
        ),
        Column(
            quantity='authors',
            label='Authors',
            align='left',
            selected=True,
        ),
        Column(quantity='entry_id'),
        Column(quantity='upload_id'),
        Column(quantity=f'data.notebook_file#{schema_name}'),
        #Column(quantity=f'data.tags#{schema_name}'),
    ],
    rows=Rows(
        actions=RowActions(
            items=[
                RowActionNorth(
                    tool_name='voila',
                    filepath=f'data.notebook_file#{schema_name}',
                    description='Launch voila tool in new tab',
                    icon='rocket_launch',
                ),
            ]
        ),
        details=RowDetails(),
        selection=RowSelection(),
    ),

    # Controls the default dashboard shown in the search interface
    # dashboard=Dashboard(
    #     widgets=[
    #         WidgetTerms(
    #             title='Filter Tags',
    #             layout={
    #                 'sm': Layout(minH=3, minW=3, h=6, w=6, y=0, x=0),
    #                 'md': Layout(minH=3, minW=3, h=6, w=6, y=0, x=0),
    #                 'lg': Layout(minH=3, minW=3, h=6, w=6, y=0, x=0),
    #                 'xl': Layout(minH=3, minW=3, h=6, w=6, y=0, x=0),
    #                 'xxl': Layout(minH=3, minW=3, h=6, w=6, y=0, x=0),
    #             },
    #             search_quantity='results.eln.tags',
    #             showinput=True,
    #             scale='linear',
    #         ),
    #     ]
    # ),
)
