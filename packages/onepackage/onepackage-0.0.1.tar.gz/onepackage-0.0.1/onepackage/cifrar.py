from .validarMensaje import validarMensaje

def cifrar(message):
    """Retorna el mensaje cifrado.

    >>> cifrar("gato") == "gaitober"
    True

    >>> cifrar("GATO") == "Message contains unsupported characters"
    True
    
    """
    mensajeCifrado = ""

    if validarMensaje(message):
        for letra in message:
            if letra == "e":
                mensajeCifrado += "enter"
            elif letra == "i":
                mensajeCifrado += "imes"
            elif letra == "a":
                mensajeCifrado += "ai"
            elif letra == "o":
                mensajeCifrado += "ober"
            elif letra == "u":
                mensajeCifrado += "ufat"
            else:
                mensajeCifrado += letra
    else:
        mensajeCifrado = "Message contains unsupported characters"

    return mensajeCifrado
