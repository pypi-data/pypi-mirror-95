from collections import OrderedDict
from functools import cached_property, partial
import json
from pathlib import Path
import re

import jsonschema
from .exceptions import InvalidDoc
from .utils import yaml_loads


def validate_openapi(doc):
    schema_file = Path(__file__).absolute().parent.joinpath(
        'openapi_v3_schema.json')
    with open(schema_file) as f:
        v3_schema = json.load(f)
    return jsonschema.validate(doc, v3_schema)


# /pets/(?P<pet_name>[a-z]+)
_re_path_pattern = re.compile(r'\(\?P%\((.+?)\)s[^/$]+')
# /pets/<slug:pet_id>
_slug_path_pattern = re.compile(r'%\((.+?)\)s')
_duplicate_slash_pattern = re.compile(r'/{1,}')


def get_re_parameter(match, parameters=None):
    assert parameters is not None
    parameters[match.group(1)] = {
        'in': 'path',
        'name': match.group(1),
        'schema': {
            'type': 'string',
        },
        'required': True,
    }
    return '{' + match.group(1) + '}'


def get_slug_parameter(match, parameters=None):
    assert parameters is not None
    parameters[match.group(1)] = {
        'in': 'path',
        'name': match.group(1),
        'schema': {
            'type': 'string',
        },
        'required': True,
    }
    return '{' + match.group(1) + '}'


def get_path_parameters(url_pattern):
    parameters = {}
    url_pattern = _re_path_pattern.sub(
        partial(get_re_parameter, parameters=parameters),
        url_pattern,
    )
    url_pattern = _slug_path_pattern.sub(
        partial(get_slug_parameter, parameters=parameters),
        url_pattern,
    )
    url_pattern = url_pattern.lstrip('^/').rstrip('$')
    url_pattern = _duplicate_slash_pattern.sub('/', url_pattern)
    return '/' + url_pattern, parameters


class OPENAPI:
    DEFAULT_OPENAPI_VERSION_DOC = 'openapi: 3.0.0'
    DEFAULT_OPENAPI_INFO_DOC = '''
    title: Awesome API
    description: this is auto generated doc by xxx
    version: 1.0.0
    '''
    DEFAULT_OPENAPI_ENDPOINT_DOC = '''
    summary: undocumented
    responses:
      200:
        description: ok
    '''
    HTTP_METHODS = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
    OPENAPI_KEY_LIST = [
        'info',
        'externalDocs',
        'servers',
        'tags',
        'paths',
        'security',
        'components',
    ]

    def __init__(self):
        self._doc_dict = OrderedDict()
        self.initialize()

    def as_dict(self):
        return self._doc_dict

    def _update_doc(self, value, key=None):
        """value can be doc string or dict object
        """
        if isinstance(value, str):
            value = yaml_loads(value)
        if not value:
            return
        if key:
            if key in self._doc_dict and isinstance(self._doc_dict[key], dict):
                self._doc_dict[key].update(**value)
            else:
                self._doc_dict[key] = value
        else:
            self._doc_dict.update(**value)

    def initialize(self):
        self._update_doc(self.DEFAULT_OPENAPI_VERSION_DOC)
        self._update_doc(self.DEFAULT_OPENAPI_INFO_DOC, key='info')

        self._update_doc(self.get_version_doc())
        for key in self.OPENAPI_KEY_LIST:
            func_to_get_doc = getattr(self, f'get_{key.lower()}_doc')
            self._update_doc(func_to_get_doc(), key)

    def from_obj(self, obj, prefix='OPENAPI'):
        self._update_doc(getattr(obj, f'{prefix}_VERSION', None))
        for key in self.OPENAPI_KEY_LIST:
            key_str = f'{prefix}_{key.upper()}'
            self._update_doc(getattr(obj, key_str, None), key)

    def get_version_doc(self):
        return self.DEFAULT_OPENAPI_VERSION_DOC

    def get_info_doc(self):
        return self.DEFAULT_OPENAPI_INFO_DOC

    def get_servers_doc(self):
        return ''

    def get_tags_doc(self):
        return ''

    def get_paths_doc(self):
        return ''

    def get_components_doc(self):
        return ''

    def get_security_doc(self):
        return ''

    def get_externaldocs_doc(self):
        return ''

    def get_path_doc(self, path_view):
        dct = {}
        for method in self.HTTP_METHODS:
            endpoint_func = getattr(path_view, method.lower())
            if not endpoint_func:
                continue
            dct[method] = self.get_endpoint_doc(endpoint_func)

    def load_api_doc_from_doc_string(self, pyobj, default=None):
        if default is None:
            default = {}
        doc_string = pyobj.__doc__ or ''
        split_by = '--api-doc--'
        doc_string = doc_string.split(split_by, 1)[-1]
        doc = yaml_loads(doc_string)
        if not isinstance(doc, dict) or not dict:
            doc = default
        return doc

    def get_default_endpoint_doc(self):
        return yaml_loads(self.DEFAULT_OPENAPI_ENDPOINT_DOC)

    @staticmethod
    def get_path_parameters_doc(url_pattern):
        return get_path_parameters(url_pattern)

    def get_endpoint_doc(self, endpoint_func):
        return self.load_api_doc_from_doc_string(
            endpoint_func,
            default=self.get_default_endpoint_doc(),
        )

    def validate(self):
        try:
            doc_dct = json.loads(json.dumps(self.as_dict()))
            return validate_openapi(doc_dct)
        except (jsonschema.SchemaError,
                jsonschema.exceptions.ValidationError) as exc:
            raise InvalidDoc(exc)
