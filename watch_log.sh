#!/bin/bash

tail -f $logfile | grep "\(INFO\|WARN\|ERRO\|CRIT\)"
