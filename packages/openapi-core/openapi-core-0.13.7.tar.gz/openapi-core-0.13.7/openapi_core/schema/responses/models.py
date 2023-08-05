"""OpenAPI core responses models module"""
from openapi_core.schema.content.exceptions import MimeTypeNotFound
from openapi_core.schema.content.models import Content
from openapi_core.schema.media_types.exceptions import InvalidContentType


class Response(object):

    def __init__(
            self, http_status, description, headers=None, content=None,
            links=None, extensions=None):
        self.http_status = http_status
        self.description = description
        self.headers = headers and dict(headers) or {}
        self.content = content and Content(content) or Content()
        self.links = links and dict(links) or {}

        self.extensions = extensions and dict(extensions) or {}

    def __getitem__(self, mimetype):
        return self.get_content_type(mimetype)

    def get_content_type(self, mimetype):
        try:
            return self.content[mimetype]
        except MimeTypeNotFound:
            raise InvalidContentType(mimetype)
