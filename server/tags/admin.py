from django.contrib import admin
from .models import Bag, Tag, Entry, Profile, Antenna


class TagAdmin(admin.ModelAdmin):
    list_display = ["tag_id", "in_stock"]
    list_filter = ["is_taken"]
    search_fields = []
    list_per_page = 10
    
    def in_stock(self, instance):
        return not instance.is_taken
    
    
    in_stock.boolean = True
    

class EntryAdmin(admin.ModelAdmin):
    list_display =["user", "bag", "registered_at", "total_tags", "taken"]
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.related_model == Tag:
    #         kwargs["queryset"] = db_field.related_model.objects.filter(is_taken=False)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

class BagAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_user', 'is_closed', 'total_tags', 'total_missing_tags', 'missing_tags']
    
    def missing_tags(self, instance):
        return ', '.join([x.tag_id for x in instance.missing_tags])

admin.site.register(Bag, BagAdmin)
admin.site.register(Profile)
admin.site.register(Antenna)
admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)
