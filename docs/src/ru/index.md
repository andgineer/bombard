# Вступление

Bombard - это инструмент для стресс-тестирования и оценки производительности вашего HTTP-сервера. Он особенно хорош для симуляции высокой нагрузки и начального всплеска одновременных HTTP-запросов со сложной логикой. С его помощью легко и быстро описывать логику формирования запросов.

Он разработан, чтобы быть простым, но мощным инструментом для нагрузочного функционального тестирования.

Благодаря возможности использовать фрагменты кода Python вы можете легко и быстро описать сложную логику для тестов.

Отчет о тестировании показывает, сколько запросов в секунду способен обслуживать ваш сервер и с какой задержкой.

## Описание запросов

Минимально в запросе достаточно указать URL, но легко описать и JSON, например так:

```yaml
- url: https://example.com/login
  method: POST
  body:
    username: !python str(supply('username'))
    password: !python str(supply('password'))
  save:
    token: response.json()['token']
```

В первом запросе вы можете получить токен, как в примере выше.

И использовать его в следующих запросах:

```yaml
- url: https://example.com/api
  headers:
    Authorization: !python '"Bearer " + str(supply("token"))'
```

## Встроенные примеры

Для просмотра списка встроенных примеров:

```bash
bombard --examples
```

## Командная строка

Из командной строки вы можете изменить количество потоков, количество повторов, переопределить переменные, настроить вид отчета и так далее.

Также вы можете загрузить свой собственный файл `bombard.yaml` из любого понравившегося вам примера:

```bash
bombard --example http_get --reload
```

## Отчет

Пример отчета для команды:

```bash
bombard --example http_get --repeat 1000
```

## Исходный код

[GitHub](https://github.com/masterandrey/bombard/)
