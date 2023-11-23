"""Unit testing on OSEF types."""

# Standard imports
from typing import get_type_hints
import hashlib
import numpy as np

# Project imports
import osef
from osef.spec import _types, osef_types
from tests import tests_base

# Constants
# Define black-listed OSEF types (types with no packer that we do not want to test).
BLACK_LISTED_OSEF_TYPES = [
    osef_types.OsefTypes._INTERACTIVE_REQUEST,
    osef_types.OsefTypes._INTERACTIVE_RESPONSE,
    osef_types.OsefTypes._INTERACTIVE_REQUEST_ID,
    osef_types.OsefTypes._INTERACTIVE_REQUEST_BACKGROUND_HEADER,
    osef_types.OsefTypes._INTERACTIVE_RESPONSE_BACKGROUND_HEADER,
    osef_types.OsefTypes._INTERACTIVE_REQUEST_BACKGROUND_DATA,
    osef_types.OsefTypes._INTERACTIVE_RESPONSE_BACKGROUND_DATA,
    osef_types.OsefTypes._INTERACTIVE_REQUEST_PINGPONG,
    osef_types.OsefTypes._INTERACTIVE_RESPONSE_PINGPONG,
]


class TestTypes(tests_base.BaseTestCase):
    def test_object_properties_parsing(self):
        for frame in osef.parse(self.LIGHT_TRACKING_FILEPATH):
            object_properties = frame["timestamped_data"]["scan_frame"][
                "tracked_objects"
            ]["object_properties"]

            self.assertIsNotNone(object_properties)
            self.assertTrue(np.issubdtype(np.bool_, (object_properties[0].dtype)))

    def test_bitfield_parsing(self):
        for frame in osef.parse(self.MOBILE_TRACKING_FILEPATH):
            bg_bits = frame["timestamped_data"]["scan_frame"]["augmented_cloud"][
                "background_bits"
            ]
            EXPECTED_HASH = "03e0a9453d8da0fe90bc603bde0d4dcc"
            self.assertEqual(EXPECTED_HASH, hashlib.md5(bg_bits.tobytes()).hexdigest())

    def test_parsed_types(self):
        for file_path in self.ALL_RECORD_PATHS:
            frame_iterator = osef.parse(file_path)
            for frame in frame_iterator:
                self._check_node_type(frame)

    def _check_node_type(self, node: dict):
        for key, value in node.items():
            type_info = _types.get_type_info_by_key(key)
            if isinstance(type_info.node_info, _types.InternalNodeInfo):
                if type_info.node_info.node_type == list:
                    for item in value:
                        self._check_node_type(item)
                else:
                    self._check_node_type(value)
            else:
                unpack_function = type_info.node_info.unpack
                hints = get_type_hints(unpack_function)["return"]

                self.assertIsNotNone(
                    unpack_function, msg=f"No parsing function for {key}"
                )
                self.assertIn(
                    "return",
                    get_type_hints(unpack_function),
                    msg=f"No return type specified for {unpack_function}",
                )

                # HACK: Use the origin for checking numpy type.
                # PEP646: https://peps.python.org/pep-0646/
                # https://stackoverflow.com/a/66657424
                # Using numpy class typing return is only available from python 3.11.
                # def func() -> np.ndarray[dtype]
                if hasattr(hints, "__origin__"):
                    self.assertIsInstance(
                        value,
                        hints.__origin__,
                        msg=f"for key `{key}`",
                    )
                else:
                    self.assertIsInstance(
                        value,
                        get_type_hints(unpack_function)["return"],
                        msg=f"for key `{key}`",
                    )

    def test_public_osef_types(self):
        """Test the OSEF types parser are all defined according to the public OSEF types deployed."""
        for type in osef_types.OsefTypes:
            if type in BLACK_LISTED_OSEF_TYPES:
                continue
            self.assertTrue(
                type.value in _types.outsight_types.keys(),
                f"{type.name} not defined in Outsight types",
            )
