from nomad.config.models.plugins import SchemaPackageEntryPoint


class HZBBSPackageEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_battery_space.schema_packages.hzb_bs_package import (
            m_package,
        )

        return m_package


class HZBBSAssemblyPackageEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_battery_space.schema_packages.hzb_bs_assembly_package import (
            m_package,
        )

        return m_package


hzb_bs_package = HZBBSPackageEntryPoint(
    name='hzb_bs',
    description='Schema package for HZB battery samples.',
)

hzb_bs_assembly_package = HZBBSAssemblyPackageEntryPoint(
    name='hzb_bs_assembly',
    description='Schema package for HZB battery assembly samples.',
)

