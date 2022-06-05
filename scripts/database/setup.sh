#!/usr/bin/env bash

set -x
psql -U postgres -c "drop database template_postgis"
psql -U postgres -c "drop database cartoview"
psql -U postgres -c "drop database cartoview_data"
psql -U postgres -c "drop database upload_test"
psql -U postgres -c "drop database test_upload_test"
psql -U postgres -c "drop user cartoview"
psql -U postgres -c "create user cartoview CREATEDB SUPERUSER"
psql -U postgres -c "ALTER USER cartoview WITH PASSWORD 'cartoview';"
psql -U postgres -c "create database template_postgis"
psql -U postgres -d template_postgis -c 'CREATE EXTENSION postgis;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cartoview;'
psql -U postgres -c "create database cartoview OWNER cartoview TEMPLATE template_postgis"
psql -U postgres -c "create database cartoview_data OWNER cartoview TEMPLATE template_postgis"