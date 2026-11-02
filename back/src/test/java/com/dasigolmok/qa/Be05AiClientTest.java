package com.dasigolmok.qa;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import com.dasigolmok.ai.AiClient;
import com.dasigolmok.global.exception.ApiException;
import com.dasigolmok.global.exception.GlobalExceptionHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.UnknownContentTypeException;

import java.lang.reflect.Field;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import java.net.http.HttpClient;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.atLeast;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

@SpringBootTest
class Be05AiClientTest {

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    RestTemplate restTemplate;

    @Autowired
    GlobalExceptionHandler handler;

    @Test
    @DisplayName("BE05-001")
    void be05_001() throws Exception {
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(objectMapper.readTree("{\"ok\":true}")).when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        client.options();
        verify(mockRt).getForObject(eq("http://ai:8000/api/v1/options"), eq(JsonNode.class));
        System.out.println("OBS BE05-001 url=http://ai:8000/api/v1/options");
    }

    @Test
    @DisplayName("BE05-002")
    void be05_002() throws Exception {
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(objectMapper.readTree("{\"ok\":true}")).when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        client.diagnose(Map.of("district", "마포구", "dong", "연남동", "industry", "한식"));
        verify(mockRt).postForObject(eq("http://ai:8000/api/v1/diagnose"), any(), eq(JsonNode.class));
        System.out.println("OBS BE05-002 url=http://ai:8000/api/v1/diagnose");
    }

    @Test
    @DisplayName("BE05-003")
    void be05_003() throws Exception {
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(objectMapper.readTree("{\"ok\":true}")).when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        client.recommend(Map.of("district", "마포구", "dong", "연남동"));
        verify(mockRt).postForObject(eq("http://ai:8000/api/v1/recommend"), any(), eq(JsonNode.class));
        System.out.println("OBS BE05-003 url=http://ai:8000/api/v1/recommend");
    }

    @Test
    @DisplayName("BE05-004")
    void be05_004() throws Exception {
        JsonNode expected = objectMapper.readTree("{\"districts\":[\"마포구\"]}");
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(expected).when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        JsonNode actual = new AiClient(mockRt, "http://ai:8000").options();
        System.out.println("OBS BE05-004 type=" + actual.getClass().getSimpleName() + " body=" + actual);
        assertTrue(actual instanceof JsonNode);
        assertEquals(expected, actual);
    }

    @Test
    @DisplayName("BE05-005")
    void be05_005() throws Exception {
        JsonNode expected = objectMapper.readTree("{\"status\":\"stable\"}");
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(expected).when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        JsonNode actual = new AiClient(mockRt, "http://ai:8000")
                .diagnose(Map.of("district", "마포구", "dong", "연남동", "industry", "한식"));
        System.out.println("OBS BE05-005 body=" + actual);
        assertEquals(expected, actual);
    }

    @Test
    @DisplayName("BE05-006")
    void be05_006() throws Exception {
        JsonNode expected = objectMapper.readTree("{\"recommendations\":[]}");
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(expected).when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        JsonNode actual = new AiClient(mockRt, "http://ai:8000")
                .recommend(Map.of("district", "마포구", "dong", "연남동"));
        System.out.println("OBS BE05-006 body=" + actual);
        assertEquals(expected, actual);
    }

