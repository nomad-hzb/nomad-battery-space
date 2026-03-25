"""
Verify that creator field data persists correctly across save/load cycles
"""
import json
import sys
import tempfile

from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.battery_sample_package import Anode


def test_creator_persistence():
    """Verify creator data survives save/load cycle"""
    print("\n=== Testing creator field data persistence ===\n")
    
    # STEP 1: Create and save
    print("STEP 1: Create entry with auto-filled creator")
    anode1 = Anode(name='persistence_test', mass=1.2, area=0.95)
    metadata1 = EntryMetadata(
        entry_name='persistence_test',
        upload_id='test_upload_persist',
        main_author='5f1c5877-5607-4d0f-b67e-9384f801a11d'
    )
    archive1 = EntryArchive(data=anode1, metadata=metadata1)
    normalize_all(archive1)
    
    print(f"  creator after normalize: {anode1.creator}")
    print(f"  type: {type(anode1.creator).__name__}")
    
    # Serialize to JSON (like saving to DB)
    print("\nSTEP 2: Serialize to JSON (simulating DB save)")
    archive_json = archive1.m_to_json()
    archive_dict = json.loads(archive_json)
    creator_saved = archive_dict['data'].get('creator')
    print(f"  creator in JSON: {creator_saved}")
    print(f"  Contains user_id: {'user_id' in creator_saved if isinstance(creator_saved, dict) else 'N/A'}")
    print(f"  Contains first_name: {'first_name' in creator_saved if isinstance(creator_saved, dict) else 'N/A'}")
    print(f"  Contains last_name: {'last_name' in creator_saved if isinstance(creator_saved, dict) else 'N/A'}")
    print(f"  Contains email: {'email' in creator_saved if isinstance(creator_saved, dict) else 'N/A'}")
    
    # Save to file (simulating database storage)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(archive_dict, f)
        temp_file = f.name
    print(f"  Saved to: {temp_file}")
    
    # STEP 3: Load from file (like reopening from DB)
    print("\nSTEP 3: Load from file (simulating DB load)")
    with open(temp_file) as f:
        archive_dict_loaded = json.load(f)
    
    # STEP 4: Deserialize
    print("\nSTEP 4: Deserialize from JSON")
    archive2 = EntryArchive.m_from_dict(archive_dict_loaded)
    anode2 = archive2.data
    creator_loaded = anode2.creator
    
    print(f"  creator after reload: {creator_loaded}")
    print(f"  type: {type(creator_loaded).__name__}")
    print(f"  first_name: {getattr(creator_loaded, 'first_name', 'N/A')}")
    print(f"  last_name: {getattr(creator_loaded, 'last_name', 'N/A')}")
    print(f"  email: {getattr(creator_loaded, 'email', 'N/A')}")
    
    # STEP 5: Verify data integrity
    print("\nSTEP 5: Verify data integrity")
    
    checks = [
        ('Has first_name', hasattr(creator_loaded, 'first_name') and creator_loaded.first_name),
        ('Has last_name', hasattr(creator_loaded, 'last_name') and creator_loaded.last_name),
        ('Has email', hasattr(creator_loaded, 'email') and creator_loaded.email),
        ('first_name is "Svetlana"', getattr(creator_loaded, 'first_name', '') == 'Svetlana'),
        ('last_name is "Grinman"', getattr(creator_loaded, 'last_name', '') == 'Grinman'),
    ]
    
    all_pass = True
    for check_name, check_result in checks:
        status = "✓" if check_result else "✗"
        print(f"  {status} {check_name}")
        all_pass = all_pass and check_result
    
    if all_pass:
        print("\n✓✓✓ SUCCESS: Creator field data persists correctly!")
        print("\nNOTE: The 'User account' dropdown won't populate in the local instance")
        print("because the local NOMAD can't fetch User objects from Keycloak.")
        print("But the author information IS correctly stored and will display")
        print("in the manual entry fields (First name, Last name, Email, etc.)")
    else:
        print("\n✗ FAILURE: Some data was lost!")
        return False
    
    # Clean up
    import os
    os.unlink(temp_file)
    return all_pass


if __name__ == '__main__':
    success = test_creator_persistence()
    sys.exit(0 if success else 1)
