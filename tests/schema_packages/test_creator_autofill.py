"""
Test that creator field is auto-filled with main_author during normalization
"""
from nomad.client import normalize_all
from nomad.datamodel import EntryArchive, EntryMetadata

from nomad_battery_space.schema_packages.battery_sample_package import Anode


def test_anode_creator_autofill(capsys):
    """Test that creator is auto-filled from archive.metadata.main_author"""
    
    # Create a test archive manually with metadata
    anode_data = Anode(name='test_anode_01', mass=1.2, area=0.95)
    
    # Create metadata with a main_author (as string user_id)
    metadata = EntryMetadata(
        entry_name='test_anode_01',
        upload_id='test_upload_123',
        main_author='test_user_id'  # Simulate the upload creator as string
    )
    
    archive = EntryArchive(data=anode_data, metadata=metadata)
    
    # Before normalization, creator should be None
    print("\n=== BEFORE NORMALIZATION ===")
    print(f"Creator: {anode_data.creator}")
    print(f"Creator type: {type(anode_data.creator)}")
    print(f"Main author: {archive.metadata.main_author}")
    print(f"Main author type: {type(archive.metadata.main_author)}")
    assert anode_data.creator is None, "Creator should be None before normalization"
    
    # Call normalize
    print("\n=== CALLING normalize_all() ===")
    normalize_all(archive)
    
    # After normalization, creator should be filled
    print("\n=== AFTER NORMALIZATION ===")
    print(f"Creator: {anode_data.creator}")
    print(f"Creator type: {type(anode_data.creator)}")
    print(f"Main author: {archive.metadata.main_author}")
    print(f"Main author type: {type(archive.metadata.main_author)}")
    
    # Check if creator was auto-filled
    if anode_data.creator:
        print("\n✓ SUCCESS: creator auto-filled")
        print(f"  Value: {anode_data.creator}")
        
        # Check if it's properly an AuthorReference
        if isinstance(anode_data.creator, str):
            print("  Note: creator is a string (user_id), not an AuthorReference object")
            print("  This might be why the GUI doesn't display it - the type needs to be resolved")
        elif hasattr(anode_data.creator, 'user_id'):
            print(f"  Creator is AuthorReference with user_id: {anode_data.creator.user_id}")
            
        assert anode_data.creator is not None, "Creator should be auto-filled"
    else:
        print("\n✗ ISSUE: creator is still None after normalization")
        print("  This means archive.metadata.main_author is empty or not accessible")
        raise AssertionError(f"Creator was not auto-filled. Main author: {archive.metadata.main_author}")
