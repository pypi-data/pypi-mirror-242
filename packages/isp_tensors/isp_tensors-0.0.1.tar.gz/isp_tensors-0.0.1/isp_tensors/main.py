from typing import Optional, Any, Dict
from isp_tensors.utils import load_framework, check_simple_dict, dict_to_bytes, get_metadata
from safetensors import deserialize

import gzip
import json
import struct

def save(tensors:Any, framework: str, metadata: Optional[dict] = None) -> bytes:
    """ Save a safetensor object to a bytes object
    
    Args:
        tensors (Any): safetensor object.
        framework (str): name of the framework used to generate the safetensor.
        metadata (Optional[dict], optional): product metadata. Defaults to None.

    Returns:
        bytes: safetensor bytes object.
    """

    # Check if the dictionary have been correctly formatted
    if metadata is not None:
        check_simple_dict(metadata)
            
    # Generate the safetensor bytes
    safe_framework = load_framework(framework)
    original_safetensor = safe_framework.save(tensors)

    # Deserialize the safetensor bytes
    p_metadata = get_metadata(original_safetensor)
    p_data = dict(deserialize(original_safetensor))

    # Compress the safetensor bytes
    init_offset = 0
    for name, pkg_dict in p_data.items():
        compressed_tensor = gzip.compress(pkg_dict["data"])
        p_data[name].update({"data": compressed_tensor})
        final_offset = init_offset + len(compressed_tensor)
        p_metadata[name].update({"compress_offset": [init_offset, final_offset]})
        init_offset = final_offset
    
    # Serialize product & user metadata
    PH = dict_to_bytes(p_metadata) + b" "
    UH = dict_to_bytes(metadata) + b" "
    
    
    # Serialize the ips_tensor object
    magick_bytes = b'\x1e;4\x01\x00\x00\x00\x00' # NeverForget
    sPH = struct.pack('<Q', len(PH))
    sUH = struct.pack('<Q', len(UH))
    data = b"".join([pkg_dict["data"] for pkg_dict in p_data.values()])

    return magick_bytes + sPH + sUH + PH + UH + data

def save_file(
    tensors: Any,
    filename: str,
    framework: str,
    metadata: Optional[dict] = None,    
):
    """ Save a safetensor object to a file

    Args:
        tensors (Any): safetensor object.
        filename (str): path to the output file.
        framework (str): name of the framework used to generate the safetensor.
        metadata (Optional[dict], optional): product metadata. Defaults to None.
    """
    with open(filename, "wb") as f:
        f.write(save(tensors, framework, metadata))



def load(data: bytes, framework: str, tensor_names: Optional[list] = None) -> dict:
    """ Load a safetensor object from a bytes object
    
    Args:
        data (bytes): safetensor bytes object.
        framework (str): name of the framework used to generate the safetensor.
        tensor_names (Optional[list], optional): list of tensors to load. Defaults to None.

    Returns:
        dict: safetensor load object.
    """

    # Load the safetensor framework
    safe_framework = load_framework(framework)

    # Load the product metadata
    sPH = struct.unpack('<Q', data[8:16])[0]    
    PH = json.loads(data[slice(24, sPH + 23)])

    # Load the tensor names
    if tensor_names is None:
        tensor_names = list(PH.keys())

    # Set the init of the tensor data
    sUH = struct.unpack('<Q', data[16:24])[0]
    it = 24 + sPH + sUH

    # Save the umcompressed data
    dict_container = {}
    tensor_container = b""
    for name, pkg_dict in PH.items():
        if name in tensor_names:
            iof, fof = pkg_dict.pop("compress_offset")
            dict_container[name] = pkg_dict
            tensor_container += gzip.decompress(data[slice(it + iof, it + fof)])
    
    # Serialize the dict_container
    sdict = dict_to_bytes(dict_container) + b" "
    noh = struct.pack('<Q', len(sdict))

    return safe_framework.load(noh + sdict + tensor_container)

def load_file(
    filename: str,
    framework: str,
    tensor_names: Optional[list] = None,
):
    """ Load a safetensor object from a file

    Args:
        filename (str): path to the input file.
        framework (str): name of the framework used to generate the safetensor.
        tensor_names (Optional[list], optional): list of tensors to load. Defaults to None.

    Returns:
        dict: safetensor load object.
    """
    
    # Load the safetensor framework
    safe_framework = load_framework(framework)

    with open(filename, "rb") as f:
        f.seek(8) # skip the magick bytes
    
        # Load the product metadata
        sPH = struct.unpack('<Q', f.read(8))[0]
        sUH = struct.unpack('<Q', f.read(8))[0]
        PH = json.loads(f.read(sPH))

        # Load the tensor names
        if tensor_names is None:
            tensor_names = list(PH.keys())

        # Skip the user metadata
        f.seek(sUH, 1)
        
        # Save the umcompressed data
        dict_container = {}
        tensor_container = b""
        for name, pkg_dict in PH.items():
            if name in tensor_names:
                iof, fof = pkg_dict.pop("compress_offset")
                dict_container[name] = pkg_dict
                tensor_container += gzip.decompress(
                    f.read(fof - iof)
                )                
            else:
                f.seek(pkg_dict.pop("compress_offset")[1], 1)

    # Serialize the dict_container
    sdict = dict_to_bytes(dict_container) + b" "
    noh = struct.pack('<Q', len(sdict))

    return safe_framework.load(noh + sdict + tensor_container)


def read_metadata_bytes(data: bytes) -> Dict[str, dict]:
    """ Load the metadata from a bytes object

    Args:
        data (bytes): safetensor bytes object.
    
    Returns:
        Dict[str, dict]: a dictionary with the product 
            metadata and user metadata.
    """
    
    # read the product metadata length
    sPH = struct.unpack('<Q', data[8:16])[0]
    sUH = struct.unpack('<Q', data[16:24])[0]
    
    # read the product metadata
    PH = json.loads(data[slice(24, sPH + 23)])
    UH = json.loads(data[slice(sPH + 24, sPH + sUH + 23)])

    return {"PH": PH, "UH": UH}


def read_metadata(filename: str) -> Dict[str, dict]:
    """ Load the metadata from a isp_tensor file

    Args:
        filename (str): path to the isp_tensor file.

    Returns:
        Dict[str, dict]: a dictionary with the product 
            metadata and user metadata.
    """

    with open(filename, "rb") as f:
        f.seek(8) # skip the magick bytes
        
        # read the product metadata length
        sPH = struct.unpack('<Q', f.read(8))[0]
        sUH = struct.unpack('<Q', f.read(8))[0]
        
        # read the product metadata
        PH = json.loads(f.read(sPH))
        
        # read the user metadata
        UH = json.loads(f.read(sUH))
        
    return {"PH": PH, "UH": UH}
