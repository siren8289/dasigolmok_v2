package com.dasigolmok.qa;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import com.dasigolmok.ai.AiClient;
import com.dasigolmok.diagnosis.repository.DiagnosisRepository;
import com.dasigolmok.global.exception.ApiException;
import com.dasigolmok.global.exception.GlobalExceptionHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.nio.charset.StandardCharsets;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.options;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

@SpringBootTest
@AutoConfigureMockMvc
class Be06GlobalExceptionTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    GlobalExceptionHandler handler;

    @Autowired
    DiagnosisRepository diagnosisRepository;

    @MockBean
    AiClient aiClient;

    @BeforeEach
    void clean() {
        diagnosisRepository.deleteAll();
    }

    @Test
    @DisplayName("BE06-001")
    void be06_001() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/424242")).andReturn();
        String body = body(result);
        obs("BE06-001", result);
        assertEquals(404, status(result), brief(body));
        assertTrue(body.contains("\"errorCode\""), body);
        assertTrue(body.contains("NOT_FOUND"), body);
        assertTrue(body.contains("\"message\""), body);
    }

    @Test
    @DisplayName("BE06-002")
    void be06_002() throws Exception {
        given(aiClient.diagnose(any())).willThrow(ApiException.aiError("AI 서버 호출에 실패했습니다.", new IllegalStateException("down")));
        MvcResult result = mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"district\":\"마포구\",\"dong\":\"연남동\",\"industry\":\"한식\"}"))
                .andReturn();
        String body = body(result);
        obs("BE06-002", result);
        assertTrue(status(result) >= 500, "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("AI_ERROR"), body);
        assertTrue(body.contains("\"message\""), body);
    }

    @Test
    @DisplayName("BE06-003")
    void be06_003() throws Exception {
        MvcResult result = mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"district\":\"\",\"dong\":\"연남동\",\"industry\":\"한식\"}"))
                .andReturn();
        String body = body(result);
        obs("BE06-003", result);
        assertEquals(400, status(result), brief(body));
        assertTrue(body.contains("VALIDATION_ERROR"), body);
    }

    @Test
    @DisplayName("BE06-004")
    void be06_004() throws Exception {
        MvcResult result = mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"district\":"))
                .andReturn();
        String body = body(result);
        obs("BE06-004", result);
        assertEquals(400, status(result), brief(body));
        assertTrue(body.contains("INVALID_JSON"), body);
    }

    @Test
    @DisplayName("BE06-005")
    void be06_005() {
        ResponseEntity<Map<String, String>> response = handler.handleUnexpected(new RuntimeException("boom-internal-detail"));
        System.out.println("OBS BE06-005 status=" + response.getStatusCode().value() + " body=" + response.getBody());
        assertEquals(500, response.getStatusCode().value());
        assertEquals("INTERNAL_ERROR", response.getBody().get("errorCode"));
        assertNotNull(response.getBody().get("message"));
        assertFalse(response.getBody().get("message").contains("boom-internal-detail"));
    }

    @Test
    @DisplayName("BE06-006")
    void be06_006() {
        ListAppender<ILoggingEvent> appender = attach(GlobalExceptionHandler.class.getName());
        ApiException ex = ApiException.aiError("ai-down-marker", new IllegalStateException("root-cause-marker"));
        handler.handleApiException(ex);
        String logs = eventsText(appender);
        System.out.println("OBS BE06-006 logs=" + brief(logs));
        assertTrue(logs.contains("ai-down-marker"), "원인 메시지 없음 logs=" + brief(logs));
        assertTrue(logs.contains("root-cause-marker"), "cause 없음 logs=" + brief(logs));
        assertTrue(appender.list.stream().anyMatch(event -> event.getLevel() == Level.ERROR && event.getThrowableProxy() != null),
                "스택 로그 없음");
    }

    @Test
    @DisplayName("BE06-007")
    void be06_007() {
        ListAppender<ILoggingEvent> appender = attach(GlobalExceptionHandler.class.getName());
        handler.handleApiException(ApiException.notFound("없는 진단"));
        String logs = eventsText(appender);
        System.out.println("OBS BE06-007 events=" + appender.list.size() + " logs=" + brief(logs));
        assertTrue(appender.list.stream().noneMatch(event -> event.getLevel() == Level.ERROR),
                "4xx ERROR 로그 " + brief(logs));
        assertTrue(appender.list.stream().allMatch(event -> event.getThrowableProxy() == null),
                "4xx 스택 로그 " + brief(logs));
    }

    @Test
    @DisplayName("BE06-008")
    void be06_008() {
        SQLException sql = new SQLException("ERROR: syntax error at \"; DROP TABLE diagnosis\" password=secret-stack");
        ResponseEntity<Map<String, String>> response = handler.handleUnexpected(sql);
        String text = String.valueOf(response.getBody());
        System.out.println("OBS BE06-008 body=" + text);
        assertEquals(500, response.getStatusCode().value());
        assertEquals("INTERNAL_ERROR", response.getBody().get("errorCode"));
        assertFalse(text.contains("DROP TABLE"), text);
        assertFalse(text.contains("secret-stack"), text);
        assertFalse(text.contains("SQLException"), text);
    }

    @Test
    @DisplayName("BE06-009")
    void be06_009() throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(10);
        try {
            List<Future<MvcResult>> futures = new ArrayList<>();
            for (int i = 0; i < 10; i++) {
                long id = 910000L + i;
                futures.add(pool.submit(() -> mockMvc.perform(get("/api/diagnoses/" + id)).andReturn()));
            }
            for (int i = 0; i < futures.size(); i++) {
                long id = 910000L + i;
                MvcResult result = futures.get(i).get(10, TimeUnit.SECONDS);
                String body = body(result);
                System.out.println("OBS BE06-009 id=" + id + " status=" + status(result) + " body=" + brief(body));
                assertEquals(404, status(result), brief(body));
                assertTrue(body.contains("NOT_FOUND"), body);
                assertTrue(body.contains(String.valueOf(id)), "응답이 요청 id와 다름 body=" + brief(body));
            }
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    @DisplayName("BE06-010")
    void be06_010() throws Exception {
        MvcResult result = mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"district\":\"\",\"dong\":\" \",\"industry\":null}"))
                .andReturn();
        String body = body(result);
        obs("BE06-010", result);
        assertEquals(400, status(result), brief(body));
        assertTrue(body.contains("VALIDATION_ERROR"), body);
        assertTrue(body.contains("district"), body);
        assertTrue(body.contains("dong"), body);
        assertTrue(body.contains("industry"), body);
    }

    @Test
    @DisplayName("BE06-011")
    void be06_011() {
        ApiException ex = new ApiException(HttpStatus.BAD_REQUEST, "NOT_FOUND", null, null);
        try {
            ResponseEntity<Map<String, String>> response = handler.handleApiException(ex);
            String message = response.getBody() == null ? null : response.getBody().get("message");
            System.out.println("OBS BE06-011 status=" + response.getStatusCode().value() + " message=" + message);
            assertNotNull(response.getBody());
            assertNotNull(response.getBody().get("errorCode"));
            assertNotNull(message, "message가 null");
        } catch (NullPointerException npe) {
            System.out.println("OBS BE06-011 NPE " + npe);
            fail("Map.of null message로 추가 예외: " + npe);
        }
    }

    @Test
    @DisplayName("BE06-012")
    void be06_012() throws Exception {
        Logger logger = (Logger) LoggerFactory.getLogger("org.springframework.web.cors.DefaultCorsProcessor");
        Level previous = logger.getLevel();
        logger.setLevel(Level.DEBUG);
        ListAppender<ILoggingEvent> appender = new ListAppender<>();
        appender.start();
        logger.addAppender(appender);
        try {
            MvcResult result = mockMvc.perform(options("/api/diagnoses")
                            .header("Origin", "https://evil.example")
                            .header("Access-Control-Request-Method", "POST"))
                    .andReturn();
            String allow = result.getResponse().getHeader("Access-Control-Allow-Origin");
            String logs = eventsText(appender);
            System.out.println("OBS BE06-012 status=" + status(result) + " allow=" + allow + " logs=" + brief(logs));
            assertTrue(status(result) == 403 || allow == null || !"https://evil.example".equals(allow),
                    "허용되지 않은 Origin이 통과 status=" + status(result) + " allow=" + allow);
            assertTrue(logs.contains("Reject") || logs.contains("not allowed") || logs.contains("CORS") || logs.contains("evil.example"),
                    "CORS 거부 로그 없음 logs=" + brief(logs) + " status=" + status(result));
        } finally {
            logger.detachAppender(appender);
            logger.setLevel(previous);
        }
    }

    @Test
    @DisplayName("BE06-013")
    void be06_013() throws Exception {
        MvcResult result = mockMvc.perform(delete("/api/options")).andReturn();
        obs("BE06-013", result);
        assertEquals(405, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE06-014")
    void be06_014() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/abc")).andReturn();
        String body = body(result);
        String contentType = String.valueOf(result.getResponse().getContentType());
        obs("BE06-014", result);
        assertEquals(400, status(result), "status=" + status(result) + " contentType=" + contentType + " body=" + brief(body));
        assertTrue(contentType.contains("application/json"), "contentType=" + contentType);
        assertTrue(body.contains("\"errorCode\""), body);
        assertTrue(body.contains("\"message\""), body);
    }

    private static ListAppender<ILoggingEvent> attach(String name) {
        Logger logger = (Logger) LoggerFactory.getLogger(name);
        ListAppender<ILoggingEvent> appender = new ListAppender<>();
        appender.start();
        logger.addAppender(appender);
        return appender;
    }

    private static String eventsText(ListAppender<ILoggingEvent> appender) {
        StringBuilder builder = new StringBuilder();
        for (ILoggingEvent event : appender.list) {
            builder.append(event.getLevel()).append(' ').append(event.getFormattedMessage()).append('\n');
            if (event.getThrowableProxy() != null) {
                builder.append(event.getThrowableProxy().getClassName()).append(": ")
                        .append(event.getThrowableProxy().getMessage()).append('\n');
                if (event.getThrowableProxy().getCause() != null) {
                    builder.append(event.getThrowableProxy().getCause().getMessage()).append('\n');
                }
            }
        }
        return builder.toString();
    }

    private static int status(MvcResult result) {
        return result.getResponse().getStatus();
    }

    private static String body(MvcResult result) throws Exception {
        return result.getResponse().getContentAsString(StandardCharsets.UTF_8);
    }

    private static void obs(String id, MvcResult result) throws Exception {
        System.out.println("OBS " + id + " status=" + status(result) + " body=" + brief(body(result)));
    }

    private static String brief(String value) {
        if (value == null) {
            return "null";
        }
        String one = value.replaceAll("\\s+", " ");
        return one.length() > 180 ? one.substring(0, 180) : one;
    }
}
