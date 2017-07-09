#!/bin/bash
DATABASE_URL=$(heroku config:get DATABASE_URL -a pgadmin3) pgadmin3
