# Continuous Integration

Our Continuous Integration (CI) approach is one of _"zero-infrastructure overhead"_. As such, we utilize [GitHub Actions](https://github.com/features/actions) to build and push the microservice's associated container image to Docker Hub for public consumption.  The GitHub Actions workflows are defined in the owning repository's `.github/workflows/dockerbuild.yaml` file.

The **Reefer Simulator** microservice's CI implementation can be found via [/.github/workflows/dockerbuild.yaml](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/blob/master/.github/workflows/dockerbuild.yaml) in the [refarch-reefer-ml](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/) repository, while the **SpringContainerMS** microservice's CI implementation can be found via [.github/workflows/dockerbuild.yaml](https://github.com/ibm-cloud-architecture/refarch-kc-container-ms/blob/master/.github/workflows/dockerbuild.yaml) in the [refarch-kc-container-ms](https://github.com/ibm-cloud-architecture/refarch-kc-container-ms/) repository. For results of individual completed CI workflow actions, you can view the results via the **Actions** tab of a given repository.

## Overview of Continuous Integration workflows for this project

### 1 - Validate Docker Secrets

The first job in each GitHub Actions workflow, `validate-docker-secrets`, ensures that all the necessary Secrets are defined on the repository under which the build action is running. Similar to Kubernetes Secrets, [GitHub Repository Secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets) allow you to store encrypted, sensitive information in a programmatically accessible way.

### 2 - Build Component Images

#### Appsody build for the Simulator microservice

The [simulator](https://github.com/ibm-cloud-architecture/refarch-reefer-ml/tree/master/simulator) microservice is built using the [Appsody](https://appsody.dev) open-source project, while leveraging the [Python Flask Appsody Stack](https://github.com/appsody/stacks/tree/master/incubator/python-flask) for its underlying framework.  The project can be easily built in a local environment by issuing the `appsody build` commands, further documented on the Appsody site under [Building and deploying](https://appsody.dev/docs/using-appsody/building-and-deploying).

The second job in the Simulator microservice workflow, `build-simulator-image`, runs on a base Ubuntu container image, creates a new semtanically-versioned tag _(in the form of `0.1.2`)_ for the repository, installs the latest Appsody CLI tools, performs the `appsody build` command with the [appropriate parameters](https://appsody.dev/docs/using-appsody/building-and-deploying#building-your-runtime-docker-image-with-appsody), tags the newly created version-specific image with `latest` as well, and pushes the image with both tags to the public Docker Hub repository defined by the aforementioned repository secrets.

#### Container build for the Spring Container microservice

The [SpringContainerMS](https://github.com/ibm-cloud-architecture/refarch-kc-container-ms/tree/master/SpringContainerMS) microservice is developed using the Spring Boot framework, compiled via `maven` and an associated `pom.xml` file, and packaged via a traditional Dockerfile. This project can be built locally via Maven and/or Docker, however it is recommended to consume the published container images that are a result of this continuous integration.

The second job in the SpringContainerMS microservice workflow, `build-springcontainer-image`, runs on a base Ubuntu container image, creates a new semtanically-versioned tag _(in the form of `0.1.2`)_ for the repository, performs a traditional `docker build` using the [SpringContainerMS/Dockerfile](https://github.com/ibm-cloud-architecture/refarch-kc-container-ms/blob/master/SpringContainerMS/Dockerfile), tags the newly created version-specific image with `latest` as well, and pushes the image with both tags to the public Docker Hub repository defined by the aforementioned repository secrets.

### 3 - GitOps Updates

The final job, `gitops-repo-webhook`, is a linkage to our general continuous deployment process, which is GitOps-based and available via [ibm-cloud-architecture/refarch-kc-gitops](https://github.com/ibm-cloud-architecture/refarch-kc-gitops). This step will perform a webhook call to our GitOps repository and notify that repository's GitHub Actions that an update to one of its component's container images has been made and it should scan for the latest version of all the known container images and update the associated YAML files for environment updates. Further description of this continuous deployment process will be covered in [Continuous Deployment](cd.md).
