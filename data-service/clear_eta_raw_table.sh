#!/bin/bash
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "TRUNCATE train_eta_raw;"