    @Test
    @DisplayName("BE05-007")
    void be05_007() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(null).when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000").options());
        System.out.println("OBS BE05-007 code=" + ex.getErrorCode() + " status=" + ex.getStatus().value() + " message=" + ex.getMessage());
        assertEquals("AI_ERROR", ex.getErrorCode());
        assertEquals(HttpStatus.BAD_GATEWAY, ex.getStatus());
    }

    @Test
    @DisplayName("BE05-008")
    void be05_008() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new ResourceAccessException("Connection refused", new ConnectException("Connection refused")))
                .when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000").options());
        System.out.println("OBS BE05-008 code=" + ex.getErrorCode() + " message=" + ex.getMessage());
        assertEquals("AI_ERROR", ex.getErrorCode());
        assertEquals(HttpStatus.BAD_GATEWAY, ex.getStatus());
    }

    @Test
    @DisplayName("BE05-009")
    void be05_009() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new ResourceAccessException("I/O error", new UnknownHostException("ai")))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000")
                .diagnose(Map.of("district", "마포구", "dong", "연남동", "industry", "한식")));
        System.out.println("OBS BE05-009 code=" + ex.getErrorCode() + " cause=" + ex.getCause().getClass().getSimpleName());
        assertEquals("AI_ERROR", ex.getErrorCode());
    }

    @Test
    @DisplayName("BE05-010")
    void be05_010() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new ResourceAccessException("Read timed out", new SocketTimeoutException("Read timed out")))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000")
                .recommend(Map.of("district", "마포구", "dong", "연남동")));
        System.out.println("OBS BE05-010 code=" + ex.getErrorCode() + " message=" + ex.getMessage());
        assertEquals("AI_ERROR", ex.getErrorCode());
        assertEquals(HttpStatus.BAD_GATEWAY, ex.getStatus());
    }

    @Test
    @DisplayName("BE05-011")
    void be05_011() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(HttpClientErrorException.create(HttpStatus.NOT_FOUND, "Not Found", HttpHeaders.EMPTY,
                "{\"detail\":\"missing\"}".getBytes(StandardCharsets.UTF_8), StandardCharsets.UTF_8))
                .doThrow(HttpServerErrorException.create(HttpStatus.INTERNAL_SERVER_ERROR, "ERR", HttpHeaders.EMPTY,
                        new byte[0], StandardCharsets.UTF_8))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        Map<String, Object> body = Map.of("district", "마포구", "dong", "연남동", "industry", "한식");
        ApiException notFound = assertThrows(ApiException.class, () -> client.diagnose(body));
        ApiException server = assertThrows(ApiException.class, () -> client.diagnose(body));
        System.out.println("OBS BE05-011 notFound=" + notFound.getErrorCode() + "/" + notFound.getStatus().value()
                + " server=" + server.getErrorCode() + "/" + server.getStatus().value());
        assertNotEquals(server.getErrorCode(), notFound.getErrorCode(),
                "404와 500이 구분되지 않음 code=" + notFound.getErrorCode());
        assertTrue(notFound.getErrorCode().contains("404") || "NOT_FOUND".equals(notFound.getErrorCode()),
                "404 전용 코드 없음 code=" + notFound.getErrorCode() + " status=" + notFound.getStatus().value());
    }

    @Test
    @DisplayName("BE05-012")
    void be05_012() {
        byte[] raw = "{\"detail\":[{\"loc\":[\"industry\"],\"msg\":\"field required\"}]}".getBytes(StandardCharsets.UTF_8);
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(HttpClientErrorException.create(HttpStatus.UNPROCESSABLE_ENTITY, "Unprocessable Entity",
                HttpHeaders.EMPTY, raw, StandardCharsets.UTF_8))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000")
                .diagnose(Map.of("district", "마포구", "dong", "연남동", "industry", "한식")));
        System.out.println("OBS BE05-012 message=" + ex.getMessage() + " code=" + ex.getErrorCode());
        assertTrue(ex.getMessage().contains("field required") || ex.getMessage().contains("industry"),
                "422 validation 원인 없음 message=" + ex.getMessage());
    }

    @Test
    @DisplayName("BE05-013")
    void be05_013() {
        String stack = "java.lang.IllegalStateException: secret\n\tat com.internal.Model.infer(Model.java:42)";
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(HttpServerErrorException.create(HttpStatus.INTERNAL_SERVER_ERROR, "ERR", HttpHeaders.EMPTY,
                stack.getBytes(StandardCharsets.UTF_8), StandardCharsets.UTF_8))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000")
                .recommend(Map.of("district", "마포구", "dong", "연남동")));
        ResponseEntity<Map<String, String>> response = handler.handleApiException(ex);
        String responseText = String.valueOf(response.getBody());
        System.out.println("OBS BE05-013 message=" + ex.getMessage() + " response=" + responseText);
        assertFalse(ex.getMessage().contains("IllegalStateException"), ex.getMessage());
        assertFalse(ex.getMessage().contains("com.internal"), ex.getMessage());
        assertFalse(responseText.contains("Model.java"), responseText);
        assertFalse(responseText.contains("IllegalStateException"), responseText);
    }

    @Test
    @DisplayName("BE05-014")
    void be05_014() throws Exception {
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(objectMapper.readTree("{}")).when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        try {
            JsonNode node = new AiClient(mockRt, "http://ai:8000")
                    .diagnose(Map.of("district", "마포구", "dong", "연남동", "industry", "한식"));
            System.out.println("OBS BE05-014 returned=" + node);
            fail("핵심 필드 누락을 감지하지 않고 반환: " + node);
        } catch (ApiException ex) {
            System.out.println("OBS BE05-014 rejected=" + ex.getErrorCode() + " " + ex.getMessage());
            assertNotNull(ex.getErrorCode());
        }
    }

    @Test
    @DisplayName("BE05-015")
    void be05_015() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new UnknownContentTypeException(JsonNode.class, MediaType.TEXT_HTML, 200, "OK",
                HttpHeaders.EMPTY, "<html><body>gateway</body></html>".getBytes(StandardCharsets.UTF_8)))
                .when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000").options());
        System.out.println("OBS BE05-015 message=" + ex.getMessage());
        assertTrue(ex.getMessage().contains("JSON") || ex.getMessage().contains("역직렬") || ex.getMessage().contains("형식"),
                "JSON 역직렬화 안내 없음 message=" + ex.getMessage());
    }

    @Test
    @DisplayName("BE05-016")
    void be05_016() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(HttpServerErrorException.create(HttpStatus.SERVICE_UNAVAILABLE, "unavailable", HttpHeaders.EMPTY,
                new byte[0], StandardCharsets.UTF_8))
                .when(mockRt).postForObject(anyString(), any(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        assertThrows(ApiException.class, () -> client.recommend(Map.of("district", "마포구", "dong", "연남동")));
        try {
            verify(mockRt, atLeast(2)).postForObject(anyString(), any(), eq(JsonNode.class));
            System.out.println("OBS BE05-016 retried");
        } catch (AssertionError error) {
            System.out.println("OBS BE05-016 " + error.getMessage());
            throw error;
        }
    }

    @Test
    @DisplayName("BE05-017")
    void be05_017() throws Exception {
        String dump = dumpTimeouts(restTemplate.getRequestFactory());
        RestTemplate mockRt = mock(RestTemplate.class);
        doReturn(objectMapper.readTree("{\"ok\":true}")).when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        AiClient client = new AiClient(mockRt, "http://ai:8000");
        ExecutorService pool = Executors.newFixedThreadPool(20);
        try {
            ListAppender<ILoggingEvent> appender = attach("com.dasigolmok.ai.AiClient");
            java.util.List<Future<JsonNode>> futures = new java.util.ArrayList<>();
            for (int i = 0; i < 20; i++) {
                futures.add(pool.submit(client::options));
            }
            for (Future<JsonNode> future : futures) {
                assertNotNull(future.get(5, TimeUnit.SECONDS));
            }
            System.out.println("OBS BE05-017 completed=20 timeouts=" + dump + " logs=" + appender.list.size());
            assertTrue(hasFiniteTimeout(dump, "connect", 3_000) || dump.contains("PT3S") || dump.contains("3000"),
                    "connect timeout 없음 " + dump);
            assertTrue(hasFiniteTimeout(dump, "read", 40_000) || dump.contains("PT40S") || dump.contains("40000"),
                    "read timeout 없음 " + dump);
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    @DisplayName("BE05-018")
    void be05_018() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new ResourceAccessException("I/O error on GET request for \"https://wrong/api/v1/options\": wrong",
                new UnknownHostException("wrong")))
                .when(mockRt).getForObject(eq("https://wrong/api/v1/options"), eq(JsonNode.class));
        ListAppender<ILoggingEvent> app = attach(AiClient.class.getName());
        ListAppender<ILoggingEvent> root = attach(org.slf4j.Logger.ROOT_LOGGER_NAME);
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "https://wrong").options());
        handler.handleApiException(ex);
        String logs = eventsText(app) + eventsText(root);
        System.out.println("OBS BE05-018 message=" + ex.getMessage() + " logs=" + brief(logs));
        boolean guided = containsConfigHint(ex.getMessage()) || containsConfigHint(logs);
        assertTrue(guided, "설정 오류 로그·안내 없음 message=" + ex.getMessage() + " logs=" + brief(logs));
    }

    @Test
    @DisplayName("BE05-019")
    void be05_019() {
        RestTemplate mockRt = mock(RestTemplate.class);
        doThrow(new RestClientException("upstream failed DB_PASSWORD=supersecret"))
                .when(mockRt).getForObject(anyString(), eq(JsonNode.class));
        ListAppender<ILoggingEvent> logs = attach(GlobalExceptionHandler.class.getName());
        ApiException ex = assertThrows(ApiException.class, () -> new AiClient(mockRt, "http://ai:8000").options());
        ResponseEntity<Map<String, String>> response = handler.handleApiException(ex);
        String responseText = String.valueOf(response.getBody());
        String logText = eventsText(logs);
        System.out.println("OBS BE05-019 response=" + responseText + " log=" + brief(logText));
        assertFalse(responseText.contains("DB_PASSWORD"), responseText);
        assertFalse(responseText.contains("supersecret"), responseText);
        assertFalse(logText.contains("DB_PASSWORD"), "로그에 DB_PASSWORD 노출 " + brief(logText));
        assertFalse(logText.contains("supersecret"), "로그에 비밀값 노출 " + brief(logText));
    }

    @Test
    @DisplayName("BE05-020")
    void be05_020() {
        ClientHttpRequestFactory factory = restTemplate.getRequestFactory();
        String dump = dumpTimeouts(factory);
        System.out.println("OBS BE05-020 factory=" + factory.getClass().getName() + " " + dump);
        assertTrue(dump.contains("PT3S") || dump.contains("3000"),
                "connect timeout 미적용 factory=" + factory.getClass().getName() + " " + dump);
        assertTrue(dump.contains("PT40S") || dump.contains("40000"),
                "read timeout 미적용 factory=" + factory.getClass().getName() + " " + dump);
    }

    private static boolean containsConfigHint(String text) {
        if (text == null) {
            return false;
        }
        return text.contains("설정") || text.contains("base-url") || text.contains("APP_AI_BASE_URL") || text.contains("주소");
    }

    private static boolean hasFiniteTimeout(String dump, String kind, int millis) {
        return dump.contains(kind) && (dump.contains(String.valueOf(millis)) || dump.contains("PT"));
    }

    private static ListAppender<ILoggingEvent> attach(String name) {
        Logger logger = (Logger) LoggerFactory.getLogger(name);
        logger.setLevel(Level.DEBUG);
        ListAppender<ILoggingEvent> appender = new ListAppender<>();
        appender.start();
        logger.addAppender(appender);
        return appender;
    }

    private static String eventsText(ListAppender<ILoggingEvent> appender) {
        StringBuilder builder = new StringBuilder();
        for (ILoggingEvent event : appender.list) {
            builder.append(event.getFormattedMessage()).append('\n');
            if (event.getThrowableProxy() != null) {
                appendThrowable(builder, event.getThrowableProxy(), 0);
            }
        }
        return builder.toString();
    }

    private static void appendThrowable(StringBuilder builder, ch.qos.logback.classic.spi.IThrowableProxy proxy, int depth) {
        if (proxy == null || depth > 6) {
            return;
        }
        builder.append(proxy.getClassName()).append(": ").append(proxy.getMessage()).append('\n');
        appendThrowable(builder, proxy.getCause(), depth + 1);
    }

    private static String dumpTimeouts(Object root) {
        StringBuilder builder = new StringBuilder();
        walk(root, builder, new IdentityHashMap<>(), 0);
        return builder.toString();
    }

    private static void walk(Object value, StringBuilder builder, IdentityHashMap<Object, Boolean> seen, int depth) {
        if (value == null || depth > 4 || seen.containsKey(value)) {
            return;
        }
        if (!(value instanceof Duration) && !isWalkable(value)) {
            return;
        }
        seen.put(value, Boolean.TRUE);
        Class<?> type = value.getClass();
        while (type != null && type != Object.class) {
            if (type.getName().startsWith("java.lang.")) {
                break;
            }
            for (Field field : type.getDeclaredFields()) {
                try {
                    field.setAccessible(true);
                    Object child = field.get(value);
                    String name = field.getName().toLowerCase();
                    if (child instanceof Duration duration && (name.contains("timeout") || name.contains("duration"))) {
                        builder.append(field.getName()).append('=').append(duration).append(';');
                    } else if ((child instanceof Number) && name.contains("timeout")) {
                        builder.append(field.getName()).append('=').append(child).append(';');
                    } else if (child != null && depth < 4 && isWalkable(child)) {
                        walk(child, builder, seen, depth + 1);
                    }
                } catch (RuntimeException | ReflectiveOperationException ignored) {
                    builder.append(field.getName()).append("=inaccessible;");
                }
            }
            type = type.getSuperclass();
        }
    }

    private static boolean isWalkable(Object value) {
        if (value instanceof Duration || value instanceof Number || value instanceof String || value instanceof Enum) {
            return false;
        }
        String name = value.getClass().getName();
        return name.startsWith("org.springframework") || name.startsWith("jdk.internal.net.http") || value instanceof HttpClient
                || value instanceof ClientHttpRequestFactory;
    }

    private static String brief(String value) {
        if (value == null) {
            return "null";
        }
        String one = value.replaceAll("\\s+", " ");
        return one.length() > 220 ? one.substring(0, 220) : one;
    }
}
