#!/usr/bin/env bash

set -e

python sanitise_papers.py
python neuron_data_ma.py
python neuron_data_np.py
python cls2nodes.py

echo "Done!"
