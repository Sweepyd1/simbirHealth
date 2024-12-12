# Общее описание задачи
В этом проекте разрабатывается микросервисное приложение, охватывающее различные аспекты программной инженерии, включая создание микросервисов, конфигурацию API и работу с базами данных. Цель заключается в разработке набора микросервисов, обеспечивающих функциональность для моделирования работы больницы, а также реализации дополнительных задач для расширенной функциональности и интеграции.

Архитектура приложения

Приложение состоит из нескольких ключевых микросервисов:

#### Account Microservice

Этот микросервис отвечает за авторизацию и управление данными пользователей. Все остальные сервисы зависят от него, так как именно он генерирует JWT токены и проводит их интроспекцию.

#### Hospital Microservice

Микросервис, который управляет данными о больницах, подключенных к системе. Он отправляет запросы в микросервис аккаунтов для интроспекции токена.

#### Timetable Microservice

Этот сервис отвечает за расписание врачей и больниц, а также за запись пользователей на приём. Он взаимодействует с микросервисом аккаунтов для проверки токенов и с микросервисом больниц для проверки существования связанных сущностей.

#### Document Microservice

Микросервис, который хранит историю посещений пользователей. Он также отправляет запросы в микросервис аккаунтов для интроспекции токена и в микросервис больниц для проверки существования связанных сущностей.
Эта архитектура позволяет создать гибкую и масштабируемую систему, где каждый компонент выполняет свою уникальную функцию и может быть независимо развернут и обновлён.

