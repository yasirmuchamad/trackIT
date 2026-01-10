# Item Asset & Non-Asset Refactoring Guide

## Overview
Refactored Item model and forms to support both Asset and Non-Asset items with specialized forms and views for each type.

## Changes Made

### 1. Model Updates

#### Item Model Enhanced
- ✅ **Added `item_type` field**: Choice between 'asset' and 'non_asset'
- ✅ **Added Non-Asset fields**:
  - `unit_of_measure` - Satuan (pcs, box, kg, dll)
  - `minimum_stock` - Minimum stock level for alerts
- ✅ **Enhanced Technical fields**: Added help text for electronic items
- ✅ **Added Properties**:
  - `is_asset` - Check if item is an asset
  - `is_non_asset` - Check if item is a non-asset
- ✅ **Updated `__str__` method**: Shows item type in display

### 2. Forms Refactored

#### Base ItemForm
- ✅ **Enhanced with field existence checks**
- ✅ **Conditional field handling** for different item types
- ✅ **Improved widget attributes** and styling

#### AssetItemForm
- ✅ **Specialized for Asset items**
- ✅ **Fields**: SKU, category, name, brand, model, technical specs
- ✅ **Hidden item_type field** (auto-set to 'asset')
- ✅ **Technical specifications**: CPU, RAM, Storage, Display, OS

#### NonAssetItemForm
- ✅ **Specialized for Non-Asset items**
- ✅ **Fields**: SKU, category, name, brand, model, inventory management
- ✅ **Hidden item_type field** (auto-set to 'non_asset')
- ✅ **Inventory fields**: Unit of measure (required), minimum stock
- ✅ **Unit suggestions**: Datalist with common units

### 3. Views Architecture

#### Specialized Views for Assets
- ✅ **AssetItemListView** - List only asset items
- ✅ **AssetItemCreateView** - Create asset items with technical specs
- ✅ **AssetItemUpdateView** - Update asset items

#### Specialized Views for Non-Assets
- ✅ **NonAssetItemListView** - List only non-asset items
- ✅ **NonAssetItemCreateView** - Create non-asset items with inventory fields
- ✅ **NonAssetItemUpdateView** - Update non-asset items

#### Enhanced General Views
- ✅ **ItemListView Enhanced**:
  - Filter by item type (all/asset/non_asset)
  - Search functionality across multiple fields
  - Pagination support
  - Statistics display (asset count, non-asset count)

### 4. URL Structure

#### New URL Patterns
```python
# Asset Item URLs
path('asset/', AssetItemListView.as_view(), name='list_asset_item'),
path('asset/create/', AssetItemCreateView.as_view(), name='create_asset_item'),
path('asset/update/<int:pk>/', AssetItemUpdateView.as_view(), name='update_asset_item'),

# Non-Asset Item URLs
path('non-asset/', NonAssetItemListView.as_view(), name='list_non_asset_item'),
path('non-asset/create/', NonAssetItemCreateView.as_view(), name='create_non_asset_item'),
path('non-asset/update/<int:pk>/', NonAssetItemUpdateView.as_view(), name='update_non_asset_item'),
```

### 5. Templates Created

#### Asset Templates
- ✅ **`asset_list.html`** - Asset items listing with technical specs
- ✅ **`asset_create.html`** - Asset creation form with technical fields

#### Non-Asset Templates
- ✅ **`non_asset_list.html`** - Non-asset items listing with inventory info
- ✅ **`non_asset_create.html`** - Non-asset creation form with inventory fields

#### Enhanced General Template
- ✅ **`list.html` Updated** - Unified view with filtering and search

### 6. Template Features

#### Asset Templates
- ✅ **Technical specifications display** (CPU, RAM, Storage, etc.)
- ✅ **Auto SKU generation** based on category and name
- ✅ **Organized form sections** (Basic Info, Technical Specs)
- ✅ **Asset-specific styling** (blue theme, chip icons)

