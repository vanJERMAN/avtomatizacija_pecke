import utime
import mcron
import mcron.decorators
import os
import umail
import time
from machine import Pin
from machine import I2C
import vl53l0x

print("Zaženjam skripto procenti.py")

interval = 1800
distance_list = []
max_distance=37
try_number = 0
anti_email = 0
empty_container = 0
sender_email = "HERE GOES SENDER EMAIL"
sender_password = "HERE GOES SENDER PASSWORD"
receiver = ["HERE GOES FIRST (main) RECEIVER EMAIL", "HERE GOES SECOND RECEIVER EMAIL"]

try:
	def sensor(callback_id, current_time, callback_memory):
		global try_number
		global empty_container
		global anti_email

		calculate()
		distance_avg = sum(distance_list) / 10
		percentage=procenti(distance_avg)

		if try_number == 0 and empty_container == 0:
			if percentage <= 3:
				print("Prenizka razdalja: {}% / {}cm".format(percentage, distance_avg))
				try_number += 1
				mail("prva NAPAKA V MERITVI: {}%".format(100-percentage), distance_avg, receiver[0])
			elif percentage > 3 and percentage < 90:
				print("Razdalja: {}% / {}cm".format(percentage, distance_avg))
			elif percentage >= 90 and percentage < 95:
				try_number += 1
				print("Razdalja: {}% / {}cm".format(percentage, distance_avg))
				mail("PEČKA JE SKORAJ PRAZNA: {}%".format(100-percentage), distance_avg, receiver)
			elif percentage >= 95 and percentage <= 100:
				empty_container += 1
				mail("PEČKA JE PRAZNA: {}%".format(100-percentage), distance_avg, receiver)
			elif percentage > 100 and percentage <= 110:
				empty_container += 1
				mail("PEČKA JE PRAZNA: 100%", distance_avg, receiver)
			elif percentage > 110:
				try_number += 1
				print("Sedaj je previsoka razdalja: {}% / {}cm".format(percentage, distance_avg))
				mail("prva NAPAKA V MERITVI: {}%".format(100-percentage), distance_avg, receiver[0])
			else:
				print("Nekai je narobe pri procentih, try_number == 0")
				mail("Nekai je narobe pri: if try_number == 1:", distance_avg, receiver[0])

		elif try_number == 1 and anti_email == 0 and empty_container == 0:
			if percentage <= 3:
				print("Ponovno prenizka razdalja: {}% / {}cm".format(percentage, distance_avg))
				mail("PONOVNO NAPAKA V MERITVI: {}%".format(100-percentage), distance_avg, receiver[0])
				anti_email += 1
			elif percentage > 3 and percentage < 90:
				print("Razdalja: {}% / {}cm".format(percentage, distance_avg))
				try_number=0
			elif percentage >= 90 and percentage < 95:
				print("Razdalja: {}% / {}cm".format(percentage, distance_avg))
			elif percentage >= 95 and percentage <= 100:
				empty_container += 1
				try_number=0
				mail("PEČKA JE PRAZNA: {}%".format(100-percentage), distance_avg, receiver)
			elif percentage > 100 and percentage <= 110:
				empty_container += 1
				try_number=0
				mail("PEČKA JE PRAZNA: 100%", distance_avg, receiver)
			elif percentage > 110:
				print("Sedaj je previsoka razdalja: {}% / {}cm".format(percentage, distance_avg))
				mail("PONOVNO NAPAKA V MERITVI: {}%".format(100-percentage), distance_avg, receiver[0])
				anti_email += 1
			else:
				print("Nekai je narobe pri: if try_number == 1:")
				mail("Nekai je narobe pri: if try_number == 1:", distance_avg, receiver[0])
				anti_email += 1
		elif try_number == 1 and anti_email == 1 and empty_container == 0:
			if percentage > 3 and percentage <= 110:
				print("Ponovno pravilno izmerilo")
				mail("PRAVILNO IZMERILO: {}%".format(100-percentage), distance_avg, receiver[0])
				try_number = 0
				anti_email = 0
			else:
				mail("+3x NAPAKA V MERITVI: {}%".format(100-percentage), distance_avg, receiver[0])
				print(percentage)
				print(distance_avg)
		elif empty_container == 1:
			if percentage > 3 and percentage < 90:
				empty_container = 0
				print("Hvala da si nafilal pelete")

		distance_list.clear()




	def calculate():
		try:
			i2c = I2C(-1, Pin(5), Pin(4))
			tof = vl53l0x.VL53L0X(i2c)
			while len(distance_list) < 10:
				tof.start()
				tof.read()
				print(tof.read())
				distance=(tof.read())/10
				tof.stop()
				time.sleep(0.1)
				print('Distance: {}cm'.format(distance))
				if distance > 0.5:
					distance_list.append(distance)
		except:
			print("Nekaj je narobe pri calculate()")



	def procenti(cm):
			procent=(cm*100)/max_distance
			return round(procent)


	def mail(machine, distance, receiver):
	    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
	    smtp.login(sender_email, sender_password)
	    smtp.to(receiver)
	    smtp.write("From: {} <{}>\n".format(machine, sender_email))
	    smtp.write("Subject: Čas je za dofilat pelete!\n\n")
	    smtp.write("Kmalu bo zmanjkalo pelet. Razdalja: {}cm\n".format(distance))
	    smtp.send()
	    smtp.quit()



	def stop():
		mcron.remove_all()
		os.remove("main.py")


	mcron.init_timer()
	mcron.insert(interval, {0}, '{}s'.format(interval), sensor)

except:
	mail("PRIŠLO JE DO NAPAKE V MERITVI, treba bo ročno nastavit", "error", receiver)

