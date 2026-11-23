from nomad_battery_space.dashboards.markdown_page import create_markdown_app

SOURCE_URL = 'https://github.com/nomad-hzb/hzb-bat-image/blob/main/CHANGELOG.md'

app = create_markdown_app(SOURCE_URL)
