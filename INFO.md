# Introduction to Kubernetes

## What is it?

Open Source system/platform for automating deployment, scaling and management of containerized and cloud-native applications. A container orchestrator. Cloud-native application design is to have small components that make up an application, which in return, allows for easier scaling/deployment/monitoring/rollout.

## What it can do?

- Networking - provides a frameowkr for managing and controlling containers' network communications. 
- Security - provides features that allow to build more secure applications. 
- Configuration Management - Helps manage application configuration and pass configuration data to containers.
- ...and much more!

## What is **Kubernetes Cluster**?

Kubernetes Cluster is a collection of nodes (machines) that can run containers. There are only two main components:

1. Control Plane (Master Node)
2. Workers (Worker Node)

## What is **Control plane**?

Control plane manages one or more worker nodes.

- Collection of services that control the cluster.
- Also known as master node(s).
- Consists of multiple components. Each component can be run on multiple instances for High Availability.
- User/Engineer interacts with the clusting using Control plane.
- Monitors state of the cluster. Handles cluster as a whole.

## What are **Worker nodes**?

Machines that run containers within the cluster.

- Runs and manages containers on the node.
- Requires a container runtime to manage containers.
- Uses 'kubelet' to manage Kubernetes activity on the node.
- Monitors the state of containers on the node and reports the status back to control plane.
- Manages objects in a declarative state.
- Only performs actions that are related to that specific worker node.

## What is **Kubernetes Api**?

Core of Kubetnetes Control Plane, a core component of control plane, is an API server.

- A basic HTTP API.
- Performs CRUD (Create, Read, Update, Delete) style operations.
- Is the interface between the users and the cluster itself.
- Lets users query and manipulate objects, thereby controlling the cluster.
- Kubernetes components communicate to each other via the Kubernetes API.

## What is **etcd**?

A consistent, HA and distributed key/value store that is utilized by Kubernetes for storing cluster data.

- Kubernetes utilizes it a sort of database.
- Kubernetes stores configuration of the cluster in etcd.
- Most noticeably, it stores configuration data, state data and metadata for Kubernetes.

## What are Kubernetes Objects?

Persistent data entities stored by Kubernetes. Represent state of cluster.

- When interacting with Kubernetes API, essentially, just interacting with objects.
- Can create or manipulate Kubernetes Objects via Kubernetes API.
- Basically some data that is stored on Control Plane that represents the state of some resource in the cluster.
- Kubernetes Objects are generally presesnted in the form of YAML data.
- Nearly all Kubernetes Objects have an API version associated with them, and are defined in the YAML template. Allows defining which version of Kubernetes API is the Kubernetes Object compatible with.

## Kubernetes networking

- Kubernetes manages the Pod Networking.
- Utilizes CNI (Container Networking Interface) that implements networking using third party plugins.
- Each Node of the Cluster get allocated with a subset of addresses from it.
- When Pods are provisioned, depending on the Node that they are created in - they get an IP from the IP range that is associated to that Node.
- Every Pod gets an IP.
- The IP allocated to the Pod is what it identifies it's address as.
- Generally, the IP allocated to the Pod can be reached from any of the other Nodes or Pods in the Kubernetes Cluster.

## Kubernetes networking - Services (cont'd)

- **Kubernetes Services** object provider a "_Stable Network Abstraction_", which can allow one Pod to communicate with another directly via the Service itself instead of having to tell Each Pod the address of the other Pod for communication.
- Every **Kubernetes Services** gets a name and an IP. During the lifecycle of the Service, the Name/IP never change and are relatively _static_ in nature. This allows for stability and reliability for communication between Pods.
- **Kubernetes Service** is responsible for exposing an interface to those pods, which enables network access from either within the cluster or between external processes and the service.
- The name and IP of the **Kubernetes Service** get registered in the Kubernetes Cluster's built-in DNS (or addon DNS),
- Every Kubernetes Cluster has a native DNS (whether enabled or disabled), every Pod knows how to utilize it.
- The DNS plugin allows for every Pod on the cluster to be able to resolve a Service name.
- In order to tell the Kubernetes Service which Pods to route traffic to, `label selectors` are utilized.
- When a **Service** object is created with a `label selector`, Kubernetes creates another object called an `endpoint` object (ep).
- Endpoint Objects are list of Pod IPs and Ports that match the Service's `label selector`. **Endpoint** object name is always the same as that of the **Service**.
- **Service** keeps watching/communicating with the Kubernetes API to check for the state of Pods, whether they are being added or removed and updates the list in the `endpoint` object.
- **kube-proxy** basically writes IPVS/IPTABLES rules on each node that facilitate addressing any requests to a Service to the relative Pod Address that lives under that service.
- IPVS mode which has been stable since Kubernetes 1.11 (utilzied by **kube-proxy**) is more scaleable, utilizes the Linux Kernel IP Virtual Server and is a Native Layer 4 Load Balancer when compared to IPTABLES mode. **Round-Robin** is the default in IPVS mode but can use other mechanisms.

