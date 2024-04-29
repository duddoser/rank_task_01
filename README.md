# Задача Ранжирования
## Условие
На вход подается датасает с признаками rank, query_id, feature0,..., feature146. 

*Задача*: для каждого запроса пользователя отранжировать документы.

Приложение написано на языке python и представлено в виде файлов с расширениями .py и .ipynb.

Программа написана с использованием библиотек:
* catboost (1.2.5)
* sklearn (1.4)
* tensorflow-ranking (1.4.0)

## Решение задачи
### Препроцессинг и анализ датасета.
Перед работой с полученными входными данными необходимо взглянуть на то, что они из себя представляют, т.е. посмотреть представленные типы данных и возможно изменить датасет. 
В данном случае пришлось убрать признаки и строки с незаполненными значениями, т.к. количество таких данных было мало. 

После этого можно проанализировать зависимости между признаками. Взглянув на таблицу, отображающую корреляцию признаков, можно заметить, что многие фичи зависят линейно друг от друга
(и достаточно сильно). Для борьбы с мультиколлинеарностью помимо использования l2 - регуляризации (гиперпараметр которой еще нужно найти), попробуем удалить признаки с корреляцией
0.95 и больше. Это даст чуть лучше значение на метрике.

И последнее: отмасштабируем данные, т.к. они распределены в разных границах.

### Обучение модели
Для начала разделим датасет на обучающую, валидационную и тестовую выборку.Так как в этой программе используется алгоритм бустинга, валидационная выборка будет хорошом решением для
решения проблемы переобучения. 

Параметры модели находятся  в словаре *default_parametres*. Далее обучим выборку и посмотрим метрику NDCG@5 и MAP@5 для валидационной выборки на графике. Как видно для нашей модели достаточно
около 50 деревьев.

### Предсказание
Предскажем значения для тестовой выборки и посмотрим метрики для полученных результатов.

NDCG = 0.79094

MAP = 0.7769

## Вывод
Полученная модель неплохо справаляется с задачей ранжирования, ведь значения метрик примерно около 0.80.
