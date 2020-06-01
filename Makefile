up:
	# bring up the services
	docker-compose up -d

sync: up
	# set up the database tablea
	docker-compose exec cartoview python manage.py migrate
	docker-compose exec cartoview python manage.py loaddata sample_admin.json
	docker-compose exec cartoview python manage.py loaddata default_oauth_apps_docker.json
	docker-compose exec cartoview python manage.py loaddata app_stores.json
	docker-compose exec cartoview python manage.py loaddata initial_data.json

backfill_api_keys:
	docker-compose exec cartoview python manage.py backfill_api_keys

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
reset: down up wait sync

collect_static: up
	docker-compose exec cartoview python manage.py collectstatic --noinput

prepare_oauth:
	docker-compose exec cartoview paver prepare_docker_oauth_fixture
	docker-compose exec cartoview paver install_docker_data_dir

run: up wait prepare_oauth prepare_manager sync collect_static backfill_api_keys

static_db: up sync wait collect_static

update:
	docker-compose exec cartoview pip install cartoview --no-cache-dir -U
	docker-compose restart cartoview
new_app: collect_static
	docker-compose restart cartoview
