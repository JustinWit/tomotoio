# Description

Project files for the UIST Student Innovation Contest 2021

Abstract:
Games provide an interesting platform to test robot interaction capabilities for task automation. For our project, we will use toio robots to act as the dealer in blackjack. Implementation includes programming the robots and designing attachment mechanisms (e.g. Legos, 3D-printed parts) to accomplish required tasks such as drawing the top card off the deck, dealing cards to players, and flipping cards over when necessary. Robots will coordinate with each other and rely on user interaction via sound or gesture recognition (e.g. "hit", "stand"). Our goal is to create smooth and natural gameplay while highlighting the potential of toio robots.

Preview Link: https://www.youtube.com/watch?v=85TVs3F-DmM&list=PLqhXYFYmZ-Vdt6Y1WSItsFrE4W7HGrPP7&index=8

This runs on Linux with Python 3.6 or later.

# Usage Notes

1. Power on your Toio cubes, and run `./scan-cubes.sh`. It will scan the cubes and create `toio-cubes.txt` that includes their MAC addresses. Note that the scanning requires the root privilege and you may be asked the `sudo` password.
2. blackjack3.py was the working code file used during the conference.
