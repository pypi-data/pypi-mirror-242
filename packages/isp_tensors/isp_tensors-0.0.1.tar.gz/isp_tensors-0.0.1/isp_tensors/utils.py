import importlib
import json
import struct

def load_framework(framework: str):
    if framework == "torch":
        return importlib.import_module("safetensors.torch")        
    elif framework == "tensorflow":
        return importlib.import_module("safetensors.tensorflow")
    elif framework == "numpy":
        return importlib.import_module("safetensors.numpy")
    elif framework == "jax":
        return importlib.import_module("safetensors.flax")
    elif framework == "padddle":
        return importlib.import_module("safetensors.paddle")
    else:
        raise ValueError(f"Unknown framework {framework}")

def check_simple_dict(metadata: dict):
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a dictionary")
    
    # the dict can't be nested dict
    if any(isinstance(v, dict) for v in metadata.values()):
        raise ValueError("metadata can't be nested dict")

    # the dict only support string, float, int, bool
    if any(not isinstance(v, (str, float, int, bool)) for v in metadata.values()):
        raise ValueError("metadata only support string, float, int, bool")

    return True

def dict_to_bytes(metadata: dict):
    return json.dumps(metadata) \
               .replace(": ", ":") \
               .replace(", ", ",") \
               .encode("utf-8")


def get_length_of_header(data: bytes):
    return struct.unpack('<Q', data[:8])[0]


def get_metadata(bytes, nl_header=None):
    if nl_header is None:
        nl_header = get_length_of_header(bytes)    
    return json.loads(bytes[8:7 + nl_header])