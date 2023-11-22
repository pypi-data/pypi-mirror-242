import logging
from onepackage import cifrar, descifrar

#logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.debug('>>> Estamos comenzando la ejecución del paquete.')
    
    logging.debug(help(cifrar))

    logging.debug(help(descifrar))

    logging.debug('>>> Estamos finalizando la ejecución del paquete.')