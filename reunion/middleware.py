import subprocess


class GitVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.version = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=format:"%s"'], stderr=subprocess.STDOUT
        ).decode("utf-8").split(" - ")

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        response.context_data["version"] = self.version[0][1:]
        return response
