FROM gradle:8-jdk17 AS build


WORKDIR /app


COPY . /app


RUN ./gradlew build --no-daemon


FROM eclipse-temurin:17-jdk-alpine


COPY --from=build /app/build/libs/demo-0.0.1-SNAPSHOT.jar /app/app.jar

# Открываем порт для приложения
EXPOSE 8081

# Запуск приложения
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
