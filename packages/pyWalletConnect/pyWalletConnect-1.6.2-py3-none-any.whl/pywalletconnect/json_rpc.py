# -*- coding: utf8 -*-

# pyWalletConnect : JSON RPC
# Copyright (C) 2021-2022 BitLogiK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have receive a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


"""JSON RPC for pyWalletConnect"""


from json import dumps, loads
from time import time_ns


# ---- Helpers about messages encoding


def json_encode(dataobj):
    """Compact JSON encoding."""
    return dumps(dataobj, separators=(",", ":"))


# ---- JSON RPC functions to pack/unpack

# The wallet is a JSON-RPC service in the WalletConnect standard


def rpc_query(method, params):
    """Build a JSON-RPC query object."""
    return {
        "jsonrpc": "2.0",
        "id": time_ns(),
        "method": method,
        "params": params,
    }


def json_rpc_unpack_response(raw_response):
    """Decode JSON-RPC raw bytes response and return result."""
    try:
        resp_obj = loads(raw_response)
    except Exception as exc:
        raise Exception(f"Error : not JSON response : {raw_response}") from exc
    if resp_obj["jsonrpc"] != "2.0":
        raise Exception(f"Server is not JSONRPC 2.0 but {resp_obj.jsonrpc}")
    if "error" in resp_obj:
        if "message" in resp_obj["error"]:
            err_msg = resp_obj["error"]["message"]
        else:
            err_msg = resp_obj["error"]
        raise Exception(err_msg)
    if "result" not in resp_obj:
        raise Exception(f"No result in response {raw_response}")
    return resp_obj["result"]


def json_rpc_pack_response(idmsg, result_obj, success=True):
    """Build a JSON-RPC response."""
    response_type = "result" if success else "error"
    request_obj = {
        "jsonrpc": "2.0",
        "id": idmsg,
        response_type: result_obj,
    }
    return json_encode(request_obj).encode("utf8")


def json_rpc_unpack(buffer):
    """Decode a JSON-RPC call query : id, method, params."""
    try:
        resp_obj = loads(buffer)
    except Exception as exc:
        raise Exception(f"Error : not JSON response : {buffer}") from exc
    if resp_obj["jsonrpc"] != "2.0":
        raise Exception(f"Server is not JSONRPC 2.0 but {resp_obj.jsonrpc}")
    if "error" in resp_obj:
        if "message" in resp_obj["error"]:
            err_msg = resp_obj["error"]["message"]
        else:
            err_msg = resp_obj["error"]
        raise Exception(err_msg)
    return resp_obj["id"], resp_obj.get("method"), resp_obj.get("params")
