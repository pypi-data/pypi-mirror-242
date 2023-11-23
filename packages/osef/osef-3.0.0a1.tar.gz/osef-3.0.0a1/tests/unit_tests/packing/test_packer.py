"""Test packer"""

# Standard imports
import os
import tempfile

# Project imports
from osef.spec import _packers, osef_types
from osef.spec.osef_types import OsefKeys
from osef.packing import packer
from osef.parsing import osef_stream, parser
from osef.parsing._lazy_parser import _LazyDict, BinaryLeaf, _LazyList
from osef.parsing._parser_common import _TreeNode
from osef.spec import _types
from tests import tests_base


class TestPacker(tests_base.BaseTestCase):
    def test_parse_to_pack_parse(self):
        for file in self.ALL_RECORD_PATHS:
            tfile = tempfile.NamedTemporaryFile(suffix=".osef", mode="wb", delete=False)
            for frame_dict in parser.parse(file):
                # re pack and store in file
                bin_frame = packer.pack(frame_dict)
                tfile.write(bin_frame)
            tfile.close()

            with osef_stream.create_osef_stream(
                file
            ) as ref, osef_stream.create_osef_stream(tfile.name) as packed:
                ref_iterator = parser.get_tlv_iterator(ref)
                packed_iterator = parser.get_tlv_iterator(packed)
                for ref_item, packed_item in zip(ref_iterator, packed_iterator):
                    ref_idx, ref_tlv = ref_item
                    packed_idx, packed_tlv = packed_item
                    ref_tree = parser.build_tree(ref_tlv)
                    ref_frame_dict = parser.parse_to_dict(ref_tree)
                    packed_tree = parser.build_tree(packed_tlv)
                    packed_frame_dict = parser.parse_to_dict(packed_tree)
                    self.assertEqual(ref_idx, packed_idx)
                    self.compare_dict(ref_frame_dict, packed_frame_dict)
                    self.compare_dict(
                        packed_frame_dict, ref_frame_dict
                    )  # to avoid inclusion issues
                    self.assertEqual(str(ref_frame_dict), str(packed_frame_dict))
                    self._compare_trees(ref_tree, packed_tree)
                    self.assertEqual(ref_tlv, packed_tlv)

            os.unlink(tfile.name)

    def _compare_trees(self, ref_tree: _TreeNode, raw_tree: _TreeNode):
        osef_type, children, leaf_value = raw_tree
        ref_osef_type, ref_children, ref_leaf_value = ref_tree

        # Get leaf type info
        type_info = _types.get_type_info_by_id(osef_type)

        # For leaves or unknown, check values
        if isinstance(type_info.node_info, _packers.PackerBase):
            return self.assertEqual(ref_leaf_value, leaf_value)

        for ref_child, child in zip(ref_children, children):
            self._compare_trees(ref_child, child)

    def test_packer_with_lazy_unpacking(self):
        # Save up some values with classic parsing
        nb_points_list = []
        nb_layers_list = []
        nb_objects_list = []
        for frame in parser.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=False):
            nb_points_list.append(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.AUGMENTED_CLOUD.value
                ][OsefKeys.NUMBER_OF_POINTS.value]
            )
            nb_layers_list.append(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.AUGMENTED_CLOUD.value
                ][OsefKeys.NUMBER_OF_LAYERS.value]
            )
            nb_objects_list.append(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.TRACKED_OBJECTS.value
                ][OsefKeys.NUMBER_OF_OBJECTS.value]
            )

        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        timestamp_to_set: float = 100000.0

        # Open the osef again with lazy parsing, and update the timestamp
        with open(output_file, "wb") as file:
            for frame in parser.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=True):
                frame[OsefKeys.TIMESTAMPED_DATA.value][
                    OsefKeys.TIMESTAMP_MICROSECOND.value
                ] = timestamp_to_set
                file.write(packer.pack(frame))

        # Check that the timestamp is updated and that the other fields are unchanged
        for frame, nb_points, nb_layers, nb_objects in zip(
            parser.parse(output_file), nb_points_list, nb_layers_list, nb_objects_list
        ):
            self.assertEqual(
                frame[OsefKeys.TIMESTAMPED_DATA.value][
                    OsefKeys.TIMESTAMP_MICROSECOND.value
                ],
                timestamp_to_set,
            )
            self.assertEqual(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.AUGMENTED_CLOUD.value
                ][OsefKeys.NUMBER_OF_POINTS.value],
                nb_points,
            )
            self.assertEqual(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.AUGMENTED_CLOUD.value
                ][OsefKeys.NUMBER_OF_LAYERS.value],
                nb_layers,
            )
            self.assertEqual(
                frame[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.TRACKED_OBJECTS.value
                ][OsefKeys.NUMBER_OF_OBJECTS.value],
                nb_objects,
            )

    def test_unpacking_enabled(self):
        """Test the unpacking activation"""
        timestamp = 123456.123456

        packer = _packers.TimestampPacker()
        binary_value = packer.pack(timestamp)
        lazy_dict = _LazyDict(
            {
                "key": BinaryLeaf(
                    osef_types.OsefTypes.TIMESTAMP_MICROSECOND, binary_value
                )
            }
        )
        lazy_list = _LazyList(
            [BinaryLeaf(osef_types.OsefTypes.TIMESTAMP_MICROSECOND, binary_value)]
        )
        self.assertTrue(lazy_dict.unpacking)
        self.assertTrue(lazy_list.unpacking)

        value = lazy_dict["key"]
        self.assertEqual(
            value, timestamp
        )  # Assuming _parse_osef_binary converts bytes to list
        value = lazy_list[0]
        self.assertEqual(
            value, timestamp
        )  # Assuming _parse_osef_binary converts bytes to list

    def test_unpacking_disabled(self):
        """Test the get key when it is unpacking is deactivated"""
        timestamp = 123456.123456

        packer = _packers.TimestampPacker()
        binary_value = packer.pack(timestamp)
        lazy_dict = _LazyDict(
            {
                "key": BinaryLeaf(
                    osef_types.OsefTypes.TIMESTAMP_MICROSECOND, binary_value
                )
            }
        )
        lazy_list = _LazyList(
            [BinaryLeaf(osef_types.OsefTypes.TIMESTAMP_MICROSECOND, binary_value)]
        )
        lazy_dict.unpacking = False
        lazy_list.unpacking = False
        self.assertFalse(lazy_dict.unpacking)

        value = lazy_dict["key"]
        self.assertIsInstance(value, BinaryLeaf)  # Should not be unpacked

        value = lazy_list[0]
        self.assertIsInstance(value, BinaryLeaf)  # Should not be unpacked

    def test_parsing_after_lazing_packing(self):
        """Test to parse the frame data after packing it with the lazy packing."""
        osef_parser = parser.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=True)
        frame_dict = next(osef_parser)

        _ = packer.pack(frame_dict)

        self.assertTrue(
            isinstance(
                frame_dict[OsefKeys.TIMESTAMPED_DATA.value][OsefKeys.SCAN_FRAME.value][
                    OsefKeys.TRACKED_OBJECTS.value
                ][OsefKeys.NUMBER_OF_OBJECTS.value],
                int,
            )
        )
