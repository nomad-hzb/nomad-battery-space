from nomad.config.models.plugins import SchemaPackageEntryPoint


class BatterySamplePackageEntryPoint(SchemaPackageEntryPoint):

    def load(self):
        from nomad_battery_space.schema_packages.battery_sample_prototype import m_package

        return m_package


bat_schema_package = BatterySamplePackageEntryPoint(
    name='bat_sample',
    description='Schema package for battery sample @HZB.',
)
