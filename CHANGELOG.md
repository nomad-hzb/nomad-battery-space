# Changelog

All notable changes to this plugin will be documented in this file.

## [0.2.3] - 2026-08-04

### Added
- **Schema class diagrams**: D2 format diagrams for visual documentation of schema relationships

### Changed
- **Search App**: Refined and improved search interface with enhanced filter functionality
- **Result columns**: Improved column configuration and display in search results
- **BS_Chemical filter group**: Aligned filter structure for better organization
- **Voila Finder App**: Stability improvements and CI/CD fixes

### Fixed
- Multiple CI/CD pipeline issues and GitHub Actions compatibility
- Added constraint dependencies for pymatgen-core

## [0.2.2] - 2026-07-23

### Added
- **Voila Finder App**: New search application for discovering and launching Voila notebooks
- **BS_VoilaNotebook Schema**: Extended Voila notebook schema for batch notebook uploads
- **Voila launch functionality**: Direct launch of Voila dashboards from search results

### Fixed
- Error handling for non-jupyter file uploads in Voila notebook validation

## [0.2.1] - 2026-07-20

### Fixed
- Bug fix for 'notes' field in ElectrolyteStock schema
- Fixed default value 'manual' in case_crimp for coin cells

## [0.2.0] - 2026-07-10

### Added
- **Search App Interface**: New search app with filter menus for battery data discovery
- **CoinCellBattery search filters**: Specialized search filters for coin cell batteries
- **Electrolyte Search Filters**: Advanced search filters for Electrolyte classes
- **BS_ChemicalReference properties**: Extended chemical reference properties in search app
- **OPTIMADE filter support**: Integration with OPTIMADE for materials discovery
- **Filter submenus**: Hierarchical filter menus for various schema classes 
- **Histogram data thickness filters**: Data analysis filters for material properties 
- **Search functionality**: Author filtering and type-based search capabilities 

### Changed
- **Utilities Subpackage**: Reorganized helper classes and utilities structure 
- **Redesigned filter menus**: Improved UX for search app with better organization
- **Class filter menus structure**: Enhanced class filtering hierarchy
  
### Fixed
- Removed unnecessary chemicals filter from SeparatorSample filters
- Fixed imports for nomad classes (Ruff linting)
- Various code improvements and test fixes

## [0.1.1] - 2026-06-25

### Added
- **New Data Model**: Complete refactoring of battery components data model based on **3-tier electrode architecture**
  - Restructured entire battery components package with new hierarchical design
  - Created new ``hzb_bs_assembly_package`` and enhanced ``hzb_bs_package``
  - Deprecated old battery assembly and sample packages
- **Automatic element aggregation**: Improved ``aggregated_elements`` resolution for all battery components 
- **Dimension/Mass/Volume**: Restructured component property storage 
- **ProductInfo/Supplier fields**: Extended all battery entity classes with supplier information 
- **Enhanced filter menus**: Improved search and discovery capabilities
- **Casting procedure dropdown**: Added suggestions for ElectroSheet casting procedures 

### Changed
- Pure substance field made more flexible across schemas
- Hierarchical ``aggregated_elements`` improved
- Dependencies: Pinned nomad-baseclasses to v1.0.1

### Fixed
- Description fields validation fixes
- Code improvements and linting fixes

## [0.1.0] - 2026-04-17

### Added
- Imported HZB baseclasses for reusing standardized data schemas
- Added **Voila schema** support for interactive visualizations and batch upload functionality
  
### Initial Release
This release was a snapshot of the existing development state. 
The foundational work was done in the development phase (Nov 2025 - Apr 2026):

- **Battery Cell Schemas**: CoinCellBattery, PouchCell, and CylindricalCell schemas 
- **Battery Component Classes**: Anode, Cathode, Electrolyte, and Separator schemas
- **Component References**: Schema for tracking battery component dependencies 
- **Testing Infrastructure**: Pytest test suite with reference validation
- **Documentation**: Initial documentation structure and sample registration
- **Code Quality**: Ruff linting fixes, code refactoring, and mandatory field validation

