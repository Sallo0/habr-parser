from entities import ArticleInfo, HubInfo


class ConsoleView:
    def __init__(self):
        self.separator = "-"
        self.separator_count = 46

    def display_hub(self, hub_info: HubInfo):
        print(self.separator * self.separator_count, "\n" * 4)
        print(f'{hub_info.name}'.center(46, ' '))
        print(f'{hub_info.url}'.center(46, ' '))
        print("\n" * 4, self.separator * self.separator_count)

    def display_article(self, article: ArticleInfo | None):
        if not article:
            return
        print('Название статьи:'.ljust(20), article.title)
        print('Автор:'.ljust(20), article.author_username)
        print('Дата публикации:'.ljust(20), article.pub_date)
        print('Ссылка на статью:'.ljust(20), article.article_url)
        print('Ссылка на автора:'.ljust(20), article.author_url)
        print(self.separator * self.separator_count)
