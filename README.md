# cubemap2fisheye

## Project Overview

This module transforms six input images that form a cube map into a fisheye image.

## Requirements

- Python 3
- Some external libraries must be installed in order to run the program. They can be found in the requirements.txt file

If the operating system used by the user is Windows I strongly recommend getting the most updated Anaconda distribution release. 
By default, all packages in the requirements.txt come installed except for OpenCV. It can be added to the system with the following command on the Anaconda Prompt:

	conda install -c conda-forge opencv 
	
For more information, visit the official Anaconda site: 

	https://anaconda.org/conda-forge/opencv
  
## Input files

Input images must be stored at folders "front", "right", "left", "back", "top" and "bottom" inside "input". Each image represents a face of the cube map.

Name formatting is of the type:
    '000000', '000001', ... , '000022', '000023', ... , '000138', '000139',...

If there is a sequence of images in each folder (front, right, etc.) following the above naming convention an output stream of images is generated.

There must be the same number of images in each folder. Otherwise, the script will raise an error and stop execution when it encounters the missing pictures. However, all frames before the missing one will be processed. 

## Operating instructions

Type the following command on a terminal in order to run the script (Linux)
        
		$ chmod +x converter.py
    $ python converter.py
		
Or simply type the following on the cmd if Python is already added to the PATH (Windows)
	
		$ python converter.py

## Copyright and licensing

MIT License, see LICENSE document for more information.

## Contact information

Name: Miguel Ángel Bueno Sánchez

email: miguelangelbuenos@gmail.com
