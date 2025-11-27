FROM gradle:7.0.2-jdk17 AS build


WORKDIR /app


COPY ./backend-server /app


RUN gradle build --no-daemon


FROM openjdk:17-jdk-slim


COPY --from=build /app/build/libs/*.jar /app/app.jar

# Открываем порт для приложения
EXPOSE 8080

# Запуск приложения
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
