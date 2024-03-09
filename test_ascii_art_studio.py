# test_ascii_art_studio.py

import unittest

from ascii_art_studio import ASCIIArtStudio, ASCIIImage
from PIL import Image as PILImage
import os
import pickle


class TestASCIIArtStudio(unittest.TestCase):

    def setUp(self):
        """Set up a test environment for each test method."""
        self.studio = ASCIIArtStudio()
        self.pickle_filename = "test_session.pkl"
        self.test_image_path = (
            "test_image.jpg"  # Ensure this is a valid image file in your test directory
        )

        # Create a simple test image
        if not os.path.exists(self.test_image_path):
            test_image = PILImage.new("RGB", (100, 100), color="red")
            test_image.save(self.test_image_path)

    def tearDown(self):
        """Clean up after each test method."""
        # Remove the test image file if it exists
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.pickle_filename):
            os.remove(self.pickle_filename)

    def test_initialization(self):
        """Test that the studio initializes correctly."""
        self.assertEqual(len(self.studio.images), 0)
        self.assertIsNone(self.studio.current_image)

    def test_add_image_to_studio(self):
        """Test adding an image to the studio."""
        self.studio.add_image_to_studio(self.test_image_path, alias="test_image")
        self.assertIn("test_image", self.studio.images)
        self.assertIsInstance(self.studio.images["test_image"], ASCIIImage)

    def test_set_image_width(self):
        """Test setting an image width."""
        self.studio.add_image_to_studio(self.test_image_path, alias="test_image")
        self.studio.set_image_width("test_image", 100)
        self.assertEqual(self.studio.images["test_image"].target_width, 100)

    def test_save_session_creates_file(self):
        """Test that save_session creates a pickle file."""
        self.studio.save_session(self.pickle_filename)
        self.assertTrue(os.path.exists(self.pickle_filename))

    def test_save_and_load_session(self):
        """Test that the state of the studio is preserved after saving and loading a session."""
        # Set up some state in the studio
        self.studio.add_image_to_studio("test_image.jpg", alias="test_image")

        # Save the studio's state
        self.studio.save_session(self.pickle_filename)

        # Load the studio's state from the pickle file
        with open(self.pickle_filename, "rb") as f:
            loaded_studio = pickle.load(f)

        # Verify that the loaded state matches the original state
        self.assertIn("test_image", loaded_studio.images)
        self.assertEqual(len(loaded_studio.images), len(self.studio.images))

    def test_set_image_height(self):
        """Test setting an image height."""
        self.studio.add_image_to_studio(self.test_image_path, alias="test_image")
        initial_height = self.studio.images["test_image"].target_height
        self.studio.set_image_height("test_image", 200)
        self.assertNotEqual(
            self.studio.images["test_image"].target_height, initial_height
        )
        self.assertEqual(self.studio.images["test_image"].target_height, 200)

    def test_set_image_brightness(self):
        """Test setting image brightness."""
        self.studio.add_image_to_studio(self.test_image_path, alias="test_image")
        initial_brightness = self.studio.images["test_image"].brightness
        self.studio.set_image_brightness("test_image", 1.5)
        self.assertNotEqual(
            self.studio.images["test_image"].brightness, initial_brightness
        )
        self.assertEqual(self.studio.images["test_image"].brightness, 1.5)

    def test_set_image_contrast(self):
        """Test setting image contrast."""

        self.studio.add_image_to_studio(self.test_image_path, alias="test_image")
        initial_contrast = self.studio.images["test_image"].contrast
        self.studio.set_image_contrast("test_image", 1.5)
        self.assertNotEqual(self.studio.images["test_image"].contrast, initial_contrast)
        self.assertEqual(self.studio.images["test_image"].contrast, 1.5)

    def test_conversion_ascii_art(self):
        """Test rendering of ASCII art."""
        try:
            original_test_ascii = [
                "@@@@@@@@@@@@@@@@@@@@%#***##%@@@@@@@@@@@@@@@@@@@@@@",
                "@@@@@@@@@@@@@@@@@@*=---=++*#@@@@@@@@@@@@@@@@@@@@@@",
                "@@@@@@@@@@@@@@@@#-..::-=++*#%@@@@@#####%%%@@@@@@@@",
                "@@@@@@@@@@@@@@@*...::--=+*#%@@@@@@@@@@@@@@@@@@@@%@",
                "@@@@@@@@@@%%##*....::-==+*#%@@@@@@@@@@@@@@@%#%%%%@",
                "@@@@@@%%#####%+..:::--=++*#%@@@@@@@@@@@@%#*##%%@@@",
                "@@@@%%####%@@@+ ..::--=+**#%@@@@@@@@%%####%%@@@@@@",
                "@@%%%#**#@@@@@#....:--=+*#%@@@@%%#####%%@@@@@@@@@@",
                "@%%%%#**##%%%%@*--==++**#########%%@@@@@@@@@@@@@@@",
                "@@@%%%%##################%%%@@@@@@@@@@@@@@@@@@@@@@",
                "@@@@@@@@@@@@@@@@@@%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
            ]
            self.studio.add_image_to_studio(
                "DO_NOT_DELETE_saturn.jpg", alias="test_image"
            )
            self.studio.render_ascii_art("test_image")
            self.assertEqual(
                self.studio.images["test_image"].ascii, original_test_ascii
            )
        except FileNotFoundError:
            print(
                "!Make sure you have the file DO_NOT_DELETE_saturn.jpg in the same folder!"
            )


if __name__ == "__main__":
    unittest.main()
