"""
Test full round-trip: creator field normalized, serialized, and ready for display
"""
import json

from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.battery_sample_package import Anode


def test_creator_roundtrip():
    """Test creator field through full save/load cycle"""
    print("\n=== Testing creator field round-trip ===\n")
    
    # Step 1: Create and normalize
    print("STEP 1: Create Anode with metadata containing main_author")
    anode_data = Anode(name='roundtrip_test', mass=1.2, area=0.95)
    user_id = '5f1c5877-5607-4d0f-b67e-9384f801a11d'
    metadata = EntryMetadata(
        entry_name='roundtrip_test',
        upload_id='test_upload_roundtrip',
        main_author=user_id
    )
    archive = EntryArchive(data=anode_data, metadata=metadata)
    
    print("  Before normalize:")
    print(f"    creator = {anode_data.creator}")
    print(f"    metadata.main_author = {metadata.main_author}")
    
    # Step 2: Normalize
    print("\nSTEP 2: Call normalize_all()")
    normalize_all(archive)
    
    print("  After normalize:")
    print(f"    creator = {anode_data.creator}")
    print(f"    creator type = {type(anode_data.creator).__name__}")
    
    # Step 3: Serialize to JSON (what gets saved to DB)
    print("\nSTEP 3: Serialize archive to JSON (for storage)")
    archive_json = archive.m_to_json()
    archive_dict = json.loads(archive_json)
    
    if 'data' in archive_dict and 'creator' in archive_dict['data']:
        creator_value = archive_dict['data']['creator']
        print(f"  ✓ creator in serialized data: '{creator_value}'")
        print(f"    type: {type(creator_value).__name__}")
        
        # Step 4: Verify it can be deserialized back
        print("\nSTEP 4: Deserialize from JSON (loading from DB)")
        
        # Create a new archive from the dict
        archive_reloaded = EntryArchive.m_from_dict(archive_dict)
        print(f"  Reloaded creator: {archive_reloaded.data.creator}")
        print(f"  Reloaded creator type: {type(archive_reloaded.data.creator).__name__}")
        
        if archive_reloaded.data.creator:
            creator = archive_reloaded.data.creator
            print("\nSTEP 5: Creator object ready for GUI display")
            print(f"  Has user_id: {hasattr(creator, 'user_id')}")
            if hasattr(creator, 'user_id'):
                print(f"  user_id value: {creator.user_id}")
            print(f"  Has name: {hasattr(creator, 'name')}")
            if hasattr(creator, 'name'):
                print(f"  name value: {creator.name}")
            print(f"  Has first_name: {hasattr(creator, 'first_name')}")
            if hasattr(creator, 'first_name'):
                print(f"  first_name value: {creator.first_name}")
            print(f"  Has last_name: {hasattr(creator, 'last_name')}")
            if hasattr(creator, 'last_name'):
                print(f"  last_name value: {creator.last_name}")
                
            print("\n✓✓✓ SUCCESS: Creator field is ready for GUI to display!")
            print("\nFor GUI component (AuthorEditQuantity):")
            print(f"  The component will receive creator = {creator}")
            print(f"  It should display: {getattr(creator, 'name', 'N/A')} ({getattr(creator, 'affiliation', 'N/A')})")
        else:
            print("\n✗ ERROR: creator is not set after deserialization!")
    else:
        print("  ✗ creator NOT in serialized data!")
        print(f"    available fields: {list(archive_dict['data'].keys())}")


if __name__ == '__main__':
    test_creator_roundtrip()
