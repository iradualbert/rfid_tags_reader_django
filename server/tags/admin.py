from django.contrib import admin
from .models import Tag, Entry

# Register your models here.
# class EntryInline(admin.TabularInline):
#     model = Entry
#     extra = 0

class TagAdmin(admin.ModelAdmin):
    # inlines = [EntryInline]
    list_display = ["tag_name", "in_stock", "available","last_time_taken", "recent_user"]
    list_filter = ["is_taken", "has_left", "recent_user"]
    search_fields = ["tag_name", "recent_user"]
    list_per_page = 10
    
    def in_stock(self, instance):
        return not instance.has_left

    def available(self, instance):
        return not instance.is_taken
    
    in_stock.boolean = True
    available.boolean = True
    

class EntryAdmin(admin.ModelAdmin):
    list_display =["tag", "user", "antenna", "registered_at", "left_at", "returned_at"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.related_model == Tag:
            kwargs["queryset"] = db_field.related_model.objects.filter(is_taken=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)