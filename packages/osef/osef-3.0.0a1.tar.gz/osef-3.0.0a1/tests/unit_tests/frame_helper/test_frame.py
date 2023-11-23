"""Test the OSEF frame helpers."""

# Third party imports
import numpy as np
from parameterized import parameterized_class

# OSEF imports
import osef
from osef.frame_helper import osef_frame
from osef.frame_helper.exceptions import FieldError
from osef.spec.osef_types import OsefKeys
from osef.spec import osef_types

# Project imports
from tests import tests_base


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestOsefFrame(tests_base.BaseTestCase):
    """Class to test the OSEF frame helper."""

    def test_timestamp(self):
        """Test timestamp helper is working."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=self.lazy)
        for frame in frame_iterator:
            osef_frame_helper = osef_frame.OsefFrame(frame)
            timestamp = frame[OsefKeys.TIMESTAMPED_DATA.value][
                OsefKeys.TIMESTAMP_MICROSECOND.value
            ]
            self.assertEqual(timestamp, osef_frame_helper.timestamp)


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestScanFrame(tests_base.BaseTestCase):
    """Class to test the OSEF Scan frame helper."""

    def test_no_scan_frame(self):
        """Test Scan frame is NOT defined."""
        frame_iterator = osef.parse(self.EDGE_FILEPATH, lazy=self.lazy)
        with self.assertRaises(FieldError):
            for frame in frame_iterator:
                osef_frame.ScanFrame(frame)

    def test_scan_frame(self):
        """Test Scan frame is defined."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        for frame in frame_iterator:
            osef_frame.ScanFrame(frame)

    def test_lidar_pose(self):
        """Test the lidar pose from the Scan frame."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=self.lazy)
        ref_pose = osef_frame.Pose(
            translation=np.array([0, 0, 0]),
            rotation=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        )

        for frame in frame_iterator:
            scan_frame = osef_frame.ScanFrame(frame)
            self.assertEqual(scan_frame.pose, ref_pose)

    def test_unable_to_get_element(self):
        """Test we can not get an element with [] operator."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        scan_frame = osef_frame.ScanFrame(next(frame_iterator))

        with self.assertRaises(KeyError):
            scan_frame[OsefKeys._HEIGHT_MAP.value]

    def test_get_element(self):
        """Test we can get an element with [] operator."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        scan_frame = osef_frame.ScanFrame(next(frame_iterator))

        ego_motion = scan_frame[OsefKeys.EGO_MOTION.value]
        self.assertIsNotNone(ego_motion)


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestAugmentedCloud(tests_base.BaseTestCase):
    """Class to test the OSEF AugmentedCloud helper."""

    def test_augmented_cloud(self):
        """Test augmented cloud is defined."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=self.lazy)
        for frame in frame_iterator:
            osef_frame.AugmentedCloud(frame)

    def test_no_augmented_cloud(self):
        """Test augmented cloud is NOT defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        with self.assertRaises(FieldError):
            for frame in frame_iterator:
                osef_frame.AugmentedCloud(frame)

    def test_aug_cloud_fields(self):
        """Test to get augmented cloud fields."""
        frame_iterator = osef.parse(self.MOBILE_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        aug_cloud = osef_frame.AugmentedCloud(frame_dict)
        self.assertIsNotNone(aug_cloud.reflectivities)
        self.assertIsNotNone(aug_cloud.object_ids)
        self.assertIsNotNone(aug_cloud._background_bits)

    def test_aug_cloud_missing_fields(self):
        """Test get None when fields are not present in the augmented cloud."""
        frame_iterator = osef.parse(self.COVARIANCES_RECORD, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        aug_cloud = osef_frame.AugmentedCloud(frame_dict)
        self.assertIsNone(aug_cloud._background_bits)
        self.assertIsNone(aug_cloud._road_markings_bits)
        self.assertIsNone(aug_cloud._ground_plane_bits)
        self.assertIsNone(aug_cloud.reference_map_bits)


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestEgoMotion(tests_base.BaseTestCase):
    """Class to test the OSEF EgoMotion helper."""

    def test_ego_motion(self):
        """Test EgoMotion is defined."""
        frame_iterator = osef.parse(self.SLAM_FILEPATH, lazy=self.lazy)
        for frame in frame_iterator:
            ego_motion = osef_frame.EgoMotion(frame)
            self.assertIsNotNone(ego_motion.pose_relative)

    def test_smoothed_pose(self):
        """Test to get the smoothed pose."""
        frame_iterator = osef.parse(self.COVARIANCES_RECORD, lazy=self.lazy)
        for frame in frame_iterator:
            ego_motion = osef_frame.EgoMotion(frame)
            self.assertIsNotNone(ego_motion.smoothed_pose)

    def test_divergence_indicator(self):
        """Test the slam divergence indicator."""
        frame_iterator = osef.parse(self.DIVERGENCE_RECORD, lazy=self.lazy)
        indicators = []
        for frame in frame_iterator:
            ego_motion = osef_frame.EgoMotion(frame)
            indicators.append(ego_motion.divergence_indicator)

        self.assertEqual(len(indicators), 74)


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestTrackedObjects(tests_base.BaseTestCase):
    """Class to test the OSEF TrackedObjects helper."""

    def test_tracked_objects(self):
        """Test tracked objects are defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        number_of_objects = []
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            number_of_objects.append(tracked_objects.number_of_objects)

        self.assertEqual(
            number_of_objects, [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        )

    def test_tracked_object_classes(self):
        """Test tracked object classes."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        last_object_classes = []
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            last_object_classes = tracked_objects.class_ids

        self.assertEqual(last_object_classes[0], osef_types.ClassId.UNKNOWN)
        self.assertEqual(tracked_objects.class_ids[0], osef_types.ClassId.UNKNOWN)
        self.assertEqual(last_object_classes[1], osef_types.ClassId.PERSON)

    def test_tracked_object_poses(self):
        """Test tracked object poses"""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(len(tracked_objects.poses), 9)
            self.assertEqual(tracked_objects.position_vectors.shape, (9, 3))

    def test_tracked_object_gps_data(self):
        """Test tracked object GPS poses and speeds"""
        frame_iterator = osef.parse(self.MOBILE_TRACKING_GPS_FILEPATH, lazy=self.lazy)
        last_object_gps_poses = []
        last_object_gps_speeds = []
        for frame in frame_iterator:
            try:
                tracked_objects = osef_frame.TrackedObjects(frame)
                last_object_gps_poses = tracked_objects.geographic_poses
                last_object_gps_speeds = tracked_objects.geographic_speeds
                if last_object_gps_poses is not None:
                    self.assertEqual(
                        len(last_object_gps_poses), len(last_object_gps_speeds)
                    )
                else:
                    self.assertIsNone(last_object_gps_speeds)
            # TODO: See why first frame does not have tracked_objects field in it
            except FieldError:
                pass

    def test_object_properties(self):
        """Test tracked object properties."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD, lazy=self.lazy)
        ref_properties = osef_frame.ObjectProperties(
            oriented=True,
            is_seen=True,
            has_valid_slam_pose=False,
            is_static=False,
        )

        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(tracked_objects.object_properties[0], ref_properties)

    def test_extract_object_cloud(self):
        """Test to extract the cloud of an object."""
        ID_TO_EXTRACT = 55168

        frame_iterator = osef.parse(self.MOBILE_TRACKING_FILEPATH, lazy=self.lazy)
        frame_dict = next(frame_iterator)
        tracked_objects = osef_frame.TrackedObjects(frame_dict)
        obj_cloud, obj_reflectivities = tracked_objects.extract_object_cloud(
            ID_TO_EXTRACT, return_reflectivities=True
        )

        aug_cloud = osef_frame.AugmentedCloud(frame_dict)
        expected_num_of_points = np.sum(aug_cloud.object_ids == ID_TO_EXTRACT)
        self.assertEqual(obj_cloud.shape[1], expected_num_of_points)
        self.assertEqual(obj_reflectivities.shape[0], expected_num_of_points)

    def test_bbox_vertices(self):
        """Test to get the bounding box vertices from the array of poses and bbox sizes."""
        test_frame_dict = {
            OsefKeys.TIMESTAMPED_DATA.value: {
                OsefKeys.TIMESTAMP_MICROSECOND.value: 0.0,
                OsefKeys.SCAN_FRAME.value: {
                    OsefKeys.TRACKED_OBJECTS.value: {
                        OsefKeys.NUMBER_OF_OBJECTS.value: 1,
                        OsefKeys.BBOX_SIZES.value: np.array(
                            [[1.0, 1.0, 1.0]], dtype=np.float32
                        ),
                        OsefKeys.POSE_ARRAY.value: np.array(
                            [
                                [
                                    1.5,
                                    1.5,
                                    0.5,
                                    1.0,
                                    0.0,
                                    0.0,
                                    0.0,
                                    1.0,
                                    0.0,
                                    0.0,
                                    0.0,
                                    1.0,
                                ]
                            ],
                            dtype=np.float32,
                        ),
                    }
                },
            }
        }
        tracked_objects = osef_frame.TrackedObjects(test_frame_dict)

        # Test the projected bbox
        expected_footprint_vertices = np.array(
            [[2.0, 2.0], [2.0, 1.0], [1.0, 1.0], [1.0, 2.0]]
        )
        np.testing.assert_array_equal(
            tracked_objects.bbox_footprint_vertices[0], expected_footprint_vertices
        )

        # Test the 3D bbox
        expected_bbox_vertices = np.array(
            [
                [2.0, 2.0, 0.0],
                [2.0, 1.0, 0.0],
                [1.0, 1.0, 0.0],
                [1.0, 2.0, 0.0],
                [2.0, 2.0, 1.0],
                [2.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
                [1.0, 2.0, 1.0],
            ]
        )
        np.testing.assert_array_equal(
            tracked_objects.bbox_vertices[0], expected_bbox_vertices
        )


@parameterized_class(
    ("lazy"),
    [
        (True,),
        (False,),
    ],
)
class TestZones(tests_base.BaseTestCase):
    """Class to test the Zones helper."""

    def test_no_zones(self):
        """Test Zones are NOT defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH, lazy=self.lazy)
        with self.assertRaises(FieldError):
            for frame in frame_iterator:
                osef_frame.Zones(frame)

    def test_zones(self):
        """Test Zones are defined."""
        frame_iterator = osef.parse(self.ZONE_3D_FILEPATH, lazy=self.lazy)
        zone_name_road1 = "road1"
        zone_name_road2 = "road2"

        for frame in frame_iterator:
            zones = osef_frame.Zones(frame)
            zone_names = [definition.name for definition in zones.definitions]
            self.assertIn(
                zone_name_road1, zone_names, f"{zone_name_road1} not in Zones def"
            )
            self.assertIn(
                zone_name_road2, zone_names, f"{zone_name_road2} not in Zones def"
            )

    def test_zone_bindings(self):
        """Test the zone bindings."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH, lazy=self.lazy)
        for frame in frame_iterator:
            zones = osef_frame.Zones(frame)
            bindings = zones.bindings
        self.assertEqual(len(bindings), 8)
