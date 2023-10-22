1. Założenia projektowe
==================================================


.. toctree::
    :maxdepth: 2

:Authors:
    Eryk Mika

:Version: 1.0 of 23.10.2023
:Course: Databases II


Wstęp
------------------------

Celem projektu jest zaprojektowanie i zaimplementowanie bazy danych dla systemu typu Mini-USOS wraz z funkcjonalną aplikacją webową operującą na tej bazie danych.

Wykorzystane technologie
---------------------------
Zakłada się, że do implementacji założeń projektowych wykorzystany zostanie język Python wraz z mikroframeworkiem Flask. Początkowo jako system bazodanowy użyty będzie system SQLite. 
Z punktu widzenia deweloperskiego zarządzanie zależnościami będzie się odbywać przy pomocy narzędzia Poetry.

Założenia dotyczące modelu danych
---------------------------------------------
Baza danych ma pozwalać na przechowywanie informacji o studentach, kierunkach studiów, ocenach studentów, prowadzących oraz zapisach studentów na zajęcia. Należy zagwarantować odporność modelu danych na różnego rodzaju anomalie.
Z tego powodu należy dążyć do spełnienia 3NF (postaci normalnej) dla relacji przechowywanych w bazie danych.

Funkcjonalności aplikacji
--------------------------------
Zaimplementowana aplikacja webowa ma odwzorowywać system typu USOS pod względem jego podstawowej funkcjonalności. Planuje się wdrożenie następujących funkcji:

1. Dostęp do ocen studentów

2. Dostęp do planu zajęć

3. Zapisywanie studentów na zajęcia

4. Przeglądanie komunikatów z uczelni

5. Dostęp do informacji o studentach

Należy zapewnić 2 poziomy dostępu do funkcji aplikacji - studenta oraz administratora.

Wydajność i dostępność aplikacji
---------------------------------------
Przyjmuje się, że aplikacja początkowo będzie przeznaczona dla niewielkiej grupy użytkowników - co najwyżej kilkadziesiąt studenów jednego wydziału i kilku kierunków oraz administrator. Dostęp do poszczególnych funkcjonalności będzie ograniczony.
Każdy student będzie miał po zalogowaniu dostęp do swoich danych, a administrator będzie dysponował dostępem do wszystkich danych w systemie.
