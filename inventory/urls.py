from django.urls import path
from .views import (
    InventoryDashboardView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, categoryToExcel,
    ItemListView, ItemCreateView, ItemUpdateView, ItemDeleteView, itemToExcel,
    AssetItemListView, AssetItemCreateView, AssetItemUpdateView,
    NonAssetItemListView, NonAssetItemCreateView, NonAssetItemUpdateView,
    ItemUnitListView, ItemUnitCreateView, ItemUnitUpdateView, ItemUnitDeleteView, itemunitToExcel,
    TransactionListView, TransactionCreateView, TransactionInCreateView, TransactionOutCreateView, 
    TransactionReturnCreateView, TransactionDetailView, approve_transaction, cancel_transaction, transactionToExcel
)

app_name = 'inventory'
urlpatterns = [
    # Dashboard
    path('', InventoryDashboardView.as_view(), name='dashboard'),
    
    # Category URLs
    path('category/', CategoryListView.as_view(), name='list_category'),
    path('category/create/', CategoryCreateView.as_view(), name='create_category'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='update_category'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('category/export/', categoryToExcel, name='category_to_excel'),

    # Item URLs
    path('item/', ItemListView.as_view(), name='list_item'),
    path('item/create/', ItemCreateView.as_view(), name='create_item'),
    path('item/update/<int:pk>/', ItemUpdateView.as_view(), name='update_item'),
    path('item/delete/<int:pk>/', ItemDeleteView.as_view(), name='delete_item'),
    path('item/export/', itemToExcel, name='item_to_excel'),

    # Asset Item URLs
    path('asset/', AssetItemListView.as_view(), name='list_asset_item'),
    path('asset/create/', AssetItemCreateView.as_view(), name='create_asset_item'),
    path('asset/update/<int:pk>/', AssetItemUpdateView.as_view(), name='update_asset_item'),

    # Non-Asset Item URLs
    path('non-asset/', NonAssetItemListView.as_view(), name='list_non_asset_item'),
    path('non-asset/create/', NonAssetItemCreateView.as_view(), name='create_non_asset_item'),
    path('non-asset/update/<int:pk>/', NonAssetItemUpdateView.as_view(), name='update_non_asset_item'),

    # Item Unit (Device) URLs
    path('item_unit/', ItemUnitListView.as_view(), name='list_item_unit'),
    path('item_unit/create/', ItemUnitCreateView.as_view(), name='create_item_unit'),
    path('item_unit/update/<int:pk>/', ItemUnitUpdateView.as_view(), name='update_item_unit'),
    path('item_unit/delete/<int:pk>/', ItemUnitDeleteView.as_view(), name='delete_item_unit'),
    path('item_unit/export/', itemunitToExcel, name='item_unit_to_excel'),
    
    # Transaction URLs
    path('transaction/', TransactionListView.as_view(), name='list_transaction'),
    path('transaction/create/', TransactionCreateView.as_view(), name='create_transaction'),
    path('transaction/in/', TransactionInCreateView.as_view(), name='create_transaction_in'),
    path('transaction/out/', TransactionOutCreateView.as_view(), name='create_transaction_out'),
    path('transaction/return/', TransactionReturnCreateView.as_view(), name='create_transaction_return'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transaction/<int:pk>/approve/', approve_transaction, name='approve_transaction'),
    path('transaction/<int:pk>/cancel/', cancel_transaction, name='cancel_transaction'),
    path('transaction/export/', transactionToExcel, name='transaction_to_excel'),
]
