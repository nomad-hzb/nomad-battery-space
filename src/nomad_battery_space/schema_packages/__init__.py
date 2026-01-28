from nomad.config.models.plugins import SchemaPackageEntryPoint


class BatterySamplePackageEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_battery_space.schema_packages.battery_sample_package import (
            m_package,
        )

        return m_package

class BatteryCellAssemblyPackageEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_battery_space.schema_packages.battery_cell_assembly_package import (
            m_package,
        )

        return m_package


bat_schema_package = BatterySamplePackageEntryPoint(
    name='bat_sample',
    description='Schema package for battery sample @HZB.',
)

bat_cell_assembly_package = BatteryCellAssemblyPackageEntryPoint(
    name='bat_cell_assembly',
    description='Schema package for battery cell assembly @HZB.',
)

