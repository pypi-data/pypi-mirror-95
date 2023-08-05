from django.core.management import BaseCommand
from webdocs.django.openapi_doc import DjangoOPENAPI
from webdocs.exceptions import InvalidDoc
from webdocs.utils import yaml_dumps


class Command(BaseCommand):
    help = 'generate openapi doc from doc string'

    def add_arguments(self, parser):
        parser.add_argument('--output',
                            default='../docs/api.yaml',
                            help='where to save api doc')

    def handle(self, *args, **options):
        openapi_doc = DjangoOPENAPI()
        openapi_doc.from_settings()
        output = options['output']
        with open(output, 'wb') as f:
            dct = openapi_doc.as_dict()
            f.write(yaml_dumps(dct, encoding='utf-8', allow_unicode=True))
        try:
            openapi_doc.validate()
        except InvalidDoc:
            self.stderr.write(
                'Invalid doc. You can get detail in swagger editor')
