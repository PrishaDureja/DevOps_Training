#!/bin/bash
set -e
while true; do
  echo "report: $(date)" >> /var/log/reporter/report.log
  sleep 10
done
