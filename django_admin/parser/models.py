from django.db import models
import datetime

class AbstractModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Article(AbstractModel):
    title = models.CharField(blank=True, null=True)
    url = models.CharField(unique=True, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey('Author', related_name='articles', on_delete=models.CASCADE)
    hubs = models.ManyToManyField('Hub', through='ArticleHubAssociation')

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'article'


class Hub(AbstractModel):
    name = models.CharField(blank=True, null=True)
    url = models.CharField(unique=True, blank=True, null=True)
    update_information_period = models.IntegerField(blank=True, null=True, default=1,
                                                    verbose_name='Update information period (min)')
    last_update = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())

    articles = models.ManyToManyField(Article, through='ArticleHubAssociation')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'hub'


class ArticleHubAssociation(models.Model):
    article = models.ForeignKey(Article, models.DO_NOTHING, blank=True, null=True)
    hub = models.ForeignKey('Hub', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article_hub_association'


class Author(AbstractModel):
    url = models.CharField(unique=True, blank=True, null=True)
    username = models.CharField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = False
        db_table = 'author'
