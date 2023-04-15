#!/bin/bash

while true; do
  dig foo.pagerduty.com mx          >> ./test_mx.log
  dig @8.8.8.8 foo.pagerduty.com mx >> ./test_mx.log
  dig foo.pagerduty.com mx +trace   >> ./test_mx.log

  sleep 5
done