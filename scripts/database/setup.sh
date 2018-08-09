#!/usr/bin/env bash

set -x
sudo -u postgres dropdb template_postgis
sudo -u postgres dropdb cartoview
sudo -u postgres dropdb cartoview_data
sudo -u postgres dropdb upload_test
sudo -u postgres dropdb test_upload_test
sudo -u postgres dropuser cartoview
sudo -u postgres createuser cartoview -d -s
sudo -u postgres psql -c "ALTER USER cartoview WITH PASSWORD 'cartoview';"
sudo -u postgres createdb template_postgis
sudo -u postgres psql -d template_postgis -c 'CREATE EXTENSION postgis;'
sudo -u postgres psql -d template_postgis -c 'GRANT ALL ON geometry_columns TO PUBLIC;'
sudo -u postgres psql -d template_postgis -c 'GRANT ALL ON spatial_ref_sys TO PUBLIC;'
sudo -u postgres psql -d template_postgis -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cartoview;'
sudo -u postgres createdb -O cartoview cartoview
sudo -u postgres createdb -T template_postgis -O cartoview cartoview_datastore