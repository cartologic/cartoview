up:
	# bring up the services
	docker-compose up -d

sync: up
	# set up the database tablea
	docker-compose exec cartoview python manage.py migrate
	docker-compose exec cartoview python manage.py loaddata sample_admin.json
	docker-compose exec cartoview python manage.py loaddata default_oauth_apps.json
	docker-compose exec cartoview python manage.py loaddata app_stores.json
	docker-compose exec cartoview python manage.py loaddata initial_data.json


prepare_manager: up
        #make migration for app_manager
	docker-compose exec cartoview python manage.py makemigrations app_manager
migrate_account: up
	docker-compose exec cartoview python manage.py migrate account
migrate:
	docker-compose exec cartoview python manage.py migrate --noinput
wait:
	sleep 5
logs:
	docker-compose logs --follow
logs_tail:
	docker-compose logs --follow --tail 100
logs_tail_cartoview:
	docker-compose logs --follow --tail 100 cartoview
logs_tail_geoserver:
	docker-compose logs --follow --tail 100 geoserver
down:
	docker-compose down
bower:
	docker-compose exec cartoview bower install --allow-root
reset: down up wait sync

collect_static: up
	docker-compose exec cartoview python manage.py collectstatic --noinput
run: up wait prepare_manager sync bower collect_static

static_db: up sync wait bower collect_static

update:
	docker-compose exec cartoview pip install cartoview --no-cache-dir -U
	docker-compose restart cartoview
new_app: collect_static
	docker-compose restart cartoview
