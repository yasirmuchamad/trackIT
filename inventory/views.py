import openpyxl
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models import Count, Q
from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.forms import CategoryForm, ItemForm, AssetItemForm, NonAssetItemForm, ItemUnitForm, TransactionForm, TransactionInForm, TransactionOutForm, TransactionReturnForm
from inventory.models import Category, Item, ItemUnit, Transaction
from openpyxl.styles import Font, Alignment


##########################################################  Dashboard View
class InventoryDashboardView(TemplateView):
    template_name = "inventory/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inventory Dashboard'
        
        # Basic counts
        context['total_categories'] = Category.objects.count()
        context['total_items'] = Item.objects.count()
        context['total_item_units'] = ItemUnit.objects.count()
        
        # Item Unit statistics by status
        status_stats = ItemUnit.objects.values('status').annotate(count=Count('id'))
        context['status_stats'] = {stat['status']: stat['count'] for stat in status_stats}
        
        # Item Unit statistics by condition
        condition_stats = ItemUnit.objects.values('condition').annotate(count=Count('id'))
        context['condition_stats'] = {stat['condition']: stat['count'] for stat in condition_stats}
        
        # Recent items (last 10)
        context['recent_items'] = Item.objects.order_by('-entry_date')[:10]
        
        # Items needing maintenance
        context['maintenance_needed'] = ItemUnit.objects.filter(
            Q(status='maintenance') | Q(condition='poor') | Q(condition='damaged')
        ).select_related('item', 'location', 'current_user')[:10]
        
        # Available items (can be assigned)
        context['available_items'] = ItemUnit.objects.filter(
            status='in_warehouse',
            condition__in=['excellent', 'good', 'fair']
        ).select_related('item', 'location')[:10]
        
        # Items currently in use
        context['items_in_use'] = ItemUnit.objects.filter(
            status='in_use'
        ).select_related('item', 'current_user')[:10]
        
        # Category distribution
        category_stats = Item.objects.values('category__name').annotate(count=Count('id'))
        context['category_stats'] = {stat['category__name']: stat['count'] for stat in category_stats}
        
        return context


