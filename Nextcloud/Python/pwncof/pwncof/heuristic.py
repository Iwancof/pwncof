from pwn import *
from typing import *

def read_pointer_amd64(io):
    raw = io.read(6) # 0x7fxxxxxxxxxx
    raw = raw + b'\00\00'
    
    return unpack(raw)

def find_hex(s: str) -> List[int]:
    pattern = r"0x[0-9a-fA-F]+"
    matches = re.findall(pattern, s)

    return [int(match, 16) for match in matches]
