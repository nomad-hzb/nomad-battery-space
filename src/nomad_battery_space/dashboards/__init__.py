from nomad.config.models.plugins import DashboardEntryPoint


class ChangelogDashboardEntryPoint(DashboardEntryPoint):
    def load(self):
        from nomad_battery_space.dashboards.changelog import app

        return app


changelog_dashboard = ChangelogDashboardEntryPoint(
    name='Changelog',
    id_url_safe='changelog',
    description='Changelog of the HZB battery NOMAD Oasis.',
    launch_modes=['embedded', 'tab'],
)


class MaintenanceDashboardEntryPoint(DashboardEntryPoint):
    def load(self):
        from nomad_battery_space.dashboards.maintenance import app

        return app


maintenance_dashboard = MaintenanceDashboardEntryPoint(
    name='Maintenance',
    id_url_safe='maintenance',
    description='Announcements, links and server maintenance of HZB Battery Data Space.',
    launch_modes=['embedded', 'tab'],
)
