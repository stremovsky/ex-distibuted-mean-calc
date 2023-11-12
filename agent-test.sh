#!/bin/bash

set -x

curl localhost:6000/api/histogram
curl localhost:6000/api/histogram?column=ID_CASE
curl localhost:6000/api/histogram?column=FEAT_ED_OD
curl localhost:6000/api/count
curl localhost:6000/api/mean?column=FEAT_VITAL_DBP_FIRST

