:loop
@echo off
date /t >> test_mx.log
time /t >> test_mx.log
nslookup -type=MX foo.pagerduty.com >> test_mx.log
time /t >> test_mx.log
nslookup -type=MX foo.pagerduty.com 8.8.8.8 >> test_mx.log
time /t >> test_mx.log
nslookup -type=MX -d2 foo.pagerduty.com >> test_mx.log
time /t >> test_mx.log
timeout 5
goto loop