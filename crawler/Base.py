from inspect import Traceback, trace
import re

import scrapy
import traceback
from xkafka import Producer
from crawler.common import invalid_links
from languageflow.data import Sentence
from languageflow.models.text_classifier import TextClassifier


class ArticleSpider(scrapy.Spider):
    visited = set()
    name = 'unknown'
    

    model_folder = "tmp/classification_svm_vntc"
    print(f"Load model from {model_folder}")
    classifer = TextClassifier.load(model_folder)
    print(f"Model is loaded.")


    def predict(self, text):
        sentence = Sentence(text)
        self.classifer.predict(sentence)
        labels = sentence.labels
        return labels[0]

    def doParse(self, resp):
        return None
    def parse(self, resp):
        try:
            pArticle = self.doParse(resp)
            if pArticle != None :
                # self.logger.info("ec")
                text = ' '.join(pArticle.paragraph)
                pArticle.category = self.predict(text)
                # self.logger.info(pArticle.category)
                Producer.notify('article', self.name.encode(), pArticle.SerializeToString())
                pass
        except Exception as e:
            print(traceback.format_exc())
            pass
        
        for next_page in resp.css('a'):
            if len(next_page.css('a::attr(href)').getall()) > 0:
                href = next_page.css('a::attr(href)').get()
                if href in invalid_links or 'javascript' in href or 'void' in href or 'jpg' in href or 'png' in href:
                    pass
                elif re.search("(mailto|tel)", href) is not None:
                    pass
                else:
                    if href in self.visited:
                        continue
                    self.visited.add(href)
                    yield resp.follow(href, self.parse)
        
