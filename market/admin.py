# market/admin.py
from django.contrib import admin
from .models import MarketData, Category, HistoricalMarketData, Alert

class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'quantity', 'vendor_details', 'category', 'created_by', 'created_at')
    list_filter = ('category', 'created_at', 'tags')
    search_fields = ('product_name', 'vendor_details', 'tags__name')
    raw_id_fields = ('created_by',)
    autocomplete_fields = ['tags']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class HistoricalMarketDataAdmin(admin.ModelAdmin):
    list_display = ('market_data', 'price', 'date')
    list_filter = ('date',)
    search_fields = ('market_data__product_name',)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'market_data', 'condition', 'notified')
    list_filter = ('notified',)
    search_fields = ('user__username', 'market_data__product_name')

admin.site.register(MarketData, MarketDataAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(HistoricalMarketData, HistoricalMarketDataAdmin)
admin.site.register(Alert, AlertAdmin)
