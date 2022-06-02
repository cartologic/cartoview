#!/usr/bin/env bash

set -x
psql -U postgres -c "dropdb template_postgis"
psql -U postgres -c "dropdb cartoview"
psql -U postgres -c "dropdb cartoview_data"
psql -U postgres -c "dropdb upload_test"
psql -U postgres -c "dropdb test_upload_test"
psql -U postgres -c "dropuser cartoview"
psql -U postgres -c "createuser cartoview -d -s"
psql -U postgres -c "ALTER USER cartoview WITH PASSWORD 'cartoview';"
psql -U postgres -c "createdb template_postgis"
psql -U postgres -d template_postgis -c 'CREATE EXTENSION postgis;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cartoview;'
psql -U postgres -c "createdb -O cartoview cartoview"
psql -U postgres -c "createdb -T template_postgis -O cartoview cartoview_data"