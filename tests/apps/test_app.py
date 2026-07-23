def test_importing_app():
    # this will raise an exception if pydantic model validation fails for th app
    from nomad_battery_space.apps import hzb_bat_search_app_entry_point

    assert hzb_bat_search_app_entry_point.app.label == 'BS ELN'
