#!/bin/bash
curl 'https://api.electricitymap.org/v3/power-breakdown/history?zone=FR' -H 'auth-token: use_your_token' > "/path/to/your_script/$(date +%Y%m%d%H%M)_data.json"


