# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import replace_image as module_to_test
from simpil import SimpilImage

logging = logging_helper.setup_logging()


response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://images.metadata.sky.com/pd-image/e6c1b884-5802-4efe-a669-eee522bd3b99/16-9/456?sid=4075',
                               filter=u'pd-image',
                               params=u'http://static.skyq-b.interactive.sky.com/config-published-content/apps/media/ad0c5f7723d6e80c9885aec2c062072e/hero.jpg')

image = SimpilImage(response.content)
image.save('temp.png')