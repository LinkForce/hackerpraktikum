A11y & Overlays (Aufgabe 4)

About the malware disguise:

The malware pretends to be a "Volume Booster", and use this to lure the user through clickjacking to activate a Acessibility Service, and from 
that we can enable every permission needed for the malware to operate.

About the malware target device:

I tested the malware on an emulator running Android Marshmallow 6.0 (API 23) with a 4.65" 720x1280 xhdpi screen (Galaxy Nexus default 
configuration from Android Studio). The app is suposed to work on any device screen, but I'm including the infos here just in case 
some part of my UI is not aligned. I also included an apk version with transparency on the clickjacking UI, if you would like to see how my
UI covers the accessibility configurations to trick the user into thinking he is configuring the app.

The virtual machine I tested already had 2 other accessibility services preinstalled, so my app assumes that his accessibility service will be 
the third on the list. I made this static, but I supose I could make this dynamic by quering the system about how many accessibility services are
present in the device and positioning the button accordingly.

About the accessibility service:

The accessibility service is named "Google Accessibility" and has a Google logo to pretend it's not harmful. The accessibility service does not
 have any functionality implemented, it just toasts a message to notify that it is active, so the 2 suggested improvements are not implemented.

About permissions:

The overlays are building using the TYPE_SYSTEM_ALERT overlays, so it requires ACTION_MANAGE_OVERLAY_PERMISSION. The app checks for it on the 
onCreate method of the MainActivity. If the app does not have the permission, it just asks for it. So, if the app asks for the permission, enable
it and close the app and run it again to start the clickjacking part, because the crucial code runs on the onCreate method. If the permission is
already enabled for the app prior to running (as stated in the assignment paper), it will go directly to the overlays.

Source Code: 

The source code is included in VolumeBooster.tar.gz (user version, not the translucent one). You can check the code and the comments to see how
I structured the overlays.
