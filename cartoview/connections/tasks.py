from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from cartoview.log_handler import get_logger
from django.db.models import Q
logger = get_logger(__name__)


@shared_task(bind=True)
def harvest_task(self, server_id):
    from cartoview.connections.models import Server
    try:
        server = Server.objects.get(id=server_id)
        server.handler.harvest()
    except ObjectDoesNotExist as e:
        logger.error(str(e))


@shared_task(bind=True)
def update_server_resources(self, server_id):
    from cartoview.connections.models import Server
    from cartoview.layers.models import Layer
    try:
        server = Server.objects.get(id=server_id)
        ld_list = server.handler.get_layers()
        for l in ld_list:
            name = l.get('name')
            layer = Layer.objects.get(server=server, name=name)
            for k, v in l.items():
                setattr(layer, k, v)
            layer.save()
    except ObjectDoesNotExist as e:
        logger.error(str(e))


@shared_task(bind=True)
def validate_server_resources(self, server_id):
    from cartoview.connections.models import Server
    try:
        server = Server.objects.get(id=server_id)
        ld_list = server.handler.get_layers()
        layer_names = [l.get('name') for l in ld_list]
        layers = server.layers.filter(~Q(name__in=layer_names))
        for layer in layers:
            layer.valid = False
            layer.save()
    except ObjectDoesNotExist as e:
        logger.error(str(e))


@shared_task(bind=True)
def validate_servers(self):
    from cartoview.connections.models import Server
    servers = Server.objects.all()
    for server in servers:
        validate_server_resources.delay(server_id=server.id)


@shared_task(bind=True)
def delete_invalid_resources(self, server_id):
    from cartoview.connections.models import Server
    try:
        server = Server.objects.get(id=server_id)
        invalid_layers = server.layers.filter(valid=False)
        invalid_layers.delete()
    except ObjectDoesNotExist as e:
        logger.error(str(e))
