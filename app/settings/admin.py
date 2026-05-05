from django.contrib import admin
from .models import OurHistory, Settings, Dish, Statistic, HistoryFeature, News, Category, Testimonial, Gallery, ContactMessage, Reservation
from django.utils.html import format_html

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    # Ограничиваем создание, чтобы в базе всегда была только одна запись настроек
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class HistoryFeatureInline(admin.TabularInline):
    model = HistoryFeature
    extra = 3  # Количество пустых полей для новых особенностей по умолчанию
    fields = ('title', 'description', 'icon', 'display_icon')
    readonly_fields = ('display_icon',)

    def display_icon(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 24px; color: #b85c4b; width: 30px; text-align: center;"></i>', obj.icon)
        return "-"
    display_icon.short_description = 'Превью иконки'

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css',)
        }

@admin.register(OurHistory)
class OurHistoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [HistoryFeatureInline]

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'price', 'category', 'is_promotion', 'is_popular', 'is_new')
    list_filter = ('category', 'is_popular', 'is_new', 'is_promotion')
    search_fields = ('title',)
    list_editable = ('price', 'is_promotion', 'is_popular', 'is_new')

    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'description', 'price', 'image', 'is_popular', 'is_new')
        }),
        ('Настройки акции', {
            'fields': ('is_promotion', 'discount_price', 'promotion_end_date', 'new_until_date'),
            'description': 'Укажите цену по акции, если блюдо участвует в ней.'
        }),
    )

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.image.url)
        return "-"
    get_image.short_description = 'Фото'

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'display_icon')

    def display_icon(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 24px; color: #b85c4b; width: 30px; text-align: center;"></i>', obj.icon)
        return "-"
    display_icon.short_description = 'Превью'

    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css',)
        }

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published')
    list_filter = ('is_published', 'date')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'rating')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at')
    list_editable = ('status',)
    readonly_fields = ('name', 'phone', 'email', 'message', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('status', 'created_at')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'guests', 'status')
    list_editable = ('status',)
    list_filter = ('status', 'date', 'guests')