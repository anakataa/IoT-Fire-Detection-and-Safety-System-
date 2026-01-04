# --- Этап 1: Сборка (Build) ---
FROM gradle:8.5-jdk17 AS build

# Устанавливаем рабочую папку внутри сборщика
WORKDIR /app

# Копируем файлы проекта
COPY build.gradle settings.gradle ./
COPY src ./src

# Если используешь gradlew wrapper, раскомментируй следующую строку:
# COPY gradlew ./
# COPY gradle ./gradle

# Запускаем сборку (пропускаем тесты, чтобы быстрее собрать образ)
RUN gradle build --no-daemon -x test

# --- Этап 2: Запуск (Run) ---
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Копируем собранный JAR файл из этапа сборки
# (Обрати внимание: путь build/libs/*.jar может меняться,
# обычно Spring Boot создает файл с версией, здесь мы берем любой jar)
COPY --from=build /app/build/libs/*.jar app.jar

# Открываем порт, указанный в README (8081)
EXPOSE 8081

# Команда запуска
ENTRYPOINT ["java", "-jar", "app.jar"]