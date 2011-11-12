#!/bin/bash
APP=$( dirname "${BASH_SOURCE[0]}" )
~/google_appengine/dev_appserver.py $APP
