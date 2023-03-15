# Barbero_Durmiente

Pincha [aquí](https://github.com/Xavitheforce/Barbero_Durmiente) para dirigirte a mi repositorio.

Para esta entrega he divido el codigo en 4 archivos que representan al barbero, a la tienda, a los clientes y el main. Luego he introducido la carpeta introducir que controla los inputs realizados para evitar los fallos.

Vamos a analizar las distintas piezas de código comentadas de forma independiente.

El código realizado para los clientes es el siguiente:

```python
class Customer:
	def __init__(self, name):
		self.name = name#Creamos un Cliente que solo necesita su nombre          
```

Este archivo se encarga de crear la clase cliente y darle un nombre.

El código realizado para el barbero es el siguiente:

```python
from threading import Event, Lock
import time, random
from introducir import solicitar_introducir_numero, solicitar_introducir_numero_extremo_superior

mutex = Lock()# para que no se pueda acceder a la barberia mientras se esta cortando el pelo

#variables reutilizables en todo el programa
haircutDurationMin = solicitar_introducir_numero("Introduzca el tiempo mínimo de corte de pelo")
#variable que almacena el tiempo mínimo que tardará en cortar el pelo
haircutDurationMax = solicitar_introducir_numero_extremo_superior("Introduzca el tiempo máximo de corte de pelo", haircutDurationMin)
#variable que almacena el tiempo máximo que tardará en cortar el pelo
customerIntervalMin = solicitar_introducir_numero("Introduzca el intervalo mínimo entre clientes")
#variable que almacena el intervalo mínimo entre clientes
customerIntervalMax = solicitar_introducir_numero_extremo_superior("Introduzca el intervalo máximo entre clientes", customerIntervalMin)
#variable que almacena el intervalo máximo entre clientes

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
```

Este archivo se encarga de crear las variables que definirán los tiempos dentro del codigo y de crear al barbero con sus funciones para dormir, despertar y cortar el pelo.

El código realizado para la tienda es el siguiente:

```python
from threading import Thread
from barbero import haircutDurationMin, customerIntervalMin, customerIntervalMax, mutex

class BarberShop:
	waitingCustomers = [] #lista de clientes que están esperando

	def __init__(self, barber, asientos):
		self.barber = barber
		self.asientos = asientos
		print ('BarberShop iniciado con {} sitios'.format(asientos))
		print ('Mínimo intervalo de Clientes = {}'.format(customerIntervalMin))
		print ('Máximo intervalo de Clientes = {}'.format(customerIntervalMax))
		print ('Tiempo mínimo de corte de pelo = {}'.format(haircutDurationMin))
		print ('Tiempo máximo de corte de pelo = {}'.format(customerIntervalMax))
		print ('---------------------------------------')

	def openShop(self):
		print ('La barbería se está abriendo')
		workingThread = Thread(target = self.barberGoToWork)#declaramos un hilo para que el barbero trabaje
		workingThread.start()#iniciamos el hilo del barbero

	def barberGoToWork(self):
		while True:
			mutex.acquire()#bloqueamos hasta que suceda el release

			if len(self.waitingCustomers) > 0:
				c = self.waitingCustomers[0]#cogemos al primer cliente y lo eliminamos de la lista
				del self.waitingCustomers[0]
				mutex.release()
				self.barber.cutHair(c)#hacemos que el barbero le corte el pelo al cliente escogido
			else:
				mutex.release()
				print ('Sin clientes en espera, tomando un descanso...')
				self.barber.sleep()
				print ('El barbero se ha despertado')

	def enterBarberShop(self, customer):
		mutex.acquire() #bloqueamos hasta que suceda el release
		print ('>>>>> {} entró en la tienda y está buscando un sitio'.format(customer.name))

		if len(self.waitingCustomers) == self.asientos: #si la sala de espera está llena
			print ('La sala de espera está llena, {} se va a marchar.'.format(customer.name))
			mutex.release()
		else:
			print ('{} se ha sentado en la sala de espera'.format(customer.name))
			self.waitingCustomers.append(customer) #añadimos al cliente a la lista de clientes en espera
			mutex.release()
			self.barber.wakeUp()#Despertamos al barbero       
```

Este archivo se encarga de establecer la cola de clientes, definir el comportamiento del barbero dentro de la tienda y de crear el hilo de ejecución que lleva las acciones anteriores a cabo.

Finalmente, el main es el siguiente:

```python
import time, random
import os
from barbero import Barber, customerIntervalMin, customerIntervalMax
from cola_tienda import BarberShop
from cliente import Customer
from introducir import solicitar_introducir_numero, solicitar_introducir_palabra


if __name__ == '__main__':
    nclientes = solicitar_introducir_numero("Introduzca el número de clientes que desea introducir")
    #variable que almacena el número de clientes que se van a introducir

    customers = [] #lista de clientes
    for i in range(nclientes): #bucle que introduce los clientes en la lista
        customers.append(Customer('{}'.format(solicitar_introducir_palabra("Introduzca el nombre del cliente"))))

    barber = Barber() #iniciamos al barbero

    barberShop = BarberShop(barber, asientos=1) #iniciamos la barbería con un asiento
    barberShop.openShop() #abrimos el thread

    while len(customers) > 0:
        c = customers.pop()#Cogemos un cliente y lo eliminamos de la lista
        #New customer enters the barbershop
        barberShop.enterBarberShop(c)#el cliente c entra a la barbería
        customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1) #generamos un intervalo aleatorio entre los dos valores
        time.sleep(customerInterval) #esperamos el intervalo de tiempo generado

    time.sleep(1) #esperamos un segundo para que el barbero pueda terminar de cortar el pelo
    print ('Todos los clientes de hoy han sido atendidos')
    os._exit(0) #salimos del programa/terminamos ejecución
```

Este código contruye el flujo que debe llevar el código y conecta los otros 3 archivos. Empieza definiendo el número de clientes que va a tener la ejecución y añadiendo dichos clientes en una lista. Luego, inicializa los módulos importados y crea un bucle iterarivo que recoge cada cliente de la lista y lo introduce a la tienda. Al final, un .sleep que se asegura de que ya han pasado todos los clientes por la tienda y que el barbero se ha vuelto a acostar para terminar con un os._exit, que fuerza la detención del código de forma que se acaba con el hilo de ejecución.

Ahora vamos a ver la salida por terminal del main:

![introducir_variables](https://user-images.githubusercontent.com/91721699/225333448-b4a94ede-0c53-40e9-92ee-d58711428601.png)

Lo primero que se pide es introducir los parámetros que definirán lo ocurrido en la barbería. En este ejemplo, y para poder observar todas las situaciones posibles, hemos introducido tiempos de corte de pelo que en general(por probabilidad, ya que el programa elige un número entre el intervalo establecido por los inputs de forma aleatoria, para eso el random) serán más altos que los tiempos de llegada de clientes. Cabe destacar en esta parte el control de excepciones que no permitirá introducir palabras o símbolos donde deben ir números, además de asegurar ciertas condiciones, como que el segundo número dentro de un intervalo sea mayor al anterior introducido... y tampoco permitirá introducir números donde deben ir palabras, por ejemplo al introducir nombres.

La segunda parte del output es:

![output](https://user-images.githubusercontent.com/91721699/225335153-19e4ee4e-2616-4afe-9d01-b5afd5bab1ec.png)

Como se ve en la imagen el barbero empieza durmiendo, y se despierta cuando llegan clientes. Además, cuando un cliente acaba, si no hay clientes en espera este regresa a descansar. También se ven los casos en los que llegan clientes cuando ya hay gente cortándose el pelo o esperando. En el primero, el cliente ingresa en la lista de espera, que se corresponde con un asiento, mientras que en el segundo el cliente se marcha, ya que al definir la barberia solo hemos introducido 1 asiento para poder esperar.
