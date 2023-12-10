# Easy Geometry
Набор скриптов, используемый компанией Scientia для обработки данных геометрии

[Сайт](https://scientia.ru)

[Сайт](https://scientia_ru.t.me/)

## blender_parser.py
После выполнения измерений на модели инструментом измерить, обязательно сохраните файл `.blend`

Далее открываем панель `Редактор текста` (Shift+F11)

По середине сверху этой панели нажимаете на кнопку `Создать`.

Вставляете код из `blender_parser.py` в текстовый редактор.

Нажимаем на кнопку `Запустить скрипт` (Alt+P)

Рядом с файлом .blend появится текстовый файл "%blendername%_source.txt". В него записаны координаты вершин выполненных измерений.

## post_blender_txt_parser.py
В строке 95 задаем путь к папке с файлами, в которой появился `%blendername%_source.txt`

Выполняем скрипт и получаем csv таблицы углами и азимутами выполненных измерений.

Раядом с фалами `%blendername%_source.txt` cоздается 2 файла с линейными и угловыми измерениями. `%blendername%_result_E.csv` и `%blendername%_result_F.csv` соотвественно

## connect_tables.py
Что бы объеденить все результаты `..._F.csv` `..._E.csv` в одну таблицу, необходимо в `connect_tables.py` в строке 27 заменить путь к папке в которой хранятся таблицы и запустить скрипт 

## dxf_to_digger.py
Для функционирования этого скрипта необходимо установить библиотеку `ezdxf`.
Пропишите в консоль `pip install ezdxf`

В строке 38 задаем путь к файлу dxf с трехмерной геометрией (триангуляционной сеткой)

Радом с файлом появится таблица `%blendername%_result.csv` с данными о центрах и направлениях всех треугольников
