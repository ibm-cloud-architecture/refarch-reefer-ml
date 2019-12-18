# Open Source Approach

## Build the docker image for Jupyter notebook

We are using a special version of conda to add the postgresql and kafka libraries for python so we can access postgresql or kafka from notebook. The Dockerfile may use a `cert.pem` file, which contains the postgres certificate so the notebook can connect to postgresql service with SSL connection. 

```
cd docker 
docker build -f docker-jupyter-tool -t ibmcase/jupyter .
```

To run this jupyter server use the startJupyterServer.sh script:

```
# refarch-reefer-ml project folder
./startJupyterServer.sh IBMCLOUD
```
