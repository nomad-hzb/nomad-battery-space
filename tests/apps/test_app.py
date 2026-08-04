def test_importing_app():
    # this will raise an exception if pydantic model validation fails for th app
    from nomad_battery_space.apps import hzb_bat_search_app_entry_point

    assert hzb_bat_search_app_entry_point.app.label == 'BS ELN'


def test_voila_finder_app():
    """Test that the voila finder app is importable and valid."""
    from nomad_battery_space.apps.voila_finder_app import voila_finder_app
    from nomad_battery_space.schema_packages.utilities.voila_notebook import (
        BS_VoilaNotebook,
    )

    # Check that the app imports successfully (pydantic validation)
    assert voila_finder_app.label == 'Voila'
    assert voila_finder_app.path == 'voila-battery-space'

    schema_def = BS_VoilaNotebook.m_def
    assert schema_def is not None, "BS_VoilaNotebook.m_def should exist"
    
