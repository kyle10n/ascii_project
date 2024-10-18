# Introduction to ASCII Walkthrough

## How the program is started and used.

To start the program, type the following command in your terminal when in the program's directory:
>pip3 install PIL

>python3 ascii_art_studio.py

If successful, you will be greeted with these prompts:

>Welcome to ASCII Art Studio!

>AAS Command Input:

As the user, you can input commands. If you are unsure what to input, type help when prompted and hit enter:
>AAS Command Input: help

This will display:

Help Commands:
1. load – load has two sub commands

	1a. load image – you can load an image file into the studio with this command

	e.g. load image stadshuset.jpg as hus or load stadshuset.jpg

[...cut for brevity]

Or you can simply get going with commands like:

>load image slalom.jpg as slalom

>load image stadshuset.jpg as hus

>render

>set slalom width 100

>render slalom

>set hus width 200

>render hus

Issues: Testing

I dont know how to write better unit tests...and I don't know how to actually test that the image matches the rendering.


# Reflections on Code Quality

Code design

I used object orientation to create three modules:

1. CommandHandler
This class handles all user input and controls how the Studio works through an interactive prompt.

2. ASCII Image
This class handles how the image is modified, manipulated, and stored, with the PIL library playing a crucial role.

3. ASCII Studio
This class stores images and creates an object that is easy to save and load as a pickle file.

The way I handled the input from the user through a while True loop to allow for user commands, was a user friendly way, but I would have preferred to make it all command line based. Then I could have used arg parse or extended the use of shlex to take multiple commands to simplify the main() function.

Which algorithms are used and why?

I used algorithmic thinking and came up with three key ideas. First, I would need characters that would represent a very light pixel to a spectrum of characters that would represent a very dark pixel. I would also need to get the brightness of each exact pixel. And lastly, I would need to, for each pixel across an image, use that pixel and match the brightness with a specific character. This algorithmic thinking led me to writing the convert_to_ascii() function. Where the exact steps and algorithm is written in code. This thinking is also reflected in the code design explained above. Where those ideas became three modules of code. However, in trying to keep the aspect ratio I used the font faces: Menlo with a 0.6 correction factor.

Which data structures are used and why?

I use the main python data structures such as dictionaries, lists, integers, strings, floats, tuples and so on in python. The reasons for using those are basic data storage and manipulation. However, the two data structures or custom classes that I create and instantiate, the studio, and images are more nuanced. I structured the studio with the important attribute of a dictionary which stores the images.
