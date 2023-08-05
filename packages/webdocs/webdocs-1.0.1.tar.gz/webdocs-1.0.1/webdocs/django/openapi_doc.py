from django.conf import settings
try:
    from django.core.urlresolvers import get_resolver
except ImportError:
    from django.urls import get_resolver
from webdocs.openapi_doc import OPENAPI


class DjangoOPENAPI(OPENAPI):
    def get_paths_doc(self):
        paths_doc = dict()
        resolver = get_resolver()
        for item in resolver.reverse_dict.items():
            url_path, path_doc = self.get_path_doc(*item)
            paths_doc[url_path] = path_doc
        return paths_doc

    def get_path_doc(self, view_func, url_pattern):
        path_doc = dict()
        url_path, path_parameters = url_pattern[0][0]

        # get path parameters
        url_path, default_path_parameters = \
                self.get_path_parameters_doc(url_path)
        _view_class_doc = self.load_api_doc_from_doc_string(
            view_func.view_class)
        path_parameters_doc = _view_class_doc.get('parameters', [])
        for parameter in path_parameters_doc:
            if parameter['in'] == 'path' and \
                    parameter['name'] in default_path_parameters:
                default_path_parameters.pop(parameter['name'])
        path_parameters_doc.extend(default_path_parameters.values())
        path_doc['parameters'] = path_parameters_doc

        # get endpoint doc
        for method in view_func.view_class.http_method_names:
            endpoint_func = getattr(view_func.view_class, method, None)
            if not endpoint_func or method.lower() == 'options':
                continue
            path_doc[method] = self.get_endpoint_doc(endpoint_func)
        return url_path, path_doc

    def from_settings(self):
        return self.from_obj(settings)
