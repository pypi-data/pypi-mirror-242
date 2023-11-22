# ONEPackage

[![PyPI Downloads](https://img.shields.io/pypi/dm/onepackage.svg?label=PyPI%20downloads)](https://pypi.org/project/onepackage/)

- **Source code:** https://github.com/Ange1D/ONEPackage
- **Bug reports:** https://github.com/Ange1D/ONEPackage/issues

Descripción
=========

Es un package para cifrar y descifrar texto basado en el [desafío del programa Oracle Next Education](https://ange1d.github.io/Challenge-ONE-Alura/) 
- Funciona solo con letras minúsculas
- No se deben utilizar letras con acentos ni caracteres especiales
-  Las "llaves" que se utilizan son las siguientes:
   - La letra "e" es convertida para "enter"
   - La letra "i" es convertida para "imes"
   - La letra "a" es convertida para "ai"
   - La letra "o" es convertida para "ober"
   - La letra "u" es convertida para "ufat"

## Instalación
```
pip install onepackage
```

## uso:
```python
from onepackage import cifrar
    mensaje = cifrar("gato")
    print(mensaje)
```
Output `gaitober`

```python
from onepackage import descifrar
    mensaje = descifrar("gaitober")
    print(mensaje)
```
Output `gato`

```python
from onepackage import descifrar
    mensaje = descifrar("GATO")
    print(mensaje)
```
Output `Message contains unsupported characters`


## CLI

| Comando | Descripción | 
| ------------------------ | ------------------------ | 
| cifrador | Retorna la informacion de la funcion cifrar y descifrar |



## Testing:
    import onepackage
    help(onepackage.cifrar)
    help(onepackage.descifrar)
    help(onepackage.validarMensaje)

## License

[MIT](https://github.com/Ange1D/ONEPackage/blob/main/LICENSE.txt)