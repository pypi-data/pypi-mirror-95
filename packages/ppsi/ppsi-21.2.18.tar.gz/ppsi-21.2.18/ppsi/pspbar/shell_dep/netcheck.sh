#!/usr/bin/env bash
# -*- coding:utf-8; mode: shell-script -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
#
## Check for netknown connectivity at the beginning
# This file is part of Prady_runcom.
#
# Prady_runcom is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prady_runcom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prady_runcom.  If not, see <https://www.gnu.org/licenses/>.

# This script has been copied from another program that I had written.

# Variables
google_ping_cmd="ping 8.8.8.8 -c 1 -q -w 2"
known_ping_cmd="ping 192.168.1.101 -c 1 4 -q -w 2"
inter=0
intra=0
known=0
home=0
ip_addr=
ap_addr=


# IP->AP addresses
ip_addr=`ip addr | grep "wlp" | grep "inet" | cut -d "t" -f 2 | cut -d " " -f 2 | cut -d "/" -f 1`;
if [[ -z $ip_addr ]]; then
	ip_addr=`ip addr | grep "en" | grep "inet" | cut -d "t" -f 2 | cut -d " " -f 2 | cut -d "/" -f 1`;
fi
if [[ -z $ip_addr ]]; then
	ip_addr=`hostname -I`;
fi


ap_addr="$(ip neigh | grep "\.1 " |cut -d " " -f 1)";
intra_ping_cmd="ping ${ap_addr} -c 1 -q -w 2"

export ap_addr
export ip_addr

if [[ -n "$ip_addr" ]]; then
    $google_ping_cmd 2>&1 1>/dev/null && inter=1
    $intra_ping_cmd 2>&1 1>/dev/null && intra=1
    [[ "$ap_addr" =~ "192.168.0.1" ]] && home=1
    [[ "$ap_addr" =~ "192.168.1.1" ]] && home=1
    [[ "$home" == "0" ]] && $known_ping_cmd 2>&1 1>/dev/null && known=1
fi

echo -e "${ip_addr}\t${ap_addr}\t$(( 8 * $inter + 4 * $intra + 2 * $home + $known ))"
