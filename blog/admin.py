from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin

from blog.models import PublishedPost, Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    fields = "user", "body", "created_at"
    readonly_fields = "user", "body", "created_at"
    extra = 0


class PostAdmin(ExportMixin, admin.ModelAdmin):
    fieldsets = (
        (_('Title'), {'fields': ('title', 'slug')}),
        (_('Author'), {'fields': ('author',)}),
        (_('Body'), {'fields': ('body',)}),
        (_('Statics'), {'fields': ('liked_by',)}),  # TODO: add points, comment count,
        (_('Important dates'), {'fields': ('created_at', 'updated_at',)}),
    )
    readonly_fields = 'created_at', 'updated_at', 'liked_by',
    inlines = [CommentInline]
    list_display = "title", "author", "is_published", "created_at"

    def make_published(modeladmin, request, queryset):
        queryset.update(is_published=True)
        posts = list(queryset.values_list("id", flat=True))
        messages.info(request, "Posts %s are now published!" % posts)

    make_published.short_description = "Mark selected posts as published"
    actions = ['make_published']


admin.site.register(Post, PostAdmin)
admin.site.register(PublishedPost, PostAdmin)
