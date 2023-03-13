from threading import Lock
import time, random
from barbero import Barber
from cola_tienda import BarberShop
from cliente import Customer

mutex = Lock()# para que no se pueda acceder a la barberia mientras se esta cortando el pelo

#Interval in seconds
customerIntervalMin = 5
customerIntervalMax = 15

if __name__ == '__main__':
	customers = []
	customers.append(Customer('Sara'))
	customers.append(Customer('Carlota'))
	customers.append(Customer('María'))
	customers.append(Customer('Alex'))
	customers.append(Customer('Andrea'))
	customers.append(Customer('Javi'))
	customers.append(Customer('Raúl'))
	customers.append(Customer('Rubén'))
	customers.append(Customer('Lorenzo'))
	customers.append(Customer('David'))
	customers.append(Customer('Pepe'))
	customers.append(Customer('Pedro'))
	customers.append(Customer('Paco'))
	customers.append(Customer('Juan'))
	customers.append(Customer('Tomas'))
	customers.append(Customer('Lara'))
	customers.append(Customer('Ana'))

	barber = Barber()

	barberShop = BarberShop(barber, asientos=1)
	barberShop.openShop()

	while len(customers) > 0:
		c = customers.pop()#Cogemos un cliente y lo eliminamos de la lista
		#New customer enters the barbershop
		barberShop.enterBarberShop(c)#el cliente c entra a la barbería
		customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)
		time.sleep(customerInterval)