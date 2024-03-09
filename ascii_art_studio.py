# Kyle Tenn
# February 25 2024
# Stockholm University
# DA2005 Programming techniques VT24

# used for image processing
from PIL import Image as PILImage, ImageEnhance

# used for saving the states of the objects to files
import pickle

# use for saving and parsing commands entered by user
import shlex

# use for error handling of the files
import os


class ASCIIArtStudio:
    """
    A class to represent an ASCII Art Studio, which manages multiple ASCII images.
    """

    def __init__(self):
        """Initialize the ASCII Art Studio with no images."""
        self.images = {}
        self.current_image = None

    def add_image_to_studio(
        self, filename, target_width=50, target_height=None, alias=None
    ):
        """
        Add an image to the studio, optionally with an alias, target width, and target height.

        Args:
            filename (str): The path to the image file.
            target_width (int, optional): The target width for the ASCII conversion. Default: 50
            target_height (int, optional): The target height for the ASCII conversion.
                If None, calculated based on aspect ratio. Defaults to None.
            alias (str, optional): An alias to refer to the image.
                If None, the filename is used. Defaults to None.
        """
        if alias:
            print(f"Attempting to add '{alias}' in ascii art studio")
            try:

                if alias in self.images:
                    print(f"Image with alias '{alias}' already exists.")
                    return
                new_image = ASCIIImage(filename, target_width, target_height, alias)
                self.images[alias] = new_image
                self.current_image = new_image
                print(f"Added: {alias}")
            except Exception as error:
                print("Please try again.")

        else:
            print(f"Attempting to add '{filename}' in ascii art studio")
            try:
                if filename in self.images:
                    print(f"Image with file name '{filename}' already exists.")
                    return
                new_image = ASCIIImage(filename, target_width)
                self.images[filename] = new_image
                self.current_image = new_image
                print(f"Added: {filename}")
            except Exception as error:
                print("Please try again.")

    def set_image_width(self, alias, new_width):
        """
        Set a new target width for an image and regenerate its ASCII art.

        Args:
            alias (str): The alias of the image to modify.
            new_width (int): The new target width for the ASCII conversion.
        """
        if alias not in self.images:
            print(f"Image with alias '{alias}' does not exist.")
            return

        image = self.images[alias]
        image.set_width(new_width)
        self.current_image = image
        print(f"Width of image '{alias}' set to {new_width}.")

    def set_image_height(self, alias, new_height):
        """
        Set a new target height for an image and regenerate its ASCII art.

        Args:
            alias (str): The alias of the image to modify.
            new_height (int): The new target height for the ASCII conversion.
        """
        if alias not in self.images:
            print(f"Image with alias '{alias}' does not exist.")
            return

        image = self.images[alias]
        image.set_height(new_height)
        self.current_image = image
        print(f"Height of image '{alias}' set to {new_height}.")

    def set_image_brightness(self, alias, new_brightness):
        """
        Set a new brightness level for an image.

        Args:
            alias (str): The alias of the image to modify.
            new_brightness (float): The new brightness level. Must be a positive number.
        """
        if alias not in self.images:
            print(f"Image with name '{alias}' does not exist.")
            return

        image = self.images[alias]
        image.set_brightness(new_brightness)
        self.current_image = image
        print(f"'{alias}' set to {new_brightness}.")

    def set_image_contrast(self, alias, new_contrast):
        """
        Set a new contrast level for an image.

        Args:
            alias (str): The alias of the image to modify.
            new_contrast (float): The new contrast level. Must be a positive number.
        """
        if alias not in self.images:
            print(f"Image with name '{alias}' does not exist.")
            return

        image = self.images[alias]
        image.set_contrast(new_contrast)
        self.current_image = image
        print(f"'{alias}' set to {new_contrast}.")

    def list_images_info(self):
        """Print information about all images in the studio, including the current image."""
        print("=== Current session ===")
        if self.current_image:
            print(f"Current Image:\n{self.current_image}\n")
        else:
            print("No Images Loaded")
        print("ALL IMAGES:")
        for item in self.images.values():
            print(item)

    def render_ascii_art(self, name):
        """
        Render the ASCII art of the specified image or the current image.

        Args:
            alias (str, optional): The alias of the image to render.
                If None, renders the current image. Defaults to None.
        """
        if name and name in self.images:
            img_obj = self.images[name]
        # elif filename and filename in self.images:
        #   img_obj = self.images[filename]
        elif self.current_image:
            img_obj = self.current_image
        else:
            print("No current image selected.")
            return
        self.current_image = img_obj
        img_obj.render()

    def save_session(self, pickle_name):
        """
        Save the current session to a file.

        Args:
            pickle_name (str): The name of the file to save the session to.
        """
        with open(pickle_name, "wb") as f:
            pickle.dump(self, f)
        print(f"Session saved as {pickle_name}")

    def load_session(self, filename):
        """
        Load a session from a file.

        Args:
            filename (str): The name of the file to load the session from.
        """
        with open(filename, "rb") as f:
            studio = pickle.load(f)
        self.__dict__.update(studio.__dict__)

        print(f"Session loaded from {filename}")


