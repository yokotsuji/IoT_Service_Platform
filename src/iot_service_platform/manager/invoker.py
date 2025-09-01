# manager/invoker.py

from adapters.actuator_adapter import execute_command

def invoke(service_type: str, place: str, command: str) -> str:
    """
    アクチュエータへの指令実行
    """
    result = execute_command(service_type, place, command)
    return result