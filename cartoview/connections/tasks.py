from celery import shared_task


@shared_task(bind=True)
def harvest_task(self, server_id):
    from cartoview.connections.models import Server
    server = Server.objects.get(id=server_id)
    server.handler.harvest()
