from django.contrib import admin


from .models import Property, MyProperty, PropertyRating
from .models import Images, Category, City, Neighborhood, CityImage , NeighborhoodImage


# Register your models here.


class PropertyImageInline(admin.TabularInline):
    model = Images
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [ PropertyImageInline, ]
    list_display = ["__str__","realtor","title","price"]
    search_fields = ["title", "description"]
    class Meta:
        model = Property

class CityImageInline(admin.TabularInline):
    model = CityImage
    extra = 1

class CityAdmin(admin.ModelAdmin):
    inlines = [ CityImageInline, ]
    list_display = ["__str__",]
    class Meta:
        model = City

class NeighborhoodImageInline(admin.TabularInline):
    model = NeighborhoodImage
    extra = 1

class NeighborhoodAdmin(admin.ModelAdmin):
    inlines = [ NeighborhoodImageInline, ]
    list_display = ["__str__","city",]
    class Meta:
        model = Neighborhood


admin.site.register(Property, PropertyAdmin)
admin.site.register(MyProperty)
admin.site.register(PropertyRating)
admin.site.register(Category)
admin.site.register(City, CityAdmin )
admin.site.register(Neighborhood, NeighborhoodAdmin)