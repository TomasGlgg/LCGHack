# LCGHack

```shell
$ python main.py --help
usage: main.py [-h] -k ELEMENT [ELEMENT ...] [-m MODULUS] [-a MULTIPLIER] [-c INCREMENT] [-n COUNT]

optional arguments:
  -h, --help            show this help message and exit
  -m MODULUS, --modulus MODULUS
                        Модуль LCG
  -a MULTIPLIER, --multiplier MULTIPLIER
                        Множитель LCG
  -c INCREMENT, --increment INCREMENT
                        Приращение LCG
  -n COUNT, --next COUNT
                        Вычислить следующие значения

required arguments:
  -k ELEMENT [ELEMENT ...], --known-elements ELEMENT [ELEMENT ...]
                        Известные значения
```