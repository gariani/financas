#!/bin/bash
DATABASE_URL=$(heroku config:get DATABASE_URL -a pgadmin4) pgadmin4
