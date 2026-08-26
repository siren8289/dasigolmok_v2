# Build context: repository root (see docker-compose.yml)
FROM gradle:8.10-jdk17-alpine AS build
WORKDIR /workspace
COPY back/build.gradle.kts back/settings.gradle.kts back/gradlew back/gradlew.bat ./back/
COPY back/gradle ./back/gradle
WORKDIR /workspace/back
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon
COPY back/src ./src
COPY db/migration ../db/migration
RUN ./gradlew bootJar -x test --no-daemon

# Run
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
RUN addgroup -S spring && adduser -S spring -G spring
RUN mkdir -p uploads && chown spring:spring uploads
USER spring:spring
COPY --from=build /workspace/back/build/libs/dasi-golmok-api.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
