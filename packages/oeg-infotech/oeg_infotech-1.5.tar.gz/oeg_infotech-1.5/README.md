# Библиотека Python для обработки xml файлов "Инфотех"
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/oeg.infotech.xml/oeg.infotech.xml%20tests?label=Python%202.7%203.8%203.9%20PEP%20257&style=plastic)](https://github.com/vb64/oeg.infotech.xml/actions?query=workflow%3A%22oeg.infotech.xml+tests%22)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1c0b638957f44500a10694410a238294)](https://www.codacy.com/manual/vb64/oeg.infotech.xml?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/oeg.infotech.xml&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/1c0b638957f44500a10694410a238294)](https://www.codacy.com/manual/vb64/oeg.infotech.xml?utm_source=github.com&utm_medium=referral&utm_content=vb64/oeg.infotech.xml&utm_campaign=Badge_Coverage)

Библиотека Python для обработки xml файлов "Инфотех" с поддержкой дополнительных полей, требуемых для загрузки в "ИУС Т".

## Установка

```bash
pip install oeg-infotech
```

## Использование

```python

from oeg_infotech import Infotech, XmlFormat

# загрузить файл в формате "ИУС Т"
info = Infotech.from_file('iust.xml', xml_format=XmlFormat.Iust)
assert 'IUST_TYPE' in str(info)

# загрузить файл в формате "Инфотех"
info1 = Infotech.from_file('infotech1.xml')
assert 'IPL_INSPECT' in str(info1)

# перевернуть данные, пересчитав дистанции и угловые ориентации обьектов
xml_string = info1.reverse()
assert 'IPL_INSPECT' in xml_string

# обьединить перевернутые данные из infotech1.xml и данные из infotech2.xml,
# вставив между ними трубу длиной 11 метров
xml_string = info1.join(['1100', 'infotech2.xml'])
assert 'IPL_INSPECT' in xml_string
```

## Разработка

```bash
git clone git@github.com:vb64/oeg.infotech.xml.git
cd oeg.infotech.xml
```
При использовании Python 3.8, 3.9:
```bash
$ make setup3 PYTHON_BIN=/path/to/python3/executable
make tests3
```
При использовании Python 2.7:
```bash
make setup PYTHON_BIN=/path/to/python27/executable
make tests
```