##########################################################  views for category
class CategoryListView(ListView):
    model = Category
    template_name = "inventory/category/list.html"

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="List Category"
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/create.html"
    success_url = reverse_lazy('inventory:list_category')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Create Category"
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "inventory/category/create.html"
    success_url = reverse_lazy('inventory:list_category')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Update Category"
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "inventory/category/delete.html"
    success_url = reverse_lazy('inventory:list_category')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(self.request, f"Category '{category.name}' berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
                                                    
def categoryToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Category"

    # Judul besar di baris 1
    ws.merge_cells('A1:B1')  # gabungkan dari kolom A sampai B
    ws['A1'] = "List Category"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Name']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Category.objects.all(), start=1):
        ws.append([
            idx,
            s.name,
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=category.xlsx'
    wb.save(response)
    return response


##########################################################  views for item


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/create.html"
    success_url = reverse_lazy('inventory:list_item')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Create Item"
        return context


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "inventory/item/create.html"
    success_url = reverse_lazy('inventory:list_item')

    def get_context_data(self, **kwrags):
        context = super().get_context_data(**kwrags)
        context['title']="Update Item"
        return context


class ItemDeleteView(DeleteView):
    model = Item
    template_name = "inventory/item/delete.html"
    success_url = reverse_lazy('inventory:list_item')

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        messages.success(self.request, f"Item '{item.name}' berhasil dihapus.")
        return super().delete(request, *args, **kwargs)


##########################################################  Asset Item Views
class AssetItemListView(ListView):
    model = Item
    template_name = "inventory/item/asset_list.html"
    context_object_name = 'items'

    def get_queryset(self):
        try:
            return Item.objects.filter(item_type='asset').select_related('category')
        except Exception:
            # Fallback if item_type column doesn't exist yet
            return Item.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List Asset Items"
        context['item_type'] = 'asset'
        
        try:
            # Check if migration is needed
            Item.objects.filter(item_type='asset').count()
        except Exception:
            context['migration_needed'] = True
            
        return context


class AssetItemCreateView(CreateView):
    model = Item
    form_class = AssetItemForm
    template_name = "inventory/item/asset_create.html"
    success_url = reverse_lazy('inventory:list_asset_item')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create Asset Item"
        context['item_type'] = 'asset'
        
        try:
            # Check if migration is needed
            Item.objects.filter(item_type='asset').count()
        except Exception:
            context['migration_needed'] = True
            
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Asset item '{form.instance.name}' berhasil dibuat.")
        return super().form_valid(form)


class AssetItemUpdateView(UpdateView):
    model = Item
    form_class = AssetItemForm
    template_name = "inventory/item/asset_create.html"
    success_url = reverse_lazy('inventory:list_asset_item')

    def get_queryset(self):
        try:
            return Item.objects.filter(item_type='asset')
        except Exception:
            return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Asset Item"
        context['item_type'] = 'asset'
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Asset item '{form.instance.name}' berhasil diperbarui.")
        return super().form_valid(form)


##########################################################  Non-Asset Item Views
class NonAssetItemListView(ListView):
    model = Item
    template_name = "inventory/item/non_asset_list.html"
    context_object_name = 'items'

    def get_queryset(self):
        try:
            return Item.objects.filter(item_type='non_asset').select_related('category')
        except Exception:
            # Fallback if item_type column doesn't exist yet
            return Item.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List Non-Asset Items"
        context['item_type'] = 'non_asset'
        
        try:
            # Check if migration is needed
            Item.objects.filter(item_type='non_asset').count()
        except Exception:
            context['migration_needed'] = True
            
        return context


class NonAssetItemCreateView(CreateView):
    model = Item
    form_class = NonAssetItemForm
    template_name = "inventory/item/non_asset_create.html"
    success_url = reverse_lazy('inventory:list_non_asset_item')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create Non-Asset Item"
        context['item_type'] = 'non_asset'
        
        try:
            # Check if migration is needed
            Item.objects.filter(item_type='non_asset').count()
        except Exception:
            context['migration_needed'] = True
            
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Non-asset item '{form.instance.name}' berhasil dibuat.")
        return super().form_valid(form)


class NonAssetItemUpdateView(UpdateView):
    model = Item
    form_class = NonAssetItemForm
    template_name = "inventory/item/non_asset_create.html"
    success_url = reverse_lazy('inventory:list_non_asset_item')

    def get_queryset(self):
        try:
            return Item.objects.filter(item_type='non_asset')
        except Exception:
            return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Non-Asset Item"
        context['item_type'] = 'non_asset'
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Non-asset item '{form.instance.name}' berhasil diperbarui.")
        return super().form_valid(form)


##########################################################  Enhanced Item List View
class ItemListView(ListView):
    model = Item
    template_name = "inventory/item/list.html"
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        # Test if item_type column exists by trying a simple query
        try:
            # Test query to check if item_type field exists
            Item.objects.filter(item_type='asset').exists()
            migration_needed = False
        except Exception:
            migration_needed = True
        
        # Store migration status for use in context
        self._migration_needed = migration_needed
        
        if not migration_needed:
            # Full functionality with item_type filtering
            queryset = Item.objects.select_related('category').order_by('-entry_date')
            
            # Filter by item type if specified
            item_type = self.request.GET.get('type')
            if item_type in ['asset', 'non_asset']:
                queryset = queryset.filter(item_type=item_type)
            
            # Search functionality
            search = self.request.GET.get('search')
            if search:
                queryset = queryset.filter(
                    models.Q(name__icontains=search) |
                    models.Q(sku_code__icontains=search) |
                    models.Q(brand__icontains=search) |
                    models.Q(model__icontains=search)
                )
            
            return queryset
        else:
            # Fallback mode - basic functionality only
            queryset = Item.objects.select_related('category').order_by('-entry_date')
            
            # Search functionality (without item_type filtering)
            search = self.request.GET.get('search')
            if search:
                queryset = queryset.filter(
                    models.Q(name__icontains=search) |
                    models.Q(sku_code__icontains=search) |
                    models.Q(brand__icontains=search) |
                    models.Q(model__icontains=search)
                )
            
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "List All Items"
        
        # Use stored migration status
        migration_needed = getattr(self, '_migration_needed', True)
        context['migration_needed'] = migration_needed
        
        if not migration_needed:
            # Try to get counts with item_type (if column exists)
            try:
                context['asset_count'] = Item.objects.filter(item_type='asset').count()
                context['non_asset_count'] = Item.objects.filter(item_type='non_asset').count()
            except Exception:
                context['asset_count'] = 0
                context['non_asset_count'] = 0
                context['migration_needed'] = True
        else:
            # Fallback counts
            context['asset_count'] = 0
            context['non_asset_count'] = 0
        
        context['current_filter'] = self.request.GET.get('type', 'all')
        context['search_query'] = self.request.GET.get('search', '')
        return context
                                                    
def itemToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Item"

    # Judul besar di baris 1
    ws.merge_cells('A1:L1')  # gabungkan dari kolom A sampai L
    ws['A1'] = "List Item"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'SKU', 'Category', 'Name', 'Brand', 'Model', 'CPU', 'RAM', 'Storage', 'Display', 'OS', 'Entry Date']
    ws.append(headers)

    # Data
    for idx, s in enumerate(Item.objects.all(), start=1):
        ws.append([
            idx,
            s.sku_code,
            str(s.category) if s.category else '',
            s.name,
            s.brand,
            s.model,
            s.cpu,
            s.ram,
            s.storage,
            s.display,
            s.os,
            s.entry_date.replace(tzinfo=None) if s.entry_date else ''
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=items.xlsx'
    wb.save(response)
    return response


##########################################################  views for item unit
class ItemUnitListView(ListView):
    model = ItemUnit
    template_name = "inventory/item_unit/list.html"
    context_object_name = 'item_units'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Device'
        return context

    def get_queryset(self):
        """Optimize queries with select_related"""
        return ItemUnit.objects.select_related(
            'item', 'item__category', 'location', 'location__area', 'current_user'
        ).order_by('asset_number')


class ItemUnitCreateView(CreateView):
    model = ItemUnit
    form_class = ItemUnitForm
    template_name = "inventory/item_unit/create.html"
    success_url = reverse_lazy('inventory:list_item_unit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add New Device"
        return context


class ItemUnitUpdateView(UpdateView):
    model = ItemUnit
    form_class = ItemUnitForm
    template_name = "inventory/item_unit/create.html"
    success_url = reverse_lazy('inventory:list_item_unit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Update Device"
        return context


class ItemUnitDeleteView(DeleteView):
    model = ItemUnit
    template_name = "inventory/item_unit/delete.html"
    success_url = reverse_lazy('inventory:list_item_unit')

    def delete(self, request, *args, **kwargs):
        item_unit = self.get_object()
        messages.success(self.request, f"Device '{item_unit.asset_number}' berhasil dihapus.")
        return super().delete(request, *args, **kwargs)
                                                    
def itemunitToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List Device"

    # Judul besar di baris 1
    ws.merge_cells('A1:I1')  # gabungkan dari kolom A sampai I
    ws['A1'] = "List Device"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = ['Id', 'Asset Number', 'Item', 'Serial Number', 'Location', 'IP Address', 'Status', 'Condition', 'Current User']
    ws.append(headers)

    # Data
    for idx, s in enumerate(ItemUnit.objects.select_related('item', 'location', 'current_user'), start=1):
        ws.append([
            idx,
            s.asset_number,
            s.item.name,
            s.serial_number,
            str(s.location),
            s.ip_address,
            s.get_status_display(),
            s.get_condition_display(),
            str(s.current_user) if s.current_user else 'Unassigned',
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=devices.xlsx'
    wb.save(response)
    return response


##########################################################  views for transactions
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "inventory/transaction/list.html"
    context_object_name = 'transactions'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Transaksi'
        
        try:
            # Add statistics
            context['pending_count'] = Transaction.objects.filter(status='pending').count()
            context['completed_count'] = Transaction.objects.filter(status='completed').count()
            context['in_count'] = Transaction.objects.filter(transaction_type='in').count()
            context['out_count'] = Transaction.objects.filter(transaction_type='out').count()
        except Exception:
            # Handle case when Transaction table doesn't exist yet
            context['pending_count'] = 0
            context['completed_count'] = 0
            context['in_count'] = 0
            context['out_count'] = 0
        
        return context

    def get_queryset(self):
        """Optimize queries with select_related"""
        try:
            return Transaction.objects.select_related(
                'item_unit', 'item_unit__item', 'item', 'from_location', 'to_location',
                'from_employee', 'to_employee', 'requested_by', 'approved_by'
            ).order_by('-transaction_date')
        except Exception:
            # Return empty queryset if table doesn't exist
            return Transaction.objects.none()


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "inventory/transaction/create.html"
    success_url = reverse_lazy('inventory:list_transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Buat Transaksi Baru"
        return context

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        messages.success(self.request, 'Transaksi berhasil dibuat dan menunggu persetujuan.')
        return super().form_valid(form)


class TransactionInCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionInForm
    template_name = "inventory/transaction/create_in.html"
    success_url = reverse_lazy('inventory:list_transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Barang Masuk"
        return context

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        form.instance.transaction_type = 'in'
        messages.success(self.request, 'Transaksi barang masuk berhasil dibuat.')
        return super().form_valid(form)


class TransactionOutCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionOutForm
    template_name = "inventory/transaction/create_out.html"
    success_url = reverse_lazy('inventory:list_transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Barang Keluar"
        return context

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        form.instance.transaction_type = 'out'
        messages.success(self.request, 'Transaksi barang keluar berhasil dibuat.')
        return super().form_valid(form)


class TransactionReturnCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionReturnForm
    template_name = "inventory/transaction/create_return.html"
    success_url = reverse_lazy('inventory:list_transaction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Pengembalian Barang"
        return context

    def form_valid(self, form):
        form.instance.requested_by = self.request.user
        form.instance.transaction_type = 'return'
        messages.success(self.request, 'Transaksi pengembalian berhasil dibuat.')
        return super().form_valid(form)


class TransactionDetailView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/transaction/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_id = kwargs.get('pk')
        transaction = Transaction.objects.select_related(
            'item_unit', 'item_unit__item', 'item', 'from_location', 'to_location',
            'from_employee', 'to_employee', 'requested_by', 'approved_by'
        ).get(id=transaction_id)
        
        context['transaction'] = transaction
        context['title'] = f'Detail Transaksi {transaction.transaction_number}'
        return context


def approve_transaction(request, pk):
    """Approve a transaction"""
    if not request.user.is_staff:
        messages.error(request, 'Anda tidak memiliki izin untuk menyetujui transaksi.')
        return redirect('inventory:list_transaction')
    
    try:
        transaction = Transaction.objects.get(pk=pk)
        if transaction.status == 'pending':
            transaction.approve(request.user)
            messages.success(request, f'Transaksi {transaction.transaction_number} berhasil disetujui dan dieksekusi.')
        else:
            messages.warning(request, 'Transaksi sudah diproses sebelumnya.')
    except Transaction.DoesNotExist:
        messages.error(request, 'Transaksi tidak ditemukan.')
    
    return redirect('inventory:transaction_detail', pk=pk)


def cancel_transaction(request, pk):
    """Cancel a transaction"""
    try:
        transaction = Transaction.objects.get(pk=pk)
        if transaction.status == 'pending':
            if transaction.requested_by == request.user or request.user.is_staff:
                transaction.status = 'cancelled'
                transaction.save()
                messages.success(request, f'Transaksi {transaction.transaction_number} berhasil dibatalkan.')
            else:
                messages.error(request, 'Anda tidak memiliki izin untuk membatalkan transaksi ini.')
        else:
            messages.warning(request, 'Transaksi tidak dapat dibatalkan.')
    except Transaction.DoesNotExist:
        messages.error(request, 'Transaksi tidak ditemukan.')
    
    return redirect('inventory:transaction_detail', pk=pk)


def transactionToExcel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Daftar Transaksi"

    # Judul besar di baris 1
    ws.merge_cells('A1:L1')
    ws['A1'] = "Daftar Transaksi Inventory"
    ws['A1'].font = Font(size=14, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Header
    headers = [
        'No. Transaksi', 'Jenis', 'Tanggal', 'Item', 'Asset Number', 
        'Dari Lokasi', 'Ke Lokasi', 'Dari Karyawan', 'Ke Karyawan', 
        'Alasan', 'Status', 'Dibuat Oleh'
    ]
    ws.append(headers)

    # Data
    for transaction in Transaction.objects.select_related(
        'item_unit', 'item_unit__item', 'item', 'from_location', 'to_location',
        'from_employee', 'to_employee', 'requested_by'
    ).order_by('-transaction_date'):
        
        # Determine item name and identifier
        if transaction.item_unit:
            item_name = transaction.item_unit.item.name
            item_identifier = transaction.item_unit.asset_number
        elif transaction.item:
            item_name = transaction.item.name
            item_identifier = f"Stock: {transaction.quantity}"
        else:
            item_name = "Unknown"
            item_identifier = "-"
        
        ws.append([
            transaction.transaction_number,
            transaction.get_transaction_type_display(),
            transaction.transaction_date.strftime('%d/%m/%Y %H:%M'),
            item_name,
            item_identifier,
            str(transaction.from_location) if transaction.from_location else '-',
            str(transaction.to_location) if transaction.to_location else '-',
            str(transaction.from_employee) if transaction.from_employee else '-',
            str(transaction.to_employee) if transaction.to_employee else '-',
            transaction.reason,
            transaction.get_status_display(),
            str(transaction.requested_by) if transaction.requested_by else '-',
        ])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transactions.xlsx'
    wb.save(response)
    return response