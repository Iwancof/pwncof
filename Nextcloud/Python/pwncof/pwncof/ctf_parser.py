__all__ = [
        'ropper_parser',
        ]

class RopperObject:
    def __init__(self, ropper_object: dict, base_address: int = 0):
        self.__dict__ = ropper_object
        self.base_address = base_address

    def by_data(self, data: str, *args, **kwargs):
        return RopperObject(ropper_parser(data), *args, **kwargs)

    def by_filename(self, filename: str, *args, **kwargs):
        return RopperObject(ropper_parser(filename), *args, **kwargs)

    def __getitem__(self, key: str):
        return self.__dict__[key] + self.base_address

def ropper_parser_by_file(filename: str):
    with open(filename, 'r') as f:
        return ropper_parser(f.read())

def ropper_parser(data: str) -> dict:
    """
    parse ropper output
    """

    ret = {}

    for elm in data.split('\n'):
        if ':' not in elm:
            continue
        
        addr, gadget = elm.split(':')

        addr = int(addr, 16)
        gadget = gadget.strip()

        ret[gadget] = addr

    return ret
