# Introduction 
This is a report curve for a possible Genesis Modding project.

The Mega Drive [has two sound chips][1] : YM2612 and SN76496. This first is based on FM synthesis and the second on square wave.
The YM has 6 FM channels and the SN 3 plus a noise channels.
Summing them all makes 10 channels to play.
The capabilities have been presented in a PhD, [check it out][13].


This arctile will present : 
- Projects dedicated to YM2612
- Porjects dedicated to create music based on this sound, embbedable on the megadrive
- Projects Modding the megadrive to make it behave as a midi controller.


# Projects dedicated to YM2612

There are many projects focusing in the YM2612 only that interface the chip with a tensy to expose it as a midi device.  
This article shows a [breadboard prototype][2] "Mega Midi", interfacing to a keyboard controller.

# Create musing on desktop only 

TODO : Delflemask and open source project : see linuxfr / SGDK (fr) article.

# Modding the megadrive to make a midi controller

There are projects with this objective, ask [Google][3].

The most noticeable is the genMDM. 
It is composed of an application embbeded in a cartridge and an PCB that interfaces the external  midi controller to the joystick port of the console.
Probalby the game application waits for command comming for the joystick port and send this to the chips.


The product is sold on [catSkull][5]. 
The project author "little- scale" has its [blog][7] and community thread on [chipmusic][8].
Note that the author also work for master system converter chip ["SMSMS"][11]


On top on this one has been created other (crazy) project : 
- "Look Mum no computer" as created a [big board][4] for a full synthetiser.
- The [GenAJam][9] which is ... I'm not commletely sure, it talks about patches and the possibility to load music files from SDcard.

Fact is that interfacing directly the genMDM with a keyboard controller will not result to very interesting sound, you will need a sequencer and that is what GenAJam is trying to do by hardware.
There are other SW solution like the [gen-mdm editor][10] released as a web browser plugin (open source).

Infortunately the genmdm is sold out and not easily found on "used" market (ebay). A guy provided a tip for ["genmdm DIY"][6].
Also there is a project for an open source alternative, the community thread is also on [chipmusic][12]. This project tries to be more versatile supporting several hardware for the ROM (everdrive, other cartridge), and the interface (serial, megawifi, ...).

# Project "roots"

This chapter is all about DIY with MIDI and understanding the standard.
It is needed if you want to hands on the project.
An intrduction to [MIDI (fr)][15].
Developping MIDI interface with the teensy : [dedicated library][16].
What is a [MIDI keyboard controller (fr)][17].




[1]: [http://www.vgmpf.com/Wiki/index.php?title=Genesis]
[2]: [https://www.aidanlawrence.com/mega-midi-a-playable-version-of-my-hardware-sega-genesis-synth/]
[3]: [https://www.google.com/search?client=firefox-b-d&q=sega+genesis+as+midi+controller]
[4]: [https://www.lookmumnocomputer.com/sega-megadrive-synth]
[5]: [https://catskullelectronics.com/products/genmdm?variant=29399089381454]
[6]: [https://www.vandoeselaar.com/tinkering/clone-yourself-a-genmdm/]
[7]: [http://little-scale.blogspot.com/search/label/genmdm%20tutorials]
[8]: [https://chipmusic.org/forums/topic/562/sega-md-gen-genmdm-sega-genesis-mega-drive-midi-interface/]
[9]: [https://www.youtube.com/watch?v=uE3FbmMKl-U]
[10]: [https://github.com/2xAA/genmdm-editor]
[11]: [https://chipmusic.org/forums/topic/9365/sega-master-system-how-to-make-a-sega-master-system-midi-interface/]
[12]: https://chipmusic.org/forums/topic/24476/open-source-mega-drive-midi-interface/
[13]: [https://digital.library.adelaide.edu.au/dspace/bitstream/2440/70888/10/Tomczak2011_PhD.pdf]
[14]: [https://www.retrorgb.com/genesistriplebypass.html]
[15]: [https://fr.audiofanzine.com/mao/editorial/dossiers/le-midi-introduction.html]
[16]: [https://www.pjrc.com/teensy/td_libs_MIDI.html]
[17]: [https://formation-clavier.com/clavier-maitre-midi-a-quoi-ca-sert/]
