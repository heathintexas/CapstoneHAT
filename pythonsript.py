from email import Encoders
import os

USERNAME = "capstonehat@gmail.com"
PASSWORD = "**********"

def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME, to, msg.as_string())
    server.quit()
sendMail( ["heathintexas@gmail.com"],
        "Movement Detected",
        "this is the body text of the email",
        ["test.jpg"] )
print ('email sent')



#import needed libraries
import cv2
import cv
import time

#define differential image, which takes 3 consecutive webcam captures
#and takes the absolute difference (difference in pixels) and "and's" them together bit by bit
#result each time are the pixels that have changed, effectively capturing motion
def diffImg(ta, tb, tc):
  d1 = cv2.absdiff(tc, tb)
  d2 = cv2.absdiff(tb, ta)
  return cv2.bitwise_and(d1, d2)

#camera settings
cam = cv2.VideoCapture(-1) #allows script to use camera avaliable
cam.set(3,320) #width
cam.set(4,240) #height

#create a window for diffImg to be displayed (dont really need this)
winName = "Threshold"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
#create a window to display the original image (dont need this)
winName1="Original"
cv2.namedWindow(winName1, cv2.CV_WINDOW_AUTOSIZE)

# Initialize images: images must be in grayscale in order to take binary threshold
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:
  
  #t1=t #intermediate step to keep original image
  #cv.Rectangle(cv.fromarray(t1),(106,80),(213,160),150,1,8,0) 
  cv2.imshow(winName1, t)
  differential= diffImg(t_minus,t,t_plus)#perform diffImg
  differential1=differential #intermediate step to keep original image
  cv.Rectangle(cv.fromarray(differential1),(106,80),(213,160),150,1,8,0) #create a rectangle to show the boundary of the next step
  subrec=cv.GetSubRect(cv.fromarray(differential),(80,106,80,106))#^create a sub rectangle of the array in the middle third of the image
                                                 #(left_bound,top_bound,width,height)
  cv2.imshow( winName, differential1)#show the diffImg in the window
  cv.Threshold(subrec,subrec,30,255,0)#use threshold to make it a binary image #threshold may need to be changed
  pixels=cv.CountNonZero(subrec)-108 #counts the number of white (moving) pixels 
  print "pixels in motion:", pixels #displays number of pixels in the shell

#if statement that allows the image to be saved if it is over the threshold
  if pixels>900 : 
    date_string=time.strftime("%Y-%m-%d  %H:%M") #get current time and date
    cv2.imwrite('/home/pi/Desktop/webcam/'+ date_string +'.jpg',t) #saves image t as time and date
    cv2.waitKey(5) #perform a wait so that it does not save several images

  
  
  
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)


  #kills program with 'esc' key
  key = cv2.waitKey(10)
  if key == 27:
    exit()
    break

print "Goodbye"
