import docker
import socket
import requests

from docker.models.containers import Container
from typing import Any

from tempo.serve.protocol import Protocol
from tempo.serve.runtime import Runtime
from tempo.serve.metadata import ModelDetails
from tempo.seldon.protocol import SeldonProtocol
from tempo.seldon.containers import (
    DefaultHTTPPort,
    DefaultModelsPath,
    get_container_spec,
)


class SeldonDockerRuntime(Runtime):
    def __init__(self, protocol=None):
        if protocol is None:
            self.protocol = SeldonProtocol()
        else:
            self.protocol = protocol

    def get_protocol(self) -> Protocol:
        return self.protocol

    def get_endpoint(self, model_details: ModelDetails) -> str:
        container = self._get_container(model_details)
        port_index = self._get_port_index()
        host_ports = container.ports[port_index]

        host_ip = host_ports[0]["HostIp"]
        host_port = host_ports[0]["HostPort"]

        protocol = self.get_protocol()
        predict_path = protocol.get_predict_path(model_details)

        return f"http://{host_ip}:{host_port}{predict_path}"

    def remote(self, model_details: ModelDetails, *args, **kwargs) -> Any:
        protocol = self.get_protocol()
        req = protocol.to_protocol_request(*args, **kwargs)
        endpoint = self.get_endpoint(model_details)
        response_raw = requests.post(endpoint, json=req)
        return protocol.from_protocol_response(
            response_raw.json(), model_details.outputs
        )

    def deploy(self, model_details: ModelDetails):
        docker_client = docker.from_env()
        protocol = self.get_protocol()
        container_index = self._get_port_index()
        model_folder = model_details.local_folder
        container_spec = get_container_spec(model_details, protocol)

        docker_client.containers.run(
            name=self._get_container_name(model_details),
            ports={container_index: self._get_available_port()},
            volumes={model_folder: {"bind": DefaultModelsPath, "mode": "ro"}},
            detach=True,
            **container_spec,
        )

    def _get_port_index(self):
        return f"{DefaultHTTPPort}/tcp"

    def wait_ready(self, model_details: ModelDetails, timeout_secs=None) -> bool:
        container = self._get_container(model_details)
        print(container.status)
        return container.status == "running"

    def _get_available_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def undeploy(self, model_details: ModelDetails):
        container = self._get_container(model_details)
        container.remove(force=True)

    def _get_container(self, model_details: ModelDetails) -> Container:
        container_name = self._get_container_name(model_details)

        docker_client = docker.from_env()
        container = docker_client.containers.get(container_name)

        return container

    def _get_container_name(self, model_details: ModelDetails):
        return model_details.name

    def to_k8s_yaml(self, model_details: ModelDetails) -> str:
        raise NotImplementedError()