class ASCIIImage:
    """
    A class to represent an ASCII image, including its original image,
    ASCII conversion, and properties like size, or brightness, and contrast.
    """

    def __init__(self, filename, target_width=50, target_height=None, alias=None):
        """
        Initialize an ASCII image with a file, target dimensions, and optional alias.

        Args:
            filename (str): The path to the image file.
            target_width (int, optional): The target width for the ASCII conversion. Default: 50
            target_height (int, optional): The target height for the ASCII conversion.
                If None, calculated based on aspect ratio. Defaults to None.
            alias (str, optional): An alias to refer to the image. Defaults to None.
        """
        self.filename = filename
        self.alias = alias
        self.target_width = target_width
        self.target_height = target_height
        self.image = self.load_image()
        self.ascii = self.convert_to_ascii()

        self.brightness = 1.0
        self.contrast = 1.0

    def load_image(self):
        """Load the image from the file so that we can convert it to grayscale."""
        try:
            with PILImage.open(self.filename) as im:
                return im.convert("L")
        except FileNotFoundError as e:
            print(f"Image file {self.filename} not found.")
            files = [f for f in os.listdir(".") if os.path.isfile(f)]
            print("These are the files in your directory:")
            formatted_file_names = ", ".join(files)
            print(f"{formatted_file_names}")
            raise e
        except Exception as e:
            print(
                f"Failed to load image {self.filename}: {e}. Ensure it was a .JPG or .PNG files."
            )
            raise e

    def convert_to_ascii(self):
        """Convert the loaded image to ASCII art based on current settings."""
        if not self.image:
            return []
        out = []
        replacement_chars = " .:-=+*#%@"[::-1]
        num_chars = len(replacement_chars)

        # Correction factor to account for the narrow width of characters
        correction_factor = 0.6

        width, height = self.image.size
        aspect_ratio = height / width

        if self.target_height is None:
            self.target_height = round(
                self.target_width * aspect_ratio * correction_factor
            )

        elif self.target_width is None:
            self.target_width = round(self.target_height / aspect_ratio)

        resized_image = self.image.resize(
            (int(self.target_width), int(self.target_height))
        )

        print("Size of image:", resized_image.size)

        for y in range(self.target_height):
            line = "".join(
                replacement_chars[
                    min(
                        int(resized_image.getpixel((x, y)) / 255 * num_chars),
                        num_chars - 1,
                    )
                ]
                for x in range(self.target_width)
            )

            # line = line + "|" used for debgunggig the actual width of the ascii render

            out.append(line)

        return out

    def set_width(self, new_width):
        """
        Set a new target width for the ASCII conversion and regenerate the ASCII art.

        Args:
            new_width (int): The new target width.
        """
        width, height = self.image.size
        aspect_ratio = height / width
        correction_factor = 0.6

        self.target_width = new_width
        self.target_height = round(aspect_ratio * new_width * correction_factor)

    def set_height(self, new_height):
        """
        Set a new target height for the ASCII conversion and regenerate the ASCII art.

        Args:
            new_height (int): The new target height.
        """
        width, height = self.image.size
        aspect_ratio = height / width
        correction_factor = 0.6

        self.target_height = new_height
        self.target_width = round(new_height / aspect_ratio / correction_factor)

    def set_brightness(self, new_brightness_level):
        """
        Set a new brightness level for the image.

        Args:
            new_brightness_level (float): The new brightness level. Must be a positive number.
        """
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(new_brightness_level)
        self.brightness = new_brightness_level

    def set_contrast(self, new_contrast_level):
        """
        Set a new contrast level for the image.

        Args:
            new_contrast_level (float): The new contrast level. Must be a positive number.
        """
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(new_contrast_level)
        self.contrast = new_contrast_level

    def __str__(self):
        """Return a string representation of the ASCII image, including its properties."""
        return (
            f"Filename: {self.filename}\n"
            f"Alias: {self.alias}\n"
            f"Original Size: {self.image.size}\n"
            f"Brightness: {self.brightness}\n"
            f"Contrast: {self.contrast}\n"
            f"Filename: {self.filename}\n"
            f"Target Width: {self.target_width}\n"
            f"Target Height: {self.target_height}\n"
        )

    def render(self):
        """Print the ASCII art of the image."""
        self.ascii = self.convert_to_ascii()
        print("\n".join(self.ascii))


