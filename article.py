from scrapy.item import Item,Field

class ArticleItem(Item):
    publisher = Field()
    oriId = Field()
    url = Field()
    content = Field()