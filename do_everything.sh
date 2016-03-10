#!/usr/bin/env bash

set -e

python sanitise_papers.py
python neuron_data_ma.py
python neuron_data_np.py
python cls2nodes.py
python find_difference.py
py.test prototype_network.py

echo "Done!"
