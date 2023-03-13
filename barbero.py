from threading import Event
import time, random

haircutDurationMin = 3
haircutDurationMax = 15

class Barber:
	barberWorkingEvent = Event()#El barbero se crea un evento que es cuando está trabajando

	def sleep(self):
		self.barberWorkingEvent.wait()#Definimos que si se duerme entonces el evento se para

	def wakeUp(self):
		self.barberWorkingEvent.set()#Definimos que si se despierta entonces el evento se activa

	def cutHair(self, customer):
		#Definiendo que el barbero está trabajando
		self.barberWorkingEvent.clear()#Se limpia el evento

		print ('A {} le están cortando el pelo'.format(customer.name))

		randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
		time.sleep(randomHairCuttingTime)#ponemos un tiempo aleatorio que tardará en cortar el pelo
		print ('{} ha terminado'.format(customer.name))
