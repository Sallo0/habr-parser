from django.contrib import admin

from .models import Article, ArticleHubAssociation, Author, Hub


class ArticleHubAssociationInline(admin.TabularInline):
    model = ArticleHubAssociation
    extra = 0


class ArticleInline(admin.TabularInline):
    readonly_fields = ["url", "pub_date"]
    exclude = ["title", "text"]
    model = Article
    extra = 0


@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "last_update", "update_information_period")
    inlines = (ArticleHubAssociationInline,)



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("username", "url")

    inlines = [ArticleInline]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "author", "pub_date")
    inlines = (ArticleHubAssociationInline,)
