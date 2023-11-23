"""Module to test the edition of OSEF frames."""

# Third-party imports
import numpy as np
from parameterized import parameterized_class

# Project imports
from osef import osef_frame, pack, parse
from osef.frame_helper import exceptions, frame_edition
from osef.spec.osef_types import OsefKeys
from tests import tests_base


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestFrameEdition(tests_base.BaseTestCase):
    """Class to test the OSEF frame helper."""

    def test_set_timestamp(self):
        """Test the setter for OSEF timestamp."""
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        timestamp_to_set: float = 100000.0

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame_dict in frame_iterator:
                frame_edition.set_timestamp(frame_dict, timestamp_to_set)
                file.write(pack(frame_dict))

        # Check that in output file, timestamp was well updated.
        frame_iterator = parse(output_file)
        for frame_dict in frame_iterator:
            osef_frame_helper = osef_frame.OsefFrame(frame_dict)
            self.assertEqual(osef_frame_helper.timestamp, timestamp_to_set)

    def test_set_augmented_cloud_field(self):
        """Test to modify the reflectivities in the augmented cloud of a frame dict."""
        frame_iterator = parse(self.SLAM_FILEPATH, lazy=self.lazy)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test_cloud_field.osef"))

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame_dict in frame_iterator:
                aug_cloud = osef_frame.AugmentedCloud(frame_dict)
                new_reflectivities = np.zeros(
                    aug_cloud.number_of_points, dtype=np.uint8
                )
                frame_edition.set_augmented_cloud_field(
                    frame_dict, OsefKeys.REFLECTIVITIES.value, new_reflectivities
                )
                file.write(pack(frame_dict))

        # Check that in output file, timestamp was well updated.
        for frame_dict in parse(output_file):
            aug_cloud = osef_frame.AugmentedCloud(frame_dict)
            np.testing.assert_array_equal(
                aug_cloud.reflectivities,
                np.zeros(aug_cloud.number_of_points, dtype=np.uint8),
            )

    def test_set_number_of_layers(self):
        """Test to set the number of layers in the augmented cloud field."""
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        aug_cloud = osef_frame.AugmentedCloud(frame_dict)
        frame_edition.set_augmented_cloud_field(
            frame_dict, OsefKeys.NUMBER_OF_LAYERS.value, 128
        )
        self.assertEqual(aug_cloud.number_of_layers, 128)

    def test_set_cloud_exception(self):
        """Test to raise an exception if the augmented_cloud field is missing"""
        frame_iterator = parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(exceptions.FieldError):
            frame_edition.set_augmented_cloud_field(
                frame_dict, OsefKeys.NUMBER_OF_LAYERS.value, 0
            )

    def test_set_number_of_points(self):
        """Test to raise an exception when setting the number of points"""
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(ValueError):
            frame_edition.set_augmented_cloud_field(
                frame_dict, OsefKeys.NUMBER_OF_POINTS.value, 100
            )

    def test_set_cloud_field_invalid_length(self):
        """Test to set a field of the augmented cloud with invalid length"""
        frame_iterator = parse(self.MOBILE_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        aug_cloud = osef_frame.AugmentedCloud(frame_dict)
        value = np.zeros(aug_cloud.number_of_points + 1, dtype=bool)
        # wrong shape
        with self.assertRaises(ValueError):
            frame_edition.set_augmented_cloud_field(
                frame_dict, OsefKeys._ROAD_MARKINGS_BITS.value, value
            )

    def test_get_missing_aug_cloud(self):
        """Test to get the augmented cloud field if it's not present in the frame dict."""
        frame_iterator = parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        aug_cloud = frame_edition._get_aug_cloud_dict(frame_dict)
        self.assertIsNone(aug_cloud)

    def test_filter_frame(self):
        """Test filtering the AugmentedCloud"""

        class _Record:
            def __init__(self, asserter, filepath, expected_fields=[]) -> None:
                self.asserter = asserter
                self.filepath = filepath
                self.expected_fields = expected_fields

            def test_filtered_fields(
                self, aug_cloud, number_of_points_before, number_of_points_after
            ):
                for expected_field in self.expected_fields:
                    self.asserter.assertGreater(
                        number_of_points_before, len(aug_cloud[expected_field.value])
                    )
                    self.asserter.assertEqual(
                        number_of_points_after, len(aug_cloud[expected_field.value])
                    )
                    if expected_field is OsefKeys.CARTESIAN_COORDINATES:
                        self.asserter.assertGreater(
                            number_of_points_before,
                            aug_cloud.cartesian_coordinates.shape[1],
                        )
                        self.asserter.assertEqual(
                            np.count_nonzero(condition),
                            aug_cloud.cartesian_coordinates.shape[1],
                        )

        for record in [
            _Record(
                self,
                self.MOBILE_TRACKING_FILEPATH,
                [
                    OsefKeys.CARTESIAN_COORDINATES,
                    OsefKeys.REFLECTIVITIES,
                    OsefKeys._BACKGROUND_BITS,
                    OsefKeys.OBJECT_ID_32_BITS,
                ],
            ),
            _Record(
                self,
                self.MOBILE_TRACKING_GPS_FILEPATH,
            ),
            _Record(
                self,
                self.MAPPING_RECORD,
                [
                    OsefKeys.REFERENCE_MAP_BITS,
                ],
            ),
        ]:
            for frame_dict in parse(record.filepath, lazy=self.lazy):
                aug_cloud = osef_frame.AugmentedCloud(frame_dict)
                number_of_points_before = aug_cloud.number_of_points
                condition = np.zeros(aug_cloud.number_of_points, dtype=bool)
                condition[::2] = True  # 1 / 2
                frame_edition.filter_cloud(frame_dict, condition)

                self.assertGreater(number_of_points_before, aug_cloud.number_of_points)
                self.assertEqual(
                    np.count_nonzero(condition), aug_cloud.number_of_points
                )
                record.test_filtered_fields(
                    aug_cloud, number_of_points_before, np.count_nonzero(condition)
                )

    def test_filter_frame_invalid_length(self):
        """Test filtering the AugmentedCloud exceptions"""
        for frame_dict in parse(self.MOBILE_TRACKING_FILEPATH, lazy=self.lazy):
            aug_cloud = osef_frame.AugmentedCloud(frame_dict)

            condition = np.zeros(aug_cloud.number_of_points + 1, dtype=bool)
            condition[::2] = True  # 1 / 2
            # wrong shape
            with self.assertRaises(ValueError):
                frame_edition.filter_cloud(frame_dict, condition)

    def test_filter_cloud_exception(self):
        """Test to raise an exception if the augmented_cloud field is missing"""
        frame_iterator = parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(exceptions.FieldError):
            frame_edition.filter_cloud(frame_dict, np.ones(100, dtype=bool))

    def test_set_objects_ids(self):
        """Test to modify the object IDs field in the frame dict.
        (This does not modify the number of objects)
        """
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        object_counts = []

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame_dict in frame_iterator:
                tracked_objects = osef_frame.TrackedObjects(frame_dict)
                object_counts.append(tracked_objects.number_of_objects)
                new_object_ids = np.arange(
                    tracked_objects.number_of_objects, dtype=np.uint32
                )
                frame_edition.set_tracked_objects_field(
                    frame_dict, OsefKeys.OBJECT_ID_32_BITS.value, new_object_ids
                )
                file.write(pack(frame_dict))

        # Check that in output file, timestamp was well updated.
        frame_iterator = parse(output_file)
        for frame_dict, object_count in zip(frame_iterator, object_counts):
            tracked_objects = osef_frame.TrackedObjects(frame_dict)
            np.testing.assert_array_equal(
                tracked_objects.object_ids, np.arange(object_count, dtype=np.int32)
            )

    def test_set_tracked_object_field_invalid_length(self):
        """Test to set a field of the tracked objects with invalid length"""
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        new_object_ids = np.arange(5, dtype=np.int32)
        with self.assertRaises(ValueError):
            frame_edition.set_tracked_objects_field(
                frame_dict, OsefKeys.OBJECT_ID_32_BITS.value, new_object_ids
            )

    def test_tracked_objects_exception(self):
        """Test to raise an exception if the tracked_objects field is missing"""
        frame_iterator = parse(self.MAPPING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(exceptions.FieldError):
            frame_edition.remove_object_binding(frame_dict, 1)

    def test_set_number_of_objects(self):
        """Test to raise an exception when setting the number of objects"""
        frame_iterator = parse(self.ITS_TRACKING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(ValueError):
            frame_edition.set_tracked_objects_field(
                frame_dict, OsefKeys.NUMBER_OF_OBJECTS.value, 20
            )

    def test_remove_object(self):
        """Test to remove an object from OSEF frame."""
        frame_iterator = parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        ID_TO_REMOVE: int = 8
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))

        # Remove one tracked object.
        with open(output_file, "wb") as file:
            for frame_dict in frame_iterator:
                tracked_objects = osef_frame.TrackedObjects(frame_dict)
                nb_objects = tracked_objects.number_of_objects
                if ID_TO_REMOVE in tracked_objects.object_ids:
                    frame_edition.remove_object(frame_dict, ID_TO_REMOVE)
                    self.assertEqual(tracked_objects.number_of_objects, nb_objects - 1)
                file.write(pack(tracked_objects._osef_frame))

        # Check we can read again the OSEF file.
        frame_iterator = parse(output_file)
        for frame_dict in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame_dict)
            self.assertFalse(ID_TO_REMOVE in tracked_objects.object_ids.tolist())

    def test_remove_duplicate_objects(self):
        """Test that a frame dict with duplicate objects will remove only the first one"""
        frame_dict = {
            OsefKeys.TIMESTAMPED_DATA.value: {
                OsefKeys.TIMESTAMP_MICROSECOND.value: 123456.789,
                OsefKeys.SCAN_FRAME.value: {
                    OsefKeys.TRACKED_OBJECTS.value: {
                        OsefKeys.NUMBER_OF_OBJECTS.value: 5,
                        OsefKeys.OBJECT_ID_32_BITS.value: np.array(
                            [1, 4, 5, 8, 4], dtype=np.uint32
                        ),
                        OsefKeys.CLASS_ID_ARRAY.value: np.array(
                            [2, 0, 0, 0, 1], dtype=np.uint32
                        ),
                    }
                },
            }
        }
        frame_edition.remove_object(frame_dict, object_id=4)
        tracked_objects = osef_frame.TrackedObjects(frame_dict)
        self.assertEqual(tracked_objects.number_of_objects, 3)

    def test_remove_object_binding(self):
        """Test removing bindings linked to an object."""
        OBJECT_ID_TO_REMOVE: int = 10

        for frame_dict in parse(self.ITS_TRACKING_RECORD, lazy=self.lazy):
            tracked_objects = osef_frame.TrackedObjects(frame_dict)
            if OBJECT_ID_TO_REMOVE in tracked_objects.object_ids:
                frame_edition.remove_object_binding(frame_dict, OBJECT_ID_TO_REMOVE)

            # Warning: Zones class does not take edition into account for now
            zones = osef_frame.Zones(frame_dict)
            for binding in zones.bindings:
                self.assertNotEqual(binding.object_id, OBJECT_ID_TO_REMOVE)

    def test_object_id_exception(self):
        """Test to raise an exception if an object ID is missing"""
        frame_iterator = parse(self.ITS_TRACKING_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        with self.assertRaises(exceptions.ObjectIdError):
            frame_edition.remove_object(frame_dict, 100)
