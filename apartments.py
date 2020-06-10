import random

f = open("apartments.txt", "w+")

for i in range(100):
	apt = ['Unit', 'Apt', 'Suite']
	apartment = random.choice(apt) + " " + str(random.randint(0,9)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "\n"
	f.write(apartment)
	
f.close()