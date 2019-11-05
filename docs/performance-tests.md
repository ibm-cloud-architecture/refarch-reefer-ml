# Performance tests

We have to develop some performance tests for some client engagements. So reusing the reefer telemetry generator can help us to run performance test.

The simulator is configured to run 2 Gunicorn processes with 4 threads each. So potentially running 8 requests in parallel. (See the code [simulator/infrastructure/webappconfig.py]())
