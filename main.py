import time, random
import os
from barbero import Barber, customerIntervalMin, customerIntervalMax
from cola_tienda import BarberShop
from cliente import Customer
from introducir import solicitar_introducir_numero, solicitar_introducir_palabra


if __name__ == '__main__':
	#Interval in seconds
    nclientes = solicitar_introducir_numero("Introduzca el número de clientes que desea introducir")

    customers = []
    for i in range(nclientes):
        customers.append(Customer('{}'.format(solicitar_introducir_palabra("Introduzca el nombre del cliente"))))

    barber = Barber()

    barberShop = BarberShop(barber, asientos=1)
    barberShop.openShop()

    while len(customers) > 0:
        c = customers.pop()#Cogemos un cliente y lo eliminamos de la lista
        #New customer enters the barbershop
        barberShop.enterBarberShop(c)#el cliente c entra a la barbería
        customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)
        time.sleep(customerInterval)