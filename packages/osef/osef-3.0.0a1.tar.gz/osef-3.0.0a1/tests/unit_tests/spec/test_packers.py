"""Module to test the packers/unpackers functions."""

# Standard imports
import uuid

# Third party imports
import numpy as np

# Project imports
from osef.spec import _packers, constants
from tests import tests_base


class TestArrayPacker(tests_base.BaseTestCase):
    """Class to test the array (un)packer."""

    def test_pack_unpack(self):
        """Test the array packer/unpacker."""
        value_input = np.array([2.0, 3.0], dtype=np.float32)

        packer = _packers.ArrayPacker(np.dtype(np.float32))
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertIsNone(np.testing.assert_array_equal(value_input, unpacked))

    def test_ndarray(self):
        """Test the array packer/unpacker."""
        value_input = np.array([[2.0, 3.0]], dtype=np.float32)

        packer = _packers.ArrayPacker(np.dtype(np.float32), 2)
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertIsNone(np.testing.assert_array_equal(value_input, unpacked))

    def test_structured_array(self):
        """Test the structured array packer/unpacker."""
        dtype = np.dtype([("first_type", np.float32), ("second_type", np.float64)])
        value_input = np.array([2.0, 3.0], dtype=dtype)

        packer = _packers.StructuredArrayPacker(dtype)
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertIsNone(np.testing.assert_array_equal(value_input, unpacked))

    def test_invalid_dtype(self):
        """Test that packing an array with invalid dtype will raise."""
        value_input = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        packer = _packers.ArrayPacker(np.dtype(np.float32))

        with self.assertRaises(TypeError):
            packer.pack(value_input)

    def test_invalid_shape(self):
        """Test that packing an array with invalid shape will raise."""
        value_input = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)
        packer = _packers.ArrayPacker(np.dtype(np.float32), 2)

        with self.assertRaises(TypeError):
            packer.pack(value_input)


class TestValuePacker(tests_base.BaseTestCase):
    """Class to test the value (un)packer."""

    def test_pack_unpack(self):
        """Test the value packer/unpacker."""
        value_input: int = 10

        packer = _packers.ValuePacker("<L")
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertEqual(value_input, unpacked)


class TestBytePacker(tests_base.BaseTestCase):
    """Class to test the bytes (un)packer."""

    def test_pack_unpack(self):
        """Test the byte packer/unpacker."""
        value_input = bytes("test_bytes", encoding="utf-8")

        packer = _packers.BytesPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertEqual(unpacked, value_input)


class TestDictPacker(tests_base.BaseTestCase):
    """Class to test the dict (un)packer."""

    def test_pack_unpack(self):
        """Test the dictionary packer/unpacker."""
        value_input = {"key_1": 10.0, "key_2": 20.0}

        packer = _packers.DictPacker("<ff", list(value_input.keys()))
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.compare_dict(unpacked, value_input)


class TestTimestampPacker(tests_base.BaseTestCase):
    """Class to test the timestamp (un)packer."""

    def test_pack_unpack(self):
        """Test the timestamp packer/unpacker."""
        value_input = 1672527600.0

        packer = _packers.TimestampPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertEqual(unpacked, value_input)


class TestProcessingBitfieldPacker(tests_base.BaseTestCase):
    """Class to test the processing bitfield (un)packer."""

    def test_pack_unpack(self):
        """Test the processing bitfield packer/unpacker."""
        value_input = {constants.ExtraBackgroundKeys.DELETED: 0}

        packer = _packers.ProcessingBitfieldPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertDictEqual(unpacked, value_input)


class BoolBitfieldPacker(tests_base.BaseTestCase):
    """Class to test the processing bool bitfield (un)packer."""

    def test_pack_unpack(self):
        """Test the bool bitfield packer/unpacker."""
        value_input = np.array(
            [True, True, False, False, False, False, False, False], dtype=np.bool_
        )

        packer = _packers.BoolBitfieldPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertIsNone(np.testing.assert_array_equal(unpacked, value_input))


class StringPacker(tests_base.BaseTestCase):
    """Class to test the string (un)packer."""

    def test_pack_unpack(self):
        """Test the string packer/unpacker."""
        value_input = "input"

        packer = _packers.StringPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertEqual(unpacked, value_input)


class TestImuPacker(tests_base.BaseTestCase):
    """Class to test the IMU (un)packer."""

    def test_pack_unpack(self):
        """Test the IMU packer/unpacker."""
        value_input = {
            constants.ExtraTimestampKeys.TIMESTAMP: {
                constants.ExtraTimestampKeys.UNIX_S: 1672527600,
                constants.ExtraTimestampKeys.REMAINING_US: 0,
            },
            constants.ExtraImuKeys.ACCELERATION: (0.0, 1.0, 2.0),
            constants.ExtraImuKeys.ANGULAR_VELOCITY: (0.0, 1.0, 2.0),
        }

        packer = _packers.ImuPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertDictEqual(unpacked, value_input)


class UuidPacker(tests_base.BaseTestCase):
    """Class to test the UUID (un)packer."""

    def test_pack_unpack(self):
        """Test the UUID packer/unpacker."""
        value_input = uuid.UUID("9dfa8baa-780a-11ee-b962-0242ac120002")

        packer = _packers.UuidPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertEqual(unpacked, value_input)


class TestObjectPropertiesPacker(tests_base.BaseTestCase):
    """Class to test the (un)packers function."""

    def tes_pack_unpack(self):
        """Test the object properties packer/unpacker."""
        value_input = np.array(
            [
                [True, True, False, False, False, False, False, False],
                [True, True, True, True, False, False, False, False],
            ],
            dtype=np.bool_,
        )

        packer = _packers.ObjectPropertiesPacker()
        packed = packer.pack(value_input)
        unpacked = packer.unpack(packed)

        self.assertIsNone(np.testing.assert_array_equal(unpacked, value_input))
