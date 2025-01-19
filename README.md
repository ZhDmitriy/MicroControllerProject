# MicroControllerProject

Проект по курсу "Интеллектуальная робототехника". 

Суть проекта: создание собственного FaceID инструмента для быстрого развертывания и решения соответственно бизнес и не бизнес задач. 

Проект состоит из 6 ключевых элементов: 
- imageData - папка в которую мы должны положить фотографию для сопоставления по биометрии лиц
- compareResultPointsFace.py - основной код скрипта, здесь используется библиотека mediapipe от Google
- config.yml - конфигурационные данные проекта (IP адрес сервера с видео потоком камеры ESP32CAM)
- initPointsFace.py - инициализируем и сравниваем анатомические точки лица с фотографии и с live изображения
- makeKeyAction.py - реализуем ключевое действие с компонентами Arduino (в нашем случае, если совпадение верное, то загорается зеленый светодиод, иначе красный)
- KeyActionArduino.ino - скетч дял загрузки на компонент Arduino Uno с подключенными заранее светодиодами

Что нужно изменить в проекте для кастомного запуска: 

self.directory = '/home/dmitriy/PycharmProjects/FaceIDProject/imageData' - укажите путь до своей директории, учитывая свою операционную систему (у меня Linux)

CAMERA_CONFIG:
  - CAMERA_URL:
      - 'http://172.20.10.11' - укажите свой IP-адрес сервера (чтобы его получить см. инструкцию ниже)
   

Для запуска необходимо: 

0. Подключить ESP32CAM к порту usb0 (пока работает на ОС Linux) и установить необходимые зависимиости
1. Установить Arduino IDE и запустить скетч с Camera Web Server
	1.1 Указать модель камеры CAMERA_MODEL_AI_THINKER в проекте
2. Получить IP-адрес Camera Web Server из монитора порта
3. При развертывании проекта указать в конфигурационном yml файле этот IP-адрес
4. Загрузить свою фотографию для биометрии (сопоставления лиц)
5. Запустить файл сборки = makeKeyAction.py 
	
