# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from os import path


class BooksToScrapePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'bookname': item.get('book_name')}) for x in item.get(self.images_urls_field, [])]
    def file_path(self, request, response=None, info=None):
        # ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # # detect if file_key() or image_key() methods have been overridden
        # if not hasattr(self.file_key, '_base'):
        #     _warn()
        #     return self.file_key(url)
        # elif not hasattr(self.image_key, '_base'):
        #     _warn()
        #     return self.image_key(url)
        ## end of deprecation warning block
        filename = request.meta['bookname'].replace(':', '')
        return 'full/%s.jpg' % (filename)
