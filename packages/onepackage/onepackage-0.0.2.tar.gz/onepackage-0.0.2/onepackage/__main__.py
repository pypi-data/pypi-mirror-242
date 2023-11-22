import logging
from onepackage import cifrar, descifrar

#logging.basicConfig(level=logging.INFO)

def main():
    logging.debug(help(cifrar))

    logging.debug(help(descifrar))

if __name__ == '__main__':
    logging.debug('>>> Estamos comenzando la ejecución del paquete.')
    
    main()

    logging.debug('>>> Estamos finalizando la ejecución del paquete.')