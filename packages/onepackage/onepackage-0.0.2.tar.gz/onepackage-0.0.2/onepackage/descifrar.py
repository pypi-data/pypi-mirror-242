import re
from .validarMensaje import validarMensaje

def descifrar(message):
    """Retorna el mensaje descifrado.

    >>> descifrar("gaitober") == "gato"
    True

    >>> descifrar("GAITOBER") == "Message contains unsupported characters"
    True
    
    """
    mensajeDescifrado = ""
    
    if validarMensaje(message):
        mensajeDescifrado = re.sub(r'enter', 'e', message)
        mensajeDescifrado = re.sub(r'imes', 'i', mensajeDescifrado)
        mensajeDescifrado = re.sub(r'ai', 'a', mensajeDescifrado)
        mensajeDescifrado = re.sub(r'ober', 'o', mensajeDescifrado)
        mensajeDescifrado = re.sub(r'ufat', 'u', mensajeDescifrado)
    else:
        mensajeDescifrado = "Message contains unsupported characters"

    return mensajeDescifrado