Types of Services:

- ClusterIP: Is the default if you don't specify a type. Gets it's own IP and exposes a service which is only accessible from within the Kubernetes cluster.
- NodePort: Can access via ClusterIP. However, main point is that it gets a cluster-wide port and can be accessed externally. Takes the IP of a node on the Kubernetes Cluster and appends the NodePort value as a Cluster-wide port to that IP. Exposes a service via a static port on each node's IP. Default ports that can be utilized are between 30000-32767, which can be changed if needed using the Kubernetes API flag `service-node-port-range`. While utilizing NodePort service, you can access the pod's container on a combination of either ClusterIP:ContainerPort or AnyNodeIP:NodePort.
- LoadBalancer: Provisions a Cloud based internet facing Loadbalancer, integrates that with the Kubernetes Cluster and proxies traffic to the pods in the service. Works fine with AWS/Azure/GCP.
- ExternalName: Maps a service to a predefined externalName field by returning a value for the CNAME record.

## What about Kubernetes Storage (PV Subsystem i.e. Persistent Volume Subystem)?

- Use of volumes in Kubernetes is to abstract storage/data from Pod.
- Unless Kubernetes volumes are used, any of the data/storage used essentially lives/dies with the Pod's lifecycle.
- Kubernetes Volumes (PV) make external storage available on Kubernetes Cluster.
- Kubernetes Volumes are to be used for persistent data/storage that needs to be retained or exist beyond the lifecycle of a Pod.
- Kubernetes Volumes exist on the cluster conceptually.
- In order for a Pod to utilize a Kubernetes Volume, it performs a **claim** to the Kubernetes Volume.
- Kubernetes Volume can be shared between pods (some limitations/considerations).
- Essentially providers an interface for Kubernetes to utilize physical/virtual storages such as EBS, S3, Physical disks etc..
- **CSI** (Container Storage Interface) is preferrably used by Kubernetes to achieve this. CIS is an open-standard that can be used with any container technology.

- PV subsystem consists of:

  - PV: Stands for Persistent Volume. Considered as storage resource.
  - PVC: Stands for Persistent Volume Claim. A mechanism that allows for PV's usage by defining what Pod can perform a claim to use a PV.
  - SC: Stands for Storage Classes. Allows achieving PV + PVC in a scalable dynamic way.

- Fields for the `spec` block for both **PersistentVolume** and **PersistentVolumeClaim** objects need to match for binding/usage. Keys such as `accessModes`, `storageClassName` need to be identical whereas `capacity.storage` can be identical or lower in capacity in the definition of PVC.

- Access Modes for PersistentVolume/PersistentVolumeClaim contain:

  - RWO (ReadWriteOnce): Only one Pod can ReadWrite.
  - RWM (ReadWriteMany): Multiple Pods can ReadWrite.
  - ROM (ReadOnlyMany): Multiple Pods can Read.
  - **NOTE**: NOT all volumes support all modes and a PersistentVolume can only have one PVC/AccessMode. Generally, RWM is supported with NFS based storages (e.g. EFS in AWS), compared to Block storage volumes.

- Retain Policy:

  - Delete: Will delete the Kubernetes PV and if supported by CSI, then also the actual volume.
  - Retain: Will retain the Kubernetes PV even if the Pod let's go of the PVC.

## What is `kubectl`?

Kubernetes CLI that allows to run commands against Kubernetes cluster.

- Facilitates interacting with Kubernetes via CLI.
- Communicates with Kubernetes API.
- Makes POST requests to the Kubernetes API.
- Allows to view, create, modify and delete Kubernetes Objects.
- Can be used to deploy applications, inspect and manage cluster resources, view logs etc..

## Examples usage of `kubectl`

- Retrieve complete list of supported resources.

  ```shell
  kubectl api-resources
  ```

- List all services in ps output format

  ```shell
  kubectl get services
  ```

- Retrieve detailed description of the service named `kubernetes`

  ```shell
  kubectl describe service kubernetes
  ```

- List all pods in ps output format with more information (such as node name)

  ```shell
  kubectl get pods -o wide
  ```

## What are Pods?

Group of one or more containers, with shared storage and network resources and a specification for how to run the containers.

- A Kubernetes Object that represents one or more closely connected containers in the cluster.
- Can run more than one container. However, needs to run atleast one.
- Unless there's a specific need to run two different application containers in the same pod - ideally, different application containers should be run in different pods.
- Pods can be defined/specified/created using a YAML specification.
- Designed to be ephemeral in nature, i.e. can be destroyed at any time.

Example Pod YAML specification:

```yaml
apiVersion: v1 # Version of the Kubernetes API that the kubernetes object is compatible with
kind: Pod # The kind of Kubernetes Object.
metadata:
  name: nginx-pod # Name of the Pod Object in the cluster
spec: # Desired state of your object. List of one or more containers included in the Pod
  containers:
  - name: nginx # Container name in the pod
    image: nginx # Image name for the container
    ports:
    - containerPort: 80 # Port of container to expose
```