#!/usr/bin/env bash
set -e
mkdir -p ./http/config
./get_geth_enode.sh | echo "`awk -F '@' '{print $1}'`""@"`cat ./config/bootnode_ip`:30310 | tee ./http/config/bootnode | tee ./config/bootnode


