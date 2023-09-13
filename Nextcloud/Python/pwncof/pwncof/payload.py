import struct
import unittest

class PayloadUnBuilt:
    def __init__(self, payload):
        self.payload = payload


class PayloadBuilder:
    def __init__(self):
        self.payloads = []

    def append(self, payload):
        self.payloads.append(payload)

    def append_unsize(self, payload):
        self.payloads.append(PayloadUnBuilt(payload))

    def build(self, size=None):
        first = b""
        latter = b""
        unbuilt = None

        for pelem in self.payloads:
            if isinstance(pelem, bytes):
                if unbuilt == None:
                    first += pelem
                else:
                    latter += pelem
            elif isinstance(pelem, PayloadUnBuilt):
                unbuilt = pelem
                if not isinstance(pelem.payload, bytes):
                    raise TypeError(
                        "unexpected nobuilt payload type: {}".format(pelem.payload)
                    )
            else:
                raise TypeError("unexpected element type: {}".format(pelem))

        if unbuilt == None:
            return first

        if size == None:
            raise ValueError("size is None")

        l = len(first) + len(latter)
        unbuilt_size = size - l

        if unbuilt_size % len(unbuilt.payload) != 0:
            print("Warning. The length of unbuilt payload is not fit.")

        first += unbuilt.payload * int(unbuilt_size / len(unbuilt.payload))
        first += unbuilt.payload[0 : unbuilt_size % len(unbuilt.payload)]
        first += latter

        self.payloads = [first]

        return first


class PayloadBuilderTest(unittest.TestCase):
    def test_nobuild(self):
        pb = PayloadBuilder()
        pb.append(b"test_payload")

        p = pb.build()

        self.assertEqual(p, b"test_payload")

    def test_built(self):
        pb = PayloadBuilder()
        pb.append(b"first")
        pb.append(b"second")
        pb.append(b"third")

        p = pb.build()

        self.assertEqual(p, b"firstsecondthird")

    def test_build_with_size(self):
        pb = PayloadBuilder()
        pb.append(b"first")
        pb.append_unsize(b"u")
        pb.append(b"third")

        p = pb.build(size=16)

        self.assertEqual(p, b"firstuuuuuuthird")

    def test_build_with_size2(self):
        pb = PayloadBuilder()
        pb.append(b"first")
        pb.append_unsize(b"rr")
        pb.append(b"third")

        p = pb.build(size=16)

        self.assertEqual(p, b"firstrrrrrrthird")

    def test_nobytelike_object_error(self):
        pb = PayloadBuilder()
        pb.append(123)

        with self.assertRaises(TypeError):
            pb.build()

    def test_build_error(self):
        pb = PayloadBuilder()
        pb.append(b"first")
        pb.append_unsize(b"s")
        pb.append(b"third")

        with self.assertRaises(ValueError):  # size is None
            pb.build()

    def test_nobytelike_unbuilt_error(self):
        pb = PayloadBuilder()
        pb.append_unsize("t")

        with self.assertRaises(TypeError):
            pb.build(size=16)

    def test_case_unbuilt_only(self):
        pb = PayloadBuilder()
        pb.append_unsize(b"u")

        p = pb.build(size=10)
        self.assertEqual(p, b"u" * 10)

    def test_tmp_build(self):
        pb = PayloadBuilder()
        pb.append(b"1")
        pb.append_unsize(b"aa")
        pb.append(b"2")

        l = len(pb.build(size=6))

        pb.append(b"3")
        pb.append_unsize(b"bbb")
        pb.append(b"4")

        pay = pb.build(size=l + 8)

        self.assertEqual(pay, b"1aaaa23bbbbbb4")

if __name__ == "__main__":
    unittest.main()
