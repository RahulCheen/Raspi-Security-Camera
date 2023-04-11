# Raspi-Security-Camera
This project uses the Picamera 2 module to record video using a compatible camera. It then uses a discord bot to direct-message video clips to a specific discord user-id.

# My hardware
I am running this on a Raspberry Pi 3B+ with the "Bullseye" OS. I am using a Raspberry Pi Camera Module 3 to record video.

# motion_detector.py
This script uses the picamera2 library to examine a live video feed and identify motion based on simple frame differencing. It saves video clips using the picamera2 H264 encoder but transcodes to MP4 to allow for embedding in Discord messages for easy viewing. I also have a helper function that uses Open-CV to flip the video because I installed my camera upside-down :P

# motion_notifier.py
This script governs a simple Discord bot that periodically checks a specified directory for new files and sends them to a specified Discord user via direct message. Video files are deleted from the host's local storage as the idea here is to use Discord servers via the bot's chat message history as perpetual storage.

# Issues I am having
- My autofocus doesn't work
    I'm not sure if I have a busted camera module or if I'm doing something wrong with the autofocus. I've tried a few fixes including setting a manual focus but it doesn't seem to work.
- Motion detection threshold is not well tuned
    I haven't done a ton of testing with the motion detection threshold because it is likely subject to the video feed's focal distance.
