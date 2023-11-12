#!/bin/bash

set -x

curl localhost:5000/api/count
curl localhost:5000/api/histogram?column=FEAT_ED_OD
curl localhost:5000/api/mean?column=FEAT_VITAL_DBP_FIRST

