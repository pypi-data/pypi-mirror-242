import re

def validarMensaje(message):
    """Retorna el mensaje descifrado.

    >>> validarMensaje("gato") == True
    True

    >>> validarMensaje("GATO") == False
    True

    >>> validarMensaje("") == False
    True
    
    """

    caracteresValidos = re.compile('[a-zñ ]')
    return (message != "" and len(message) > 0 and caracteresValidos.search(message) is not None)
