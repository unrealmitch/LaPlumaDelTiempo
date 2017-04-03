# -*- coding: utf-8 -*-
 
import sys

lista = []

def parser():
	file = open("piratas.txt",'r')
	while True: 
	    linea = file.readline().split()
	    if not linea: 
	        break
	    linea = [int(i) for i in linea]
	    lista.append(linea)
	file.close()
	print lista

def main():
	parser()

if __name__ == "__main__":
	main()