from django.contrib import admin

from .models import Category, Location, Post, Comment


class PostInline(admin.StackedInline):
    model = Post


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'category',
        'location',
        'pub_date',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
        'slug',
        'description',
    )
    search_fields = ('title',)
    list_filter = ('slug',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'created_at',
        'author',
    )
    list_editable = (
        'text',
    )
    search_fields = ('text',)


admin.site.empty_value_display = '-не задано-'
