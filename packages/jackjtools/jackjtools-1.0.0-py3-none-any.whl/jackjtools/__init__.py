from . import web

class web2(web.web):
    def get_url(self):
        r = self.get_web_url()
        return r