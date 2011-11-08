from django.contrib import admin

from osp.core import models

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'user__email',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'number', 'section', 'term', 'year', 'title',)
    list_filter = ('prefix', 'number', 'term', 'year',)
    search_fields = ('prefix', 'number', 'section', 'term', 'year', 'title',)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'section',)
    search_fields = ('student__username', 'student__first_name',
                     'student__last_name', 'student__email', 'section__prefix',
                     'section__number', 'section__section', 'section__term',
                     'section__year', 'section__title',)


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Enrollment, EnrollmentAdmin)
