# yandexmusicgraph
Граф исполнителей Яндекс.Музыки
## Описание
Увидев в одном из исследований Яндекса [карту русского рэпа](https://yandex.ru/company/researches/2018/rap#content__map), я решил сделать граф всех исполнителей Яндекс.Музыки.

Сбор данных будет происходить при помощи запросов к API Яндекс.Музыки. Данные будут хранится в базе данных MongoDB, а сам граф будет описан на языке DOT. Для визуализации будет использовано приложение Gephi.

![Scheme of the Program](https://sun9-44.userapi.com/c856132/v856132218/1a01cb/mI6HTAflvLk.jpg)
## Сбор данных
Чтобы составить граф, для каждого исполнителя нужно знать список похожих исполнителей. Проанализировав работу Яндекс.Музыки, были найдены следующие запросы для получения нужной информации:
1. https://music.yandex.ru/handlers/metatag.jsx?id=&tab=&page=&sortBy=popular&lang=ru
2. https://music.yandex.ru/handlers/artist.jsx?&artist=&lang=ru

Первый запрос нужен для того, чтобы получить список id исполнителей. Чтобы получить список для всех жанров в параметре id нужно указать "all", либо ничего не указывать.
Второй запрос нужен для того, чтобы получить информацию об исполнителе.

В ходе отладки программы было замечено, что Яндекс никак не ограничивает количество и частоту запросов. Поэтому при сборе данных я не использовал никаких задержек и прокси, получаемых при помощи написанного парсера.
## Хранение данных
Для хранения данных была выбрана MongoDB так как данные представляют из себя JSON-документы без жестко заданной схемы, которые могут содержать вложенные документы.
## Преобразование данных в граф
Для преобразования данных в граф была использована библиотека **graphviz**, с помощью которой получили файл графа на языке DOT.
При записи узла(исполнителя) написана проверка, что длина списка похожих исполнителей больше одного. Если не сделать этого, то на графе появятся узлы, не связанные с другими, что, в свою очередь, приведет к разлету этих узлов и неверному отображению графа на картинке.
## Визуализация графа
Существует множество инструментов для визуализации графов. Основные из них: **sfdp** из GraphViz (CLI утилита), **Gephi**.
Для наших данных подойдет Gephi, так как это GUI приложение, в котором есть возможность просмотра промежуточного результата и универсальный набор укладок.

При работе с графом в Gephi были раскрашены все узлы в цвета, которые соответствуют их жанрам, применены укладки и экспортированы в изображения.

При визуализации графа картинки недостаточно, так как из-за большого количества узлов их метки будут накладываться друг на друга. Для решения этой проблемы был установлен плагин для Gephi, который экспортирует граф в **sigma.js** шаблон.
## Результаты
В результате получился граф с ~10 000 узлов и 125 000 ребер.

### Рассмотрим несколько укладок:

#### OpenOrd
Для графа последовательно применены укладки OpenOrd + Noverlap и Расширение для устранения перекрытия узлов:
![OpenOrd](https://sun9-9.userapi.com/c855428/v855428218/1acd42/BVVc00oeHgs.jpg)

#### ForceAtlas 2
Для графа последовательно применены укладки ForceAtlas 2 + Noverlap и Расширение для устранения перекрытия узлов:
![OpenOrd](https://sun9-65.userapi.com/c855428/v855428218/1acd4c/42Zd9i9Bid0.jpg)

### Интерактивная карта
Для интерактивной карты применены укладки OpenOrd + Noverlap с большим коэффициентом отступа от других узлов, Расширение и Укладка меток:

[**Интерактивная карта**](https://dumaevrinat.github.io/yandexmusicgraph/#)

## Выводы
В результате был получен граф исполнителей Яндекс.Музыки, на котором есть явная кластеризация по жанрам. При помощи полученных данных можно составлять тематические подборки (например при помощи DBSCAN), узнавать о новых музыкантах на основе исполнителей, которых слушаете.

Также при помощи графа можно получить наглядную оценку рекомендательной системы. 

   
