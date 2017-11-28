from django.views.generic import View
from django.http import HttpResponse

import json
import logging

__author__ = "Bifei Yang"


class BaseView(View):

    logger = logging.getLogger('View')

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return self.do_dispatch(*args, **kwargs)

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        if self.request.method == 'POST':
            return self.post()
        elif self.request.method == "GET":
            return self.get()

    @property
    def body(self):
        return json.loads(self.request.body.decode() or '{}')

    @property
    def query(self):
        d = getattr(self.request, self.request.method, None)
        if d:
            d = d.dict()
        else:
            d = dict()
        d.update(self.request.FILES)
        return d

    def check_input(self, *keys):
        for k in keys:
            if k not in self.input:
                raise Exception('Field "%s" required' % (k, ))

    def post(self):
        raise Exception('You should implement "post" method')

    def get(self):
        raise Exception('You should implement "get" method')
