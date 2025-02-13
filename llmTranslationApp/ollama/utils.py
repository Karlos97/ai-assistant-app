import requests


class MicroserviceHealthError(Exception):
    """Custom exception for microservice health check errors."""

    pass


def check_microservice_health(microservice_url):
    try:
        response = requests.get(microservice_url, timeout=60)
        if response.status_code == 200:
            return True
        else:
            raise MicroserviceHealthError(
                f"Microservice unhealthy: {response.status_code} {response.text}"
            )
    except requests.exceptions.RequestException as e:
        raise MicroserviceHealthError(f"Microservice unreachable: {str(e)}")
