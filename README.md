# Астрономічний календар
## Description
Даний репозиторій-курсова робота студента першого курсу Комп'ютерних наук УКУ. Проект призначено для швидкого та зручного створення календаря астрономічних подій, цікавих для конкретної особи. 

### Опис проекту
Astro-calendar - це додаток на основі Тkinter, який забезпечує такі можливості:

* Перегляд всіх подій для певного інтервалу часу;
* Створення власного календаря з обраними подіями;
* Завантаження, збереження та модифікація існуючих календарів;

### Структура проекту
* Модулі для структури даних:
  * Calendar.py - основний функціонал структури
  * event.py, date.py, array.py - допоміжні модулі
* Модулі для реалізації GUI та логіки програми:
  * calendar_window.py - Частина головного вікна, показує один календар
  * event_window.py - Вікно з інформацією про подію
  * info_windows.py - вікна Help та About
  * scrolled_frame.py - допоміжний модуль для прокрутки календаря
  * application.py - основний модуль
* Допоміжні файли:
  * data\ - повні календарі по роках
  * usercals\ - календаря користувача

## Використання
Для початку роботи необхідно зберегти та розпакувати Astronomical Calendar-0.1.tar.zip з папки дdist  та прописату у командному рядку
`python setup.py install`
