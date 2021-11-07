
import json as js

from twisted.web import server, resource
from twisted.internet import reactor, endpoints

from stats.operations import MainOperation
from stats.stats import Stats


def main():
    # stats = Stats()
    # response = stats.main()
    # operations = MainOperation(response)
    # operations.main()
    pass

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader(b"content-type", b"application/json")
        content = js.dumps({
            'req': self.numberRequests
        })

        return content.encode("utf-8")


if __name__ == '__main__':
    endpoints.serverFromString(
        reactor, "tcp:8080"
    ).listen(server.Site(Counter()))
    reactor.run()
