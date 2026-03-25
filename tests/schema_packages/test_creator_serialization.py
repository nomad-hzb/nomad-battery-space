"""
Test that creator field is properly serialized in archive responses
"""
import json

from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.battery_sample_package import Anode


def test_creator_serialization():
    """Test that creator field is properly serialized to JSON"""
    print("\n=== Testing creator field serialization ===")
    
    anode_data = Anode(name='test_serialize', mass=1.2, area=0.95)
    
    user_id = '5f1c5877-5607-4d0f-b67e-9384f801a11d'
    metadata = EntryMetadata(
        entry_name='test_serialize',
        upload_id='test_upload_serialize',
        main_author=user_id
    )
    
    archive = EntryArchive(data=anode_data, metadata=metadata)
    
    print("\n1. Before normalize:")
    print(f"   creator = {anode_data.creator}")
    
    # Normalize
    normalize_all(archive)
    
    print("\n2. After normalize:")
    print(f"   creator = {anode_data.creator}")
    print(f"   creator type = {type(anode_data.creator)}")
    
    # Try to convert archive to dict (what would be serialized)
    print("\n3. Attempting to serialize archive to dict:")
    try:
        archive_dict = archive.m_to_dict()
        print("   ✓ Archive converted to dict successfully")
        
        # Check if creator is in the serialized data
        if 'data' in archive_dict:
            print(f"   'data' key exists: {list(archive_dict['data'].keys())}")
            if 'creator' in archive_dict['data']:
                creator_value = archive_dict['data']['creator']
                print("   ✓ 'creator' found in data!")
                print(f"     Value: {creator_value}")
                print(f"     Type: {type(creator_value)}")
            else:
                print("   ✗ 'creator' NOT found in data")
                print(f"     Available fields: {list(archive_dict['data'].keys())}")
        
        # Convert to JSON to see the full serialized form
        print("\n4. Serializing to JSON:")
        try:
            archive_json = archive.m_to_json()
            archive_obj = json.loads(archive_json)
            if 'data' in archive_obj:
                if 'creator' in archive_obj['data']:
                    print("   ✓ 'creator' is in JSON data")
                    print(f"     Value: {archive_obj['data']['creator']}")
                else:
                    print("   ✗ 'creator' NOT in JSON data")
                    print(f"     Fields in data: {list(archive_obj['data'].keys())}")
        except Exception as e:
            print(f"   Error converting to JSON: {e}")
            
    except Exception as e:
        print(f"   Error converting to dict: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_creator_serialization()
