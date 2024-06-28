db_file="instance/sharejog.sqlite"

pref_csv_file="flask_app/data/prefectures.csv"
pref_table_name="data_models_prefectures"

city_csv_file="flask_app/data/cities.csv"
city_table_name="data_models_cities"

facility_csv_file="flask_app/data/facilities.csv"
facility_table_name="data_models_facilities"

sqlite3 $db_file <<EOF
.mode csv
.import $pref_csv_file $pref_table_name
.import $city_csv_file $city_table_name
.import $facility_csv_file $facility_table_name
.quit
EOF