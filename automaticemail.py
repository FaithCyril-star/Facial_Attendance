# Import the following module
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import time

# initialize connection to our
# email server, we will use gmail here
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

# Login with your email and password
smtp.login('your email here', 'device password here')
##get an app password from your google account after enabling two-factor verification


# send our email message 'msg' to our boss
def message(subject,
			text, img,
			attachment):
	
	# build message contents
	msg = MIMEMultipart()
	
	# Add Subject
	msg['Subject'] = subject
	
	# Add text contents
	msg.attach(MIMEText(text))

	# Check if we have anything
	# given in the img parameter
	if img is not None:
		
		# Check whether we have the lists of images or not!
		if type(img) is not list:
			
			# if it isn't a list, make it one
			img = [img]

		# Now iterate through our list
		for one_img in img:
			
			# read the image binary data
			img_data = open(one_img, 'rb').read()
			# Attach the image data to MIMEMultipart
			# using MIMEImage, we add the given filename use os.basename
			msg.attach(MIMEImage(img_data,
								name=os.path.basename(one_img)))

	# We do the same for
	# attachments as we did for images
	if attachment is not None:
		
		# Check whether we have the
		# lists of attachments or not!
		if type(attachment) is not list:
			
			# if it isn't a list, make it one
			attachment = [attachment]

		for one_attachment in attachment:

			with open(one_attachment, 'rb') as f:
				
				# Read in the attachment
				# using MIMEApplication
				file = MIMEApplication(
					f.read(),
					name=os.path.basename(one_attachment)
				)
			file['Content-Disposition'] = f'attachment;\
			filename="{os.path.basename(one_attachment)}"'
			
			# At last, Add the attachment to our message object
			msg.attach(file)
	return msg


# Call the message function
msg = message("Attendance Notification", f"Hello Mr Faith, \n\n Please find attached the attendance for Calculus class on {time.asctime( time.localtime(time.time()) )[:10]} 2022.\n Thank you!",
			r"C:\Users\Owner\Downloads\FIE_Files\Acity.jpg",
			r"C:\Users\Owner\Downloads\FIE_Files\Attendance Sheet.csv")

# Make a list of emails, where you wanna send mail
to = ["your email"]

# Provide some data to the sendmail function!
smtp.sendmail(from_addr="your email",
			to_addrs=to, msg=msg.as_string())

# Finally, don't forget to close the connection
smtp.quit()
