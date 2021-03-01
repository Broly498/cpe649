"""
Tests for cloud_detector.py module
"""
import os

import pytest
import numpy as np

from s2cloudless import S2PixelCloudDetector


def test_pixel_cloud_detector():
    data_path = os.path.join(os.path.dirname(__file__), 'TestInputs', 'input_arrays.npz')
    data = np.load(data_path)

    cloud_detector = S2PixelCloudDetector(all_bands=True)
    cloud_probs = cloud_detector.get_cloud_probability_maps(data['s2_im'])
    cloud_mask = cloud_detector.get_cloud_masks(data['s2_im'])

    assert np.allclose(cloud_probs, data['cl_probs'], atol=1e-14)
    assert np.array_equal(cloud_mask, data['cl_mask'])

    cloud_detector = S2PixelCloudDetector(all_bands=False)
    with pytest.raises(ValueError):
        cloud_detector.get_cloud_probability_maps(data['s2_im'])
