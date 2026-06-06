from nomad.metainfo import Quantity


def extract_elements(component):
    """
    Extract chemical elements from a component with hierarchical aggregation support.
    
    This utility function extracts all unique element symbols from a component,
    prioritizing aggregated_elements (which contain hierarchically aggregated elements
    from referenced components) and falling back to elemental_composition (for 
    base components like BS_Chemical).
    
    Args:
        component: The component object to extract elements from
        
    Returns:
        set: Set of element strings found in the component
    """
    elements = set()
    if component is None:
        return elements
    
    # Priority 1: Use aggregated_elements if available (hierarchical aggregation)
    agg_elems = getattr(component, 'aggregated_elements', None)
    if agg_elems:
        elements.update(agg_elems)
    
    # Priority 2: Fall back to elemental_composition for base components
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