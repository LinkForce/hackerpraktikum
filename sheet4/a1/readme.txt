Skiddy’s First Steps (Aufgabe 1)

Unpack the APK and analyze the source code. Which (hard-coded) credentials are stored in the app?

You cant find this hard coded credentials in the application: YmFiYnlzQGZpcnN0LnJlOnBhY2thZ2VkLmFwcA==

Analyze the analysis routines that the app performs after login. The app tries to
detect repackaging, debugging, dynamic analysis and emulators. For each analysis
routine, write what value is being searched for and why.

Repackaging:

The app checks the SHA1 fingerprint of the certificate that was used to sign the app and compare its with a pre stored one. If the fingerprints
differs, it assumes that the app was repackaged using a different signing certificate.

Debugging:

The app checks for some constant UID's and if none of them matches, it checks for the FLAG_DEBUGGABLE flag. If this flag exists in the app's
infos, the application is in an debbugable enviromnment. The int value of this flag is 2, and is this int value that is used on the code.

Dynamic analysis:

To check this, the app looks into 3 system properties: ro.adb.secure, init.svc.adbd, sys.usb.config.
ro.adb.secure checks if adb debug requires authentication. init.svc.adbd checks if the the adb server is running, and sys.usb.config to check if
the adb server is configured to comunicate through USB. Using those properties, the app can detect if the adb server is running, and with that,
detect if the app is being analyzed.

Emulators:

This one checks the fingerprint of the build version that the running os has. If the build versoin contains "sdk" in it, the app assumes that
this os version was build to run inside and emulator, thus the app is running inside and emulator.

Patch the APK and repack it so that the routines never recognize anything.

The h4ckpr0NoDetection.apk does not detect any of the above point. (It atually looks for those points, but the app will never take any action
based on those analysis).
