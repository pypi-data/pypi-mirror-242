"""Test the OSEF Object Oriented Programming classes and parsers."""
# Third party imports
import numpy as np

# OSEF imports
import osef
from osef.frame_helper import osef_frame
from osef.spec.osef_types import ClassId

# Project imports
from tests import tests_base


class TestTrackedObjectData(tests_base.BaseTestCase):
    """Class to test the TrackedObjectData class and its parsing."""

    def test_tracked_object_extraction(self):
        """Test Tracked Object extraction."""
        frame_iterator = osef.parse(self.MOBILE_TRACKING_FILEPATH)
        frame = next(frame_iterator)
        tracked_objects = osef_frame.TrackedObjects(frame)
        tracked_objects_data = tracked_objects.extract_object_data(with_properties=True)
        self.assertEqual(len(tracked_objects_data), 8)

        # References values for the first tracked object
        ref_object_id = 55168
        ref_class_id = ClassId.UNKNOWN.value
        ref_speed_vector = np.array([6.98933077e00, -9.61939144e00, 0.00000000e00])
        ref_bbox_size = np.array([1.7233735, 1.637573, 1.6436515])

        # Raw values defined as: Tx Ty Tz Vxx Vyx Vzx Vxy Vyy Vzy Vxz Vyz Vzz
        translation, rotation = osef_frame._build_pose(
            np.array(
                [
                    -1.0155731e03,
                    -8.2964972e02,
                    -9.3711734e-01,
                    0.580814,
                    -0.8140363,
                    0.0,
                    0.8140363,
                    0.580814,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                ]
            )
        )
        ref_properties = osef_frame.ObjectProperties(
            oriented=True, is_seen=True, has_valid_slam_pose=False, is_static=False
        )

        # Compare values
        test_to = tracked_objects_data[0]
        self.assertEqual(test_to.object_id, ref_object_id)
        self.assertEqual(test_to.class_id, ref_class_id)
        # Use np.allclose // assertAlmostEqual. Use default tolerances.
        self.assertTrue(
            np.allclose(
                test_to.speed_vector,
                ref_speed_vector,
            )
        )
        self.assertAlmostEqual(test_to.bbox_size[0], ref_bbox_size[0])
        self.assertAlmostEqual(test_to.bbox_size[1], ref_bbox_size[1])
        self.assertAlmostEqual(test_to.bbox_size[2], ref_bbox_size[2])
        self.assertTrue(np.allclose(test_to.translation, translation))
        self.assertTrue(
            np.allclose(
                test_to.rotation,
                rotation,
            )
        )

        self.assertEqual(test_to.properties, ref_properties)

    def test_filtered_tracked_object_extraction(self):
        """Test Tracked Object extraction with a condition."""
        frame_iterator = osef.parse(self.MOBILE_TRACKING_FILEPATH)
        frame = next(frame_iterator)
        tracked_objects = osef_frame.TrackedObjects(frame)
        mask = tracked_objects.class_ids != 0
        tracked_objects_data = tracked_objects.extract_object_data(
            condition=mask, with_properties=True
        )
        self.assertEqual(len(tracked_objects_data), 5)

    def test_vertices_extraction(self):
        """Test Vertices Extraction"""

        frame_iterator = osef.parse(self.MOBILE_TRACKING_FILEPATH)
        frame = next(frame_iterator)
        tracked_objects = osef_frame.TrackedObjects(frame)
        tracked_objects_data = tracked_objects.extract_object_data()
        test_to = tracked_objects_data[0]

        self.assertEqual(test_to.bbox_footprint_vertices.shape[0], 4)
        self.assertEqual(test_to.bbox_vertices.shape[0], 8)

    def test_geographic_poses_speeds(self):
        """Test Geographic Poses/Speeds parsing"""

        frame_iterator = osef.parse(self.MOBILE_TRACKING_GPS_FILEPATH)
        # Get a frame where there actually is some data

        _ = [next(frame_iterator) for _ in range(19)]
        frame = next(frame_iterator)
        tracked_objects = osef_frame.TrackedObjects(frame)
        tracked_objects_data = tracked_objects.extract_object_data()
        test_to = tracked_objects_data[0]

        # Values are obtained through osed-printer
        # Adapt test float tolerance accordingly
        ref_geo_pose = osef_frame.GeographicPose(51.21562748, 6.77468446, 180.09705)
        ref_geo_speed = osef_frame.GeographicSpeed(0.60068893, 65.767235)

        self.assertAlmostEqual(test_to.geographic_pose.latitude, ref_geo_pose.latitude)
        self.assertAlmostEqual(
            test_to.geographic_pose.longitude, ref_geo_pose.longitude
        )
        self.assertAlmostEqual(
            test_to.geographic_pose.heading, ref_geo_pose.heading, places=5
        )

        self.assertAlmostEqual(
            test_to.geographic_speed.heading, ref_geo_speed.heading, places=6
        )
        self.assertAlmostEqual(test_to.geographic_speed.speed, ref_geo_speed.speed)


class TestPose(tests_base.BaseTestCase):
    def test_pose_matrix(self):
        """Test to get the matrix from the translation and the rotation."""
        translation = np.array([1.0, 2.0, 3.0])
        rotation = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

        pose = osef_frame.Pose(translation, rotation)
        expected_matrix = np.array(
            [
                [1.0, 0.0, 1.0, 1.0],
                [0.0, 1.0, 0.0, 2.0],
                [0.0, 0.0, 1.0, 3.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        np.testing.assert_array_equal(pose.matrix, expected_matrix)
