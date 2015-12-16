# CapstoneHAT

CaptstoneHAT is a project formed by Heath Lee(myself) Andrew Deaton and Tim Phelps for senior design at Texas A&M. The first initials forming HAT. Not to be confused 
with the generic name for projects built on top of the Raspberry Pi. Though it mostly is.

More can be found on the website - http://capstonehat.webs.com/

This project takes an existing product and makes it smart.

We began with a motion detection flood light, stripped away all of the control electronics and replaced them with a Raspberry Pi and a camera.

We used this simple Python script along with the OpenCV libraries to constantly check for motion in front of the flood light. When motion is 
detected. The flood lights are switched on, a picture is captured then sent via email alert to the owner.

