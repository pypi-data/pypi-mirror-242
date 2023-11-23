"""Test the OSEF lazy parser."""
# Standard imports
import pathlib
import time

from osef.spec import _types

from parameterized import parameterized_class

# OSEF imports
import osef
from osef.spec.osef_types import OsefKeys
from osef.parsing import parser, osef_stream

# Project imports
from tests import tests_base


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestParser(tests_base.BaseTestCase):
    def test_parse_to_dict(self):
        with osef_stream.create_osef_stream(self.EXAMPLE_TRACKING_FILEPATH) as stream:
            tlv_iterator = parser.get_tlv_iterator(stream)
            for idx, raw_tlv in tlv_iterator:
                raw_tree = parser.build_tree(raw_tlv)
                frame_dict = parser.parse_to_dict(raw_tree)
                self._check_tracking_frame(frame_dict)

    def test_generic_parser(self):
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=self.lazy)
        for frame in frame_iterator:
            self._check_tracking_frame(frame)

    def test_parsing_pathlib(self):
        path = pathlib.Path(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in osef.parse(path, lazy=self.lazy):
            self._check_tracking_frame(frame)

    def test_realtime_parser_example(self):
        """Test parser at real frequency on example file."""
        self._test_realtime_parser(self.EXAMPLE_TRACKING_FILEPATH)

    def test_realtime_parser_slam(self):
        """Test parser at real frequency on SLAM file."""
        self._test_realtime_parser(self.SLAM_FILEPATH)

    def test_realtime_parser_passthrough(self):
        """Test parser at real frequency on passthrough file."""
        self._test_realtime_parser(self.PASSTHROUGH_FILEPATH)

    def test_realtime_parser_edge(self):
        """Test parser at real frequency on Edge file."""
        self._test_realtime_parser(self.EDGE_FILEPATH)

    def test_realtime_parser_tracking(self):
        """Test parser at real frequency on tracking file."""
        self._test_realtime_parser(self.LIGHT_TRACKING_FILEPATH)

    def test_malformed_osef(self):
        """Test case to check parsing of a malformed OSEF file (frame gets skipped).
        An OSEF is malformed when a Length inside the OSEF is incorrect.
        """
        malformed_osef = self.RESOURCES.joinpath("malformed.osef")
        malformed_frame = 20
        try:
            length = len(list(osef.parse(malformed_osef, lazy=self.lazy)))
        except parser.MalformedTlvException:
            self.fail("myFunc() raised MalformedTlvException unexpectedly!")
        self.assertEqual(malformed_frame, length)

    def _test_realtime_parser(self, osef_file: str):
        frame_iterator = osef.parse(osef_file, real_frequency=True, lazy=self.lazy)
        record_start_time, record_end_time = 0, 0
        test_start_time = time.perf_counter()
        for idx, frame in enumerate(frame_iterator):
            if idx == 0:
                record_start_time = frame[OsefKeys.TIMESTAMPED_DATA.value][
                    OsefKeys.TIMESTAMP_MICROSECOND.value
                ]
            record_end_time = frame[OsefKeys.TIMESTAMPED_DATA.value][
                OsefKeys.TIMESTAMP_MICROSECOND.value
            ]
        test_end_time = time.perf_counter()
        test_time = test_end_time - test_start_time
        record_time = record_end_time - record_start_time

        # Check that error between real-time parser processing
        # and osef recording time is under 1%
        self.assertTrue(
            abs(test_time - record_time) / record_time < 0.01,
            msg=f"Error between processing and recording is too long (test_time = {test_time}s, record_time = {record_time}s)",
        )

    def _check_tracking_frame(self, frame_dict):
        timestamp_frame_name = OsefKeys.TIMESTAMPED_DATA.value
        self.assertIn(timestamp_frame_name, frame_dict)
        scan_frame_name = OsefKeys.SCAN_FRAME.value
        self.assertIn(scan_frame_name, frame_dict[timestamp_frame_name])

        self.assertIn(
            OsefKeys.POSE.value,
            frame_dict[timestamp_frame_name][scan_frame_name],
        )
        zones_name = OsefKeys.ZONES_DEF.value
        self.assertTrue(
            isinstance(
                frame_dict[timestamp_frame_name][scan_frame_name][zones_name], list
            )
        )

    def test_parse_timestamp(self):
        """Test to parse the timestamp of a frame TLV"""
        with osef_stream.create_osef_stream(self.EXAMPLE_TRACKING_FILEPATH) as stream:
            tlv_iterator = parser.get_tlv_iterator(stream)
            first_timestamp = parser.parse_timestamp(next(tlv_iterator)[1])
            self.assertEqual(first_timestamp, 1614158552.271776)

    def test_parse_timestamp_invalid_frame(self):
        """Test to raise an error if trying to parse the timestamp of a frame that does not contain any."""
        frame_dict = {
            OsefKeys.TIMESTAMPED_DATA.value: {
                OsefKeys.SCAN_FRAME.value: {
                    OsefKeys.AUGMENTED_CLOUD.value: {OsefKeys.NUMBER_OF_POINTS.value: 0}
                }
            }
        }
        packed_frame = osef.pack(frame_dict)
        read_tlv, _ = parser._parse_tlv_from_blob(packed_frame)

        with self.assertRaises(ValueError):
            parser.parse_timestamp(read_tlv)

    def test_get_frame_timestamps(self):
        """Test to get the list of timestamps of an OSEF file"""
        timestamps = parser.get_frame_timestamps(self.EXAMPLE_TRACKING_FILEPATH)
        self.assertTrue(all(isinstance(timestamp, float) for timestamp in timestamps))
        self.assertEqual(len(timestamps), 206)

    def test_get_frame_without_timestamp(self):
        """Test to get the list of timestamps of an OSEF file in which some frames don't have any timestamp."""
        osef_without_timestamps = self.RESOURCES.joinpath(
            "frames_without_timestamp.osef"
        )
        timestamps = parser.get_frame_timestamps(osef_without_timestamps)
        self.assertEqual(len(timestamps), 5)

    def test_non_blocking_stream_not_opened(self):
        """test that non blocking reading from a closed stream yield an exception"""
        closed_stream = osef_stream.create_osef_stream(self.EXAMPLE_TRACKING_FILEPATH)
        with self.assertRaises(parser.OsefParsingException):
            parser.parse_next_frame(closed_stream, lazy=self.lazy)

    def test_non_blocking_stream_opened(self):
        """test that non blocking reading from an opened stream yield a valid frame"""
        stream = osef_stream.create_osef_stream(self.EXAMPLE_TRACKING_FILEPATH)
        stream.connect()
        res = parser.parse_next_frame(stream, lazy=self.lazy)
        self._check_tracking_frame(res)
