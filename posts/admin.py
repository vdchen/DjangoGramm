from django.contrib import admin
from .models import Post, PostImage, Tag


# 1. PostImage Inline (allows uploading images directly when editing a Post)
class PostImageInline(admin.StackedInline):
    model = PostImage
    extra = 1  # Show 1 extra empty form by default for easy addition


# 2. Post Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Use the inline to include image uploads
    inlines = [PostImageInline]

    # Fields displayed in the list view
    list_display = ('author', 'caption_preview', 'created_at', 'total_likes')

    # Filter options in the sidebar
    list_filter = ('created_at', 'author')

    # Search fields
    search_fields = ('caption', 'author__username')

    # Add a custom method to show a short preview of the caption
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(
            obj.caption) > 50 else obj.caption

    caption_preview.short_description = 'Caption'


# 3. Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # Automatically populate the slug field from the name field
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')