#### Non-Asset Templates
- ✅ **Inventory management fields** (Unit, Min Stock)
- ✅ **Unit suggestions datalist** with common units
- ✅ **Auto SKU generation** with "NA-" prefix for non-assets
- ✅ **Non-asset styling** (green theme, cube icons)

#### Enhanced List Template
- ✅ **Type-based filtering** (All/Assets/Non-Assets)
- ✅ **Search functionality** across name, SKU, brand, model
- ✅ **Statistics cards** showing counts
- ✅ **Quick action buttons** for each item type
- ✅ **Conditional details display** based on item type

### 7. JavaScript Enhancements

#### Auto SKU Generation
- ✅ **Asset items**: `CAT-NAM-1234` format
- ✅ **Non-asset items**: `NA-CAT-NAM-1234` format
- ✅ **Dynamic generation** based on category and name input

#### Unit Suggestions
- ✅ **Datalist integration** for common units
- ✅ **Common units**: pcs, box, kg, liter, meter, roll, pack, etc.

### 8. Migration Created

#### Migration 0011_add_item_type_fields.py
- ✅ **Adds new fields**: item_type, unit_of_measure, minimum_stock
- ✅ **Updates existing fields**: Enhanced help text for technical specs
- ✅ **Safe migration**: All new fields are optional with defaults

## Benefits of Refactoring

### 1. Clear Separation of Concerns
- **Assets**: Focus on technical specifications and tracking
- **Non-Assets**: Focus on inventory management and stock levels
- **Unified Interface**: Single entry point with filtering options

### 2. Improved User Experience
- **Specialized Forms**: Only relevant fields for each item type
- **Auto-completion**: SKU generation and unit suggestions
- **Visual Distinction**: Different colors and icons for each type
- **Quick Navigation**: Direct links to specific item types

### 3. Better Data Management
- **Structured Data**: Clear distinction between asset and non-asset data
- **Inventory Tracking**: Minimum stock levels for non-assets
- **Technical Specs**: Detailed specifications for assets
- **Flexible Schema**: Extensible for future item types

### 4. Enhanced Functionality
- **Advanced Filtering**: Filter by type, search across fields
- **Statistics**: Real-time counts and analytics
- **Pagination**: Handle large datasets efficiently
- **Export Ready**: Structured data for reporting

## Usage Guide

### Creating Asset Items
1. Navigate to `/inventory/asset/create/`
2. Fill basic information (SKU auto-generated)
3. Add technical specifications (optional)
4. Save as Asset item

### Creating Non-Asset Items
1. Navigate to `/inventory/non-asset/create/`
2. Fill basic information (SKU auto-generated with NA- prefix)
3. Set unit of measure (required)
4. Set minimum stock level (optional)
5. Save as Non-Asset item

### Viewing and Managing
- **All Items**: `/inventory/item/` - Unified view with filtering
- **Assets Only**: `/inventory/asset/` - Asset-specific view
- **Non-Assets Only**: `/inventory/non-asset/` - Non-asset specific view

## Migration Instructions

### Step 1: Run Migration
```bash
python manage.py migrate inventory 0011
```

### Step 2: Update Existing Data (Optional)
```python
# In Django shell
from inventory.models import Item

# Set existing items as assets (default behavior)
Item.objects.filter(item_type__isnull=True).update(item_type='asset')
```

### Step 3: Test Functionality
1. Create new asset items
2. Create new non-asset items
3. Test filtering and search
4. Verify form validations

## Future Enhancements

### Potential Additions
- **Stock Management**: Actual stock levels for non-assets
- **Maintenance Scheduling**: Enhanced for assets
- **Depreciation Tracking**: For asset items
- **Supplier Management**: Enhanced supplier relationships
- **Barcode Integration**: QR codes for both types

The refactoring provides a solid foundation for comprehensive inventory management with clear distinction between trackable assets and consumable non-assets.