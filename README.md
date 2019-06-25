# NMS Locator

NMS locator is a python application for use with the No Man's Sky video game that will log the galactic coordinates of the player to the screen and add it to the clipboard.  With a combination of mods, and ocr, this program is also able to read in data needed for mapping black holes and save them into a csv file for easy upload.
This was created to aid in the logging and cataloging of black holes as part of the Black Hole Suns project.  More info about the Black Hole Suns can be found at www.blackholesuns.com or the subreddit [/r/NMSBlackHoleSuns](www.reddit.com/r/NMSBlackHoleSuns/).

# Setup

NMS Locator needs a few things in order to properly OCR screenshots.  You can follow the steps below or view the video tutorial series at https://www.youtube.com/watch?v=X7Ylm2pQjS4&list=PLwk60iLo_lz2m-QgExqkN63PkRZVOKX_d

1. Download and install Tesseract available here:
https://github.com/UB-Mannheim/tesseract/wiki

    I used the `4.10.2019.0314` 64 bit setup but any of them should work
    
2. Download the latest zip file containing all the files needed for NMS Locator, from here: https://github.com/BradfordBach/NMSLocator/releases
    Note: Chrome will sometimes mark this zip file as unsafe/dangerous.  This is likely because Google's webcrawlers have not yet validated the download as safe as it is a new release.
3. Put the `_BHS_Helper.Rehab_Submarine.UI.pak` mod file into your mods folder for NMS and enable mods.  This mod is used to put a solid background behind the system information on the galaxy screen.
4. Open the `config.ini` file and update the following information:
    - Set `SCREENSHOT_DIRECTORY` to wherever your screenshots for NMS are automatically saved
    - Set `TESSERACT_LOC` to the exe file you installed in step 1.  This is typically in `C:\Program Files\Tesseract-OCR\tesseract.exe`
    - Set `CSV_DIRECTORY` to wherever you want the output of the CSV file to be stored.  By default this is stored in the `%APPDATA%\Local\Programs\NMS Locator` folder
    - Set `PLAY_NOTIFICATION` to `False` if you do not want sound notifications to play as data is entered and saved.  You can also replace or remove specific sounds to your liking in the sounds folder.
5. In the `resolutions.txt` file this details the area the program crops out of your screenshots, the first two numbers are your screen resolution.  Make sure that whatever resolution you play NMS at is listed in the list.  If it is not, you will need to add a line to the file in the following format:
    - `screen-width`,`screen-height`, `top x pos`, `top y pos`, `bottom x pos`, `bottom y pos`
    - The `top x pos` and the `top y pos` is the top left corner of black box surrounding the system info in the galaxy screen.
    - The `bottom x pos` and the `bottom y pos` is the bottom right corner of the black box
    - These two values will allow the crop function of the program to properly cut out only the info it needs to complete OCR making it more accurate
    - NOTE: Smaller resolutions will have more errors in the OCR process, the larger you can run the game at, the more accurate the results will be.

# How to use
#### Non-OCR
You can either execute the raw python code or download the executable found on the releases tab of this page.
When running the program it will:
  - Automatically display the latest location of the player from the latest modified No Man Sky's save file.
  - Put the galactic coordinates into your clipboard, so you can copy and paste it into the spreadsheet or website for tracking black holes.
  - Keep a running log of all solar systems you have visited which can be found in your AppData\Local\NMS Locator folder.

#### OCR
The OCR will read screenshots from your screenshot directory and pair them with your last save location and display the resulting output and when a black hole entry and exit points are both available, it will pair them up and store them in the black_holes.csv file located in the `CSV_DIRECTORY` folder explained in setup

To do this, requires a bit of a standard workflow.  Here is the optimum steps in order to get the proper entry and exit points paired correctly.
1.  Start the Locator.
2. Make sure the first time you save automatically it is in a black hole system, or a system that is already logged.
3. Take a picture of your galaxy screen, either before or after you save, it will associate the first pairing of a valid screenshot and a valid galactic address via the save file as a single "system"
4. Travel through the blackhole, you should be able to wander throughout the current system or older systems without any effect, but if you go to a new non-blackh hole system it will think you went through the blackhole.
5. Once you're at the exit system, take a screenshot of galaxy page, and save your game by landing your ship somewhere.

That's pretty much it, if you follow those steps it will then log those entry-exit system info correctly, pair them, and put them into the CSV you can upload to the black hole tracking website.
You should be able to stop the system anytime after you log a complete black hole entry and exit system and have it pick up wherever you want if you want to deviate from this, like to just do general exploring, traveling to unlogged systems via portal and saving, ect.

## Important Limitations:
- This locator will likely incorrectly label items if you are running closer to the core, since it expects the exit point of the black hole to be a non black hole system
- Likewise the locator expects each black hole entry **and exit** to be a unique universe address.  If it is already logged, it will simply ignore the address.
- The locator only stores OCR details after a full black hole exit and entry system are logged.  If you quit after running the OCR on the black hole system, that OCR data will be lost.
- OCR tools are notoriously incorrect, and while I have made some effort to make sure the readings are more accurate, in some cases it may make mistakes.  The universal address is calculated and not a part of the OCR, so it will always be correct.
- The locator is a work in progress, and there may be issues

## FAQ:
***The program immediately closes after starting***

The most likely cause of this is your screenshot directory has not been set in the config.ini.  To find out more info on your error, try running the executable in command line.

***The program crashes due to a permission error***

This can happen if you have put the program in your Program Files directory or similar place that requires advanced permissions to write to.  You can either move the location of the NMS Locator folder, or run the app as an administrator.

***Will this work on a PS4 or XBox One?***

No, this can only work on a PC for two large reasons; it needs access to the No Man's Sky save file, and it requires a mod to display a black background behind the system information.  Neither of these things are possible on consoles.



