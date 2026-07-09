from nomad.datamodel.results import Material, Results
from nomad.metainfo import Quantity


def extract_elements(component, use_aggregated=True):
    """
    Extract chemical elements from a component with hierarchical aggregation support.
    
    This function extracts all unique element symbols from a component.
    For referenced components, it prioritizes aggregated_elements (hierarchical).
    For the component itself during normalization, set use_aggregated=False to avoid 
    using outdated aggregated_elements.
    
    Args:
        component: The component object to extract elements from
        use_aggregated: If True, use aggregated_elements from referenced components.
                       If False, only use elemental_composition (to avoid circular reference
                       during normalization of the component itself).
        
    Returns:
        set: Set of element strings found in the component
    """
    elements = set()
    if component is None:
        return elements
    
    # For referenced components: use aggregated_elements if available (hierarchical)
    if use_aggregated:
        agg_elems = getattr(component, 'aggregated_elements', None)
        if agg_elems:
            elements.update(agg_elems)
            return elements  
    
    # Extract from elemental_composition (direct composition of this component)
    ec_list = getattr(component, 'elemental_composition', None)
    if ec_list:
        for comp in ec_list:
            el = getattr(comp, 'element', None)
            if el:
                elements.add(str(el))
    
    return elements


def validate_required(value, *, name: str) -> None:
    """Validate that a required field has a non-empty value.

    Raises a ``ValueError`` when ``value`` is ``None`` or an empty or
    whitespace-only string. Intended for use by schema package normalizers
    (e.g., in `battery_sample_package.py`).

    Args:
        value: The value to validate.
        name: The human-readable name of the field used in the exception
            message.

    Raises:
        ValueError: If ``value`` is ``None`` or an empty/whitespace-only
            string.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError(f"'{name}' is mandatory and must not be empty.")


def create_millimeter_quantity(label, description, required=False):
    """Helper function to create millimeter-based float quantities."""
    return Quantity(
        type=float,
        unit="millimeter",
        description=description,
        a_eln={
            "component": "NumberEditQuantity",
            "label": label,
            "defaultDisplayUnit": "millimeter",
            "required": required,
        },
    )


def create_string_quantity(label, description=None, required=False):
    """Helper function to create string quantities."""
    return Quantity(
        type=str,
        description=description,
        a_eln={
            "component": "StringEditQuantity",
            "label": label,
            "required": required,
        },
    )


def create_area_quantity(label: str = "area", description: str = None, required: bool = False) -> Quantity:
    """
    Helper function to create area-based float quantities with centimeter squared units.
    
    Args:
        label: Display label for the quantity (default: "area")
        description: Description of the quantity (default: None)
        required: Whether the field is required (default: False)
    
    Returns:
        A Quantity configured for area measurements in cm²
    """
    if description is None:
        description = f'Geometric surface {label.lower()} of the component.'
    
    return Quantity(
        type=float,
        description=description,
        a_eln={
            "component": "NumberEditQuantity",
            "label": label,
            "defaultDisplayUnit": "centimeter ** 2"
        },
        unit='centimeter ** 2',
    )


def normalize_referenced_components(chemicals=None, materials=None, archive=None, logger=None):
    """
    Normalize all referenced child components (chemicals and/or materials).
    
    Args:
        chemicals: List of chemical references to normalize
        materials: List of material components to normalize
        archive: The archive object
        logger: The logger object
    """
    if chemicals:
        for chem_ref in chemicals:
            if chem_ref.chemical:
                chem_ref.chemical.normalize(archive, logger)
    
    if materials:
        for mat_comp in materials:
            if mat_comp.material:
                mat_comp.material.normalize(archive, logger)


def collect_and_store_elements(component, archive, chemicals=None, materials=None, referenced_components=None):
    """
    Collect elements from component sources and store in aggregated_elements and results.
    
    Args:
        component: The component object to store elements in
        archive: The archive object for results storage
        chemicals: List of chemical references to collect from
        materials: List of material components to collect from
        referenced_components: List of directly referenced components to collect from (e.g., electrode_sheet, separator_stock)
    """
    elements = set()
    
    # From own elemental_composition
    elements.update(extract_elements(component, use_aggregated=False))
    
    # From chemicals
    if chemicals:
        for chem_ref in chemicals:
            if chem_ref.chemical:
                elements.update(extract_elements(chem_ref.chemical, use_aggregated=True))
    
    # From materials
    if materials:
        for mat_comp in materials:
            if mat_comp.material:
                elements.update(extract_elements(mat_comp.material, use_aggregated=True))
    
    # From referenced components (e.g., electrode_sheet, separator_stock)
    if referenced_components:
        for ref_comp in referenced_components:
            if ref_comp:
                elements.update(extract_elements(ref_comp, use_aggregated=True))
    
    # Store aggregated elements
    elements_list = sorted(elements)
    component.aggregated_elements = elements_list
    
    # Save to results
    if archive:
        if archive.results is None:
            archive.results = Results()
        if archive.results.material is None:
            archive.results.material = Material()
        archive.results.material.elements = list(elements_list)
