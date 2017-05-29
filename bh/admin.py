from django.contrib import admin
from . import models

admin.site.site_header = 'Brotherhood: администрирование'


class PhoneInline(admin.TabularInline):
    model = models.Phone
    verbose_name_plural = 'Номера телефонов'
    extra = 0
    verbose_name = 'Телефон'


class EmailInline(admin.TabularInline):
    model = models.Email
    verbose_name_plural = 'Адреса электронной почты'
    extra = 0
    verbose_name = ''


class SocialInline(admin.TabularInline):
    model = models.Social
    verbose_name_plural = 'Социальные сети'
    extra = 0
    verbose_name = ''


class RelationInline(admin.TabularInline):
    model = models.Relation
    fk_name = 'person'
    verbose_name_plural = 'Родственные связи'
    verbose_name = ''
    extra = 0


class ActionRoleInline(admin.TabularInline):
    model = models.ActionRole
    extra = 0
    verbose_name = 'Активность'
    verbose_name_plural = 'Активности'


class PersonAdmin(admin.ModelAdmin):
    inlines = [
        EmailInline, SocialInline, PhoneInline,
        RelationInline, ActionRoleInline
    ]
    search_fields = ['first_name', 'last_name', 'middle_name']
    list_filter = [
        'married', 'baptized', 'gender', 'member',
        'gone_to_eternity', 'gone_to_another_church', 'gone'
    ]

    actions = ['set_baptized', 'set_married', 'set_member']

    def set_baptized(self, request, queryset):
        queryset.update(baptized=True)
        self.message_user(request, 'Помечены как "Крещен"')
    set_baptized.short_description = 'Пометить как "Крещен"'

    def set_married(self, request, queryset):
        queryset.update(married=True)
        self.message_user(request, 'Помечены как "Женат/замужем"')
    set_married.short_description = 'Пометить как "Женат/замужем"'

    def set_member(self, request, queryset):
        queryset.update(member=True)
        self.message_user(request, 'Помечены как "Член церкви"')
    set_member.short_description = 'Пометить как "Член церкви"'


class AddressInline(admin.TabularInline):
    model = models.Address


class RolesInline(admin.TabularInline):
    model = models.ActionRole
    verbose_name = 'Роль'
    verbose_name_plural = 'Роли'
    extra = 0


class ActionAdmin(admin.ModelAdmin):
    inlines = [
        RolesInline
    ]
    search_fields = ['name']


class EventAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'event_type', 'started_at', 'finished_at')


class AddressAdmin(admin.ModelAdmin):
    search_fields = ['text']


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('dow', 'time_from', 'time_to')

    def has_change_permission(self, request, obj=None):
        # Disable delete period ability
        if obj is not None:
            return False
        return super(PeriodAdmin, self).has_change_permission(request, obj=obj)


class PhoneAdmin(admin.ModelAdmin):
    search_fields = ['number']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    readonly_fields = ('image_tag',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.ActionType)
admin.site.register(models.Phone, PhoneAdmin)
admin.site.register(models.Skill)
admin.site.register(models.Period, PeriodAdmin)
admin.site.register(models.EventType)
admin.site.register(models.Gallery)
admin.site.register(models.Staff)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Photo, PhotoAdmin)
