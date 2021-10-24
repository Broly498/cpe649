# cpe657
CPE-657 Software Studio

Repository Contents:
 * dependencies/sentinel2-cloud-detector/
    * This project uses the sentinel2-cloud detector software located in: https://github.com/sentinel-hub/sentinel2-cloud-detector
    * The original codebase was modified and placed in an internal repository in order to track changes that were not merged back to the mainline repository.
    * For more information relating to the sentinel2-cloud detector, refer to the documentation located in this directory.

 * examples/
    * This directory contains custom scripts that are used to generate images, encrypt images, compress images, and transmit images to an FTP server.
    * Image data files that are generated by the sentinel2-cloud detector software are temporarily stored in this directory prior to transmission.

 * docs/
    * This directory contains miscellaneous tutorials and documents relating to the project.

Shell Scripts:
 * initializeSubmodules.sh
    * Initializes all of the submodule repositories contained inside of the CPE-657 project.
 * buildAllDependencies.sh
    * Compiles all of the dependencies associated with the CPE-657 project.
 * multithreaded_test.sh
    * Runs the sentinel2-cloud detector tests that were exported using the Jupyter notebook.
    * This script spawns four tests and launches them on their own unique core.
 * killImgGenAndFtpPythonProcesses.sh
    * Kills all Python processes (The Network Encryption, Network Compression, and Network Cloud Discrimination are all Python processes).
 * runImgGenAndFtpWithPiHat.sh
    * Launches a full image generation experiment.
    * The script performs the following:
       1) Runs Network Encryption Python Script (Encrypts all image files)
       2) Runs Network Compression Python Script (Compresses all encrypted files)
       3) Runs Network Cloud Discrimination Python Script (Generates sentinel2-cloud detector image files) 
       4) Runs Pi Hat Profiler Executable (Records power measurements from the Raspberry Pi)
    * The script expects TWO COMMAND-LINE ARGUMENTS:
        * argv1 - FTP Server IP Address
        * argv2 - FTP Server Port

Supplemental Information:
 * The necessary python programs have been precompiled as executables and packaged with all necessary runtime files for your convenience.
 * This package had files that were too large for Github and so it can be accessed at the following drive link (will need to be logged in to an @uah.edu email to access): https://drive.google.com/drive/folders/1puyj_BtT5TnHnwZBFc1dmSyPdyPqO0Ku?usp=sharing 
 * An additional library was used to perform power measurements. The git repository for that is located here: https://github.com/regisin/ina219.git

## License - Copied from sentinel2-cloud-detector repository

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>
<br />
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
