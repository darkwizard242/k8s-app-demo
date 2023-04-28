# k8s-app-demo

This repository contains a sample container app (utilizes **FastAPI** framework), let's call it "**tooling**", that connects to a PostgreSQL database. Repository also contains a Helm Chart to release it to Kubernetes Cluster for demo/learning purposes.

To get familiar with some of the Kubernetes objects, please [read this](/INFO.md).

## Requirements:

The following applications are utilized in this project, and thus, are required:

- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [helm](https://helm.sh/docs/intro/install/)
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Cloning Repository:

#### Using HTTPS protocol:
```shell
git clone https://github.com/darkwizard242/k8s-app-demo.git k8s-app-demo
```

#### Using SSH protocol:
```shell
git clone git@github.com:darkwizard242/k8s-app-demo.git k8s-app-demo
```

## Tutorial (docker/docker-compose)

This project already contains a `Dockerfile` and `docker-compose`. Using these, you can run the FastAPI app and Postgresql database.

### 1. Build container image:

Run the following to build the container image:
```shell
docker-compose build
```

### 2. Run container image:

Run the following to provision the container(s) in a detached mode (if you prefer non-detached mode, execute `docker-compose up`):
```shell
docker-compose up -d
```


## Tutorial (Kubernetes/minikube)

### 1. Getting **Minikube** ready:

Following command starts a local kubernetes cluster with Kubernetes version `1.25.3` while utilizing `docker` as the driver.
```shell
minikube start --driver=docker --kubernetes-version=1.25.3
```  

Validate the output of Cluster.

```shell
kubectl cluster-info
```

Retrieve Nodes information:

```shell
kubectl get nodes -o wide
```

Validate all pods in `kube-system` namespace are **READY**:
```shell
kubectl -n kube-system get pods
```

### 2. Install **metrics-server**:

Apply YAML manifest for `metrics-server`:
```shell
kubectl apply -f metrics-server.yaml
```

Ensure `metrics-server` Pod is in **READY** state:
```shell
kubectl get pods -l k8s-app=metrics-server -n kube-system
```

If POD is in a state where image PULL has failed, attempt to PULL using the following:
```shell
minikube ssh docker pull k8s.gcr.io/metrics-server/metrics-server:v0.6.2
```

### 3. Utilize minikube's docker daemon and build image:

To build and run container (in this case _docker_ images) in minikube's environment, execute the following to configure the appropriate environment variables:

```shell
eval $(minikube docker-env)
```

Build the container image:
```shell
docker build -t local/tooling:v1 .
```

### 4. Deploy and validate:

For the purpose of this tutorial, we will release the helm chart against a specific namespace called `demo'. Let's get started by creating the namespace:
```shell
kubectl create ns demo
```

Add **bitnami** helm chart repository:
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
```

Pull dependent chart to disk:
```shell
helm dependency build helmchart/
```

Deploy the Kubernetes Objects defined in the _Helm Chart_ using **helm** to  the previously created `demo` namespace while naming the Helm Release as **tooling**:
```shell
helm upgrade -i tooling helmchart/ --namespace demo
```

Once deployed, validate that all Pods are `demo` namespace are in READY state. _**NOTE** that it may take a few minutes for the Pods to be in READY state as a postgresql image is pulled down and rolled out, and is required for the app to successfully initialize_).
```shell
kubectl get pods -n demo
```

Helm chart test hooks are part of the chart, run the following to let helm perform those tests for you:
```shell
helm test tooling -n demo
```

To tail the app logs, run the following:
```shell
kubectl logs -f -l app.kubernetes.io/name=tooling -n demo
```


### 5. Access Application Endpoints:

By default, `ClusterIP` is used in this helm chart, which technically means that the `Service` endpoint is only accessible within the cluster. 

In order to access the application endpoints, `kubectl port-forward` can be used. It will allow connection/traffic to a local port to be forwarded to the port of the `Service` in the cluster for navigation/access purposes.

The command below will setup port forwarding (`<HOST_PORT_80>:<SVC_PORT_80>`) on a local host port **80** to be forwarded to the `Service` port, which also is running on port **80**.

```shell
kubectl port-forward svc/tooling 80:80 -n demo
```

Please note that `kubectl port-forward` process runs interactively (i.e. as a foreground process | use `CTRL+C` or `CMD+C` keys to end the process), so you may need to open another terminal session for any other activities.


The following command intializes a Pod that makes calls to the `Service` Endpoint with the hostname path to retrieve hostname of the Pods traffic is routed to:
```shell
kubectl run -n demo -i --tty load-generator --rm --image=busybox --restart=Never -- sh -c "while sleep 0.01; do wget -q -O- http://tooling.demo.svc.cluster.local/private/hostname && echo; done"
```

### 6. Load testing (optional):

Following command will run a pod based on Apache Bench that will load test the **Service** Endpoint:
```shell
kubectl run -i --tty apache-bench --rm --image=jordi/ab --restart=Never -- -k -c 100 -t 300s http://tooling.demo.svc.cluster.local/private/hostname
```

In the mean time, you can monitor the HorizontalPodAutoscaler to view scale-in and scale-out activities:
```shell
kubectl get hpa tooling -n demo -w
```

### 7. Cleanup:

Uninstall the helm chart:
```shell
helm uninstall tooling -n demo
```

Stop minikube cluster:
```shell
minikube stop
```

Delete minikube cluster:
```shell
minikube delete
```


## Endpoint Requests (optional)

##### GET Request (`/`):

```shell
curl -i -H "Content-Type: text/html" -X GET http://localhost/
```

##### GET Request (`/private/hostname`):

```shell
curl -i -H "Content-Type: application/json" -X GET http://localhost/private/hostname
```

##### GET Request (`/health/liveness`):

```shell
curl -i -H "Content-Type: application/json" -X GET http://localhost/health/liveness
```

##### GET Request (`/health/readiness`):

```shell
curl -i -H "Content-Type: application/json" -X GET http://localhost/health/readiness
```

##### GET Request (`/secrets`):

```shell
curl -i -H "Content-Type: application/json" -X GET http://localhost/secrets
```

##### POST Request (`/publisher`):

```shell
curl -i -d '{"text":"HTTP POST method testing"}' -H "Content-Type: application/json" -X POST http://localhost/publisher
```

## License

[MIT](/LICENSE)

## Author Information

This project was developed by [Ali Muhammad](https://www.alimuhammad.dev/).