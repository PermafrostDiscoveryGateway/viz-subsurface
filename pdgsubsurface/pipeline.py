from pathlib import Path
from typing import Union, Literal
from pyegt.defs import REGIONS
from logging import getLogger
from readgssi import readgssi

from . import utils
from . import geoid

class Pipeline():
    """
    Process GPR data to create a 3dTiles model that represents a subsurface profile.

    :param gpr_files: The GPR files to process.
    :type gpr_files: str, Path
    :param output_dir: The output directory in which to save the model.
    :type output_dir: str, Path
    """
    def __init__(self, gpr_files: Union[str, Path], output_dir: Union[str, Path]):
        self.gpr_files = gpr_files
        self.output_dir = output_dir
        self.models = []
        self.logger = getLogger(__name__)

    def process(self):
        """
        Process the GPR data to create a 3dTiles model.
        """
        # Create radar profiles
        radar_profiles = self.create_radar_profiles()
        # Extract location and depth information
        location_info = self.extract_location_info()
        depth_info = self.extract_depth_info()
        # Create models
        for radar_profile in radar_profiles:
            gltf_model = self.create_glTF_model(radar_profile, location_info, depth_info)
            self.models.append(self.create_3dtiles_model(gltf_model))
        # Save models
        self.save_models()

    def create_radar_profiles(self):
        """
        Create radar profiles for input GPR files using readgssi.

        :return: The radar profiles.
        :rtype: list of numpy.ndarray
        """
        # Use the readgssi module to create radar profiles for input GPR files
        radar_profiles = readgssi.readgssi(self.gpr_files)
        return radar_profiles

    def extract_location_info(self):
        """
        Extract location information from GPR data.

        :return: The location information.
        :rtype: dict
        """
        # Extract location information from GPR data
        location_info = utils.extract_location_info(self.gpr_files)
        return location_info

    def extract_depth_info(self):
        """
        Extract depth information from GPR data.

        :return: The depth information.
        :rtype: dict
        """
        # Extract depth information from GPR data
        depth_info = utils.extract_depth_info(self.gpr_files)
        return depth_info

    def create_glTF_model(self, radar_profiles, location_info, depth_info):
        """
        Create a glTF model using radar profiles, location array, and depth
        information.

        :param radar_profiles: The radar profiles representing subsurface conditions.
        :type radar_profiles: list
        :param location_info: The information about the location.
        :type location_info: dict
        :param depth_info: The information about the depth.
        :type depth_info: dict
        :return: The glTF model.
        :rtype: dict
        """
        # Use location information, depth information, and subsurface image data to create a glTF model
        # Paint the model with a GPR profile image that represents subsurface conditions
        # Implement the logic here
        pass

    def create_3dtiles_model(self, gltf_model):
        """
        Create a 3dTiles model using radar profiles, location array, and depth
        information.

        :param gltf_model: The radar profiles representing subsurface conditions.
        :type gltf_model: list
        :return: The 3dTiles model.
        :rtype: dict
        """
        # Use location information, depth information, and subsurface image data to create a 3dTiles model
        # Paint the model with a GPR profile image that represents subsurface conditions
        # Implement the logic here
        pass

    def save_models(self):
        """
        Save the models to the output directory.
        """
        # Save the models to the output directory
        for model in self.models:
            # Save the model to the output directory
            pass
