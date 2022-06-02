#!/usr/bin/env bash

set -x
psql -U postgres dropdb template_postgis
psql -U postgres dropdb cartoview
psql -U postgres dropdb cartoview_data
psql -U postgres dropdb upload_test
psql -U postgres dropdb test_upload_test
psql -U postgres dropuser cartoview
psql -U postgres createuser cartoview -d -s
psql -U postgres -c "ALTER USER cartoview WITH PASSWORD 'cartoview';"
psql -U postgres createdb template_postgis
psql -U postgres -d template_postgis -c 'CREATE EXTENSION postgis;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
psql -U postgres -d template_postgis -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cartoview;'
psql -U postgres createdb -O cartoview cartoview
psql -U postgres createdb -T template_postgis -O cartoview cartoview_datastore