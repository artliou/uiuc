import json
import requests
from flask import Flask, request, Response, jsonify
from flask.helpers import make_response
from kubernetes import client, config
from os import path
import yaml
application = Flask(__name__)
config.load_kube_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()
# export FLASK_ENV=development

def create_free_job_object():
    # Configure Premium Env Variables
    var1 = client.V1EnvVar(
        name="DATASET",
        value="kmnist"
    )
    var2 = client.V1EnvVar(
        name="TYPE",
        value="cnv"
    )
    resources = client.V1ResourceRequirements(
        requests={"memory": "500Mi", "cpu": "0.9"},
        limits={"memory": "800Mi", "cpu": "0.9"},
    )
    # Configureate Pod template container
    container = client.V1Container(
        name="free",
        image="arthurl3/cs498:mp3",
        command=["python",  "./classify.py"],
        env=[var1, var2],
        resources=resources
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "free"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(generate_name="free-class-"),
        spec=spec)
    return job

def create_premium_job_object():
    # Configure Premium Env Variables
    var1 = client.V1EnvVar(
        name="DATASET",
        value="mnist"
    )
    var2 = client.V1EnvVar(
        name="TYPE",
        value="ff"
    )
    # Configureate Pod template container
    container = client.V1Container(
        name="premium",
        image="arthurl3/cs498:mp3",
        command=["python",  "./classify.py"],
        env=[var1,var2]
    )
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "premium"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(generate_name="premium-class-"),
        spec=spec)

    return job

def create_job(api_instance, job, namespace):
    # print("Using Namespace", namespace)
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace=namespace)
    # print("Job created. job='%s'." % str(api_response))
    print("Job created. status='%s'." % str(api_response.status))

# Flask Server Implementation
@application.route("/config", methods=['GET'])
def get():
    print("GET Received")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    # Format 200 and Response
    mylist = []
    for pod in ret.items:
        # print("%s\t%s\t%s" % (pod.status.pod_ip, pod.metadata.namespace, pod.metadata.name))
        podObj = {
            "name": pod.metadata.name,
            "ip:": pod.status.pod_ip,
            "namespace": pod.metadata.namespace,
            "node": pod.spec.node_name,
            "status": pod.status.phase
        }
        print (podObj)
        mylist.append(podObj)
    return make_response(jsonify(pods=mylist), 200)

@application.route("/img-classification/free", methods=['POST'])
def postFree():
    strMessage = "POST @ /img-classification/free"
    # dataset = request.json["dataset"]
    print("%s\t" % strMessage)
    # print("Dataset: %s\t" % dataset)
    # print("Post Body: %s\t", request)
    job = create_free_job_object()
    create_job(batch_v1, job, "free-service")
    message = {
        'status': 200,
        'message': strMessage,
    }
    return make_response(jsonify(message), 200)

@application.route("/img-classification/premium", methods=['POST'])
def postPremium():
    strMessage = "POST @ /img-classification/premium"
    # dataset = request.json["dataset"]
    print("%s\t" % strMessage)
    # print("Post Body: %s\t", request)
    job = create_premium_job_object()
    create_job(batch_v1, job, "default")
    message = {
        'status': 200,
        'message': strMessage,
    }
    return make_response(jsonify(message), 200)

if __name__ == "__main__":
	application.run('0.0.0.0', port='5000', debug=True)
