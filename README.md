# flix-code-challenge
Flixbus Code Challenge Repo (done on a Mac)

## Setup Minikube
```
brew install minikube
```
```
minikube start --memory 4096
```
```
brew install kubectl
```
```
brew install helm
```
## Setup Kafka (and Zookeeper)

Reference: https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes/ 

```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
```
helm install zookeeper bitnami/zookeeper \
  --set replicaCount=1 \
  --set auth.enabled=false \
  --set allowAnonymousLogin=true
```
```
helm install kafka bitnami/kafka \
  --set zookeeper.enabled=false \
  --set replicaCount=1 \
  --set externalZookeeper.servers=zookeeper.default.svc.cluster.local
```

### Create Kafka Topics
```
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")
```
```
kubectl --namespace default exec -it $POD_NAME -- kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic input_topic
```
```
kubectl --namespace default exec -it $POD_NAME -- kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic output_topic
```

### Start a Kafka message consumer to test the setup
```
kubectl --namespace default exec -it $POD_NAME -- kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic output_topic
``` 

### Start a Kafka message producer to test the setup
```
kubectl --namespace default exec -it $POD_NAME -- kafka-console-producer.sh --broker-list localhost:9092 --topic input_topic
```

## Deploy the Transformer Application

The docker image is available at https://hub.docker.com/repository/docker/timokraus/utc-transformer 

To deploy it, run:
```
kubectl apply -f Deployment.yaml
```

To test the application, go to your console window where you started the input_topic producer and insert the test data manually:

* {"myKey": 1, "myTimestamp": "2022-03-01T09:11:04+01:00"}
* {"myKey": 2, "myTimestamp": "2022-03-01T09:12:08+01:00"}
* {"myKey": 3, "myTimestamp": "2022-03-01T09:13:12+01:00"}
* {"myKey": 4, "myTimestamp": ""}
* {"myKey": 5, "myTimestamp": "2022-03-01T09:14:05+01:00"}

The output messages will appear in UTC time at the output_topic consumer:

* {"myKey": 1, "myTimestamp": "2022-03-01T08:11:04+00:00"}
* {"myKey": 2, "myTimestamp": "2022-03-01T08:12:08+00:00"}
* {"myKey": 3, "myTimestamp": "2022-03-01T08:13:12+00:00"}
* {"myKey": 4, "myTimestamp": ""}
* {"myKey": 5, "myTimestamp": "2022-03-01T08:14:05+00:00"}