class ImageAdjustment:
    def __init__(self, image):
        self.image = image

    def apply_enhancement(self, enhancer_class, factor):
        enhancer = enhancer_class(self.image)
        self.image = enhancer.enhance(factor)
        return self.image


class CommandHandler:
    def __init__(self, studio):
        self.studio = studio
        self.commands = {
            "load": self.load,
            "save": self.save,
            "info": self.studio.list_images_info,
            "render": self.render,
            "set": self.set_image_property,
            "help": self.show_help,
            "quit": self.quit,
        }

    def load(self, args):
        if args[0] == "image":
            filename = args[1]
            alias = None
            if len(args) > 3 and args[2] == "as":
                alias = args[3]
            self.studio.add_image_to_studio(filename, alias=alias)
        elif len(args) == 1:
            print(args[0])
            filename = args[0]
            self.studio.add_image_to_studio(filename)
        elif args[0] == "session":
            self.studio.load_session(args[1])
        else:
            print("Invalid load command. Use 'help' for more information.")

    def save(self, args):
        if args[0] == "session":
            self.studio.save_session(args[1])
        else:
            print("Invalid save command. Use 'help' for more information.")

    def list_images_info(self):
        self.studio.list_images_info(self)

    def render(self, args):
        if len(args) == 0:
            self.studio.render_ascii_art(None)
        else:
            self.studio.render_ascii_art(args[0])

    def show_help(self, args=None):
        print(
            """Help Commands: \n
1. load – load has two sub commands
    1a. load image – you can load an image file into the studio with this command
    e.g. load image stadshuset.jpg as hus or load stadshuset.jpg
    1b. load session - you can load a saved ASCII studio session
    e.g. load session s1
2. save - saves a sesion so that you can modify and render your images
    e.g. save session as s1
3. info - Prints the current loaded image and all images.
    e.g. info
4. render - Prints the current loaded image an an ASCII drawing
5. set - used to modify the images in the ASCII studio
    5a. set image height number
    5b. set image width number
    5c. set image brightness number
    5d. set image contrast number
6. help
7. quit
                          """
        )

    def quit(self, args=None):
        print("Exiting ASCII Art Studio.")
        exit()

    def set_image_property(self, args):
        if len(args) < 3:
            print("Insufficient arguments for 'set' command.")
            return
        alias = args[0]
        property_name = args[1]
        value = args[2]

        property_setters = {
            "width": self.studio.set_image_width,
            "height": self.studio.set_image_height,
            "brightness": self.studio.set_image_brightness,
            "contrast": self.studio.set_image_contrast,
        }

        if property_name in property_setters:
            try:
                if property_name in ["width", "height"]:
                    value = int(value)
                elif property_name in ["brightness", "contrast"]:
                    value = float(value)
                property_setters[property_name](alias, value)
            except ValueError:
                print(f"Invalid value for {property_name}.")
        else:
            print(f"Unknown property: {property_name}")

    def process_command(self, command_input):
        command_args = shlex.split(command_input)
        if not command_args:
            return
        command = command_args[0].lower()
        args = command_args[1:]

        if command in self.commands:
            try:
                self.commands[command](args)
            except Exception as e:
                print(f"Error executing {command}: {e}")
        else:
            print("Unknown command. Type 'help' for a list of commands.")


class Main:
    def __init__(self):
        """Initialize the Main class with a new ASCIIArtStudio instance and a command handler."""
        self.studio = ASCIIArtStudio()
        self.command_handler = CommandHandler(self.studio)

    def run(self):
        """Run the main loop of the ASCII Art Studio application, accepting and processing user commands."""
        print("Welcome to ASCII Art Studio!")
        while True:
            command_input = input("AAS Command Input: ")
            self.command_handler.process_command(command_input)


if __name__ == "__main__":
    main = Main()
    main.run()
