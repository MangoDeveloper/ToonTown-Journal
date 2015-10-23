#!/bin/sh
cd `dirname $0`
cd ..
./astrond --loglevel info config/astrond.yml
