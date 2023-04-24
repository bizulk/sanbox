# Setup config 

TODO

# Prepare 

See [little-scale tutorial video](https://www.youtube.com/watch?v=1JW7flt45Q8)  
Flash the genMDM firmware**** following those [instructions][1] (if not flashed the device is seen as a teensy not genMDM).  
Flash the sega cartridge with the genMDM.bin file.  
Install LMMS.  
Plug the console to Video/Audio (either audio header or SCART with - if needed - HDMI converter**).  

# Setup

Plug the genMDM to the PC (but not MD) --> detected g-enMDM device.  
Launch the game --> hear a long sound.  
Plug the genMDM to the console PORT2 : the played sound is cut (no melody played as in the video, different firmware ?) /
	
# Play 
	
Launch LMMS (after detection, otherwise you may not see the genMDM in it)  
import midi file on one channel***  
set the track output to genMDM (click on the gear) and set "general volume" to 0 to not hear the PC output.  
Play the midi.
	
# Conclusion
	
Setup is ok, and any DAW can play a midi track to genMDM. The initialization order is very important.
I did not manage to change the sound with LMMS even using a [soundfont file][4]
With Ableton I could easily change the sound but could not import the midi file :D

TODO : 
- get last genMDM firmware : http://little-scale.blogspot.com/2014/05/genmdm-103-channel-fix.html
- try to change the sound.
- connnect AKA MKP controller for live session.
	

	
[1]: http://little-scale.blogspot.com/2013/01/how-to-update-genmdm-firmware.html

	
[4]: https://musical-artifacts.com/artifacts/2268

# Notes : 

**** USe 102 until the 103 firmware is confirmed to be the "fixed" one. http://little-scale.blogspot.com/2014/05/genmdm-103-channel-fix.html

** bitfunx/OSSC or GBS-Clike

*** if not soundfont warning pops, drap and drop a plugin instrument like "FreeBoy" to the to the "piste". Those plugins does not affect the Genesis, it is to hear locally.
