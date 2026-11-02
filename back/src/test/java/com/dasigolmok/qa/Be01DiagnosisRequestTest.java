package com.dasigolmok.qa;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.diagnosis.repository.DiagnosisRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.nio.charset.StandardCharsets;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

@SpringBootTest
@AutoConfigureMockMvc
class Be01DiagnosisRequestTest {

    private static final String AI = """
            {"district":"마포구","dong":"연남동","industry":"한식","quarter":"20244",
             "store_count":25,"open_rate":3.4,"close_rate":6.2,"status":"stable","is_danger":false,
             "explanation":"기본 설명","explanation_source":"basic"}
            """;

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    DiagnosisRepository diagnosisRepository;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockBean
    AiClient aiClient;

    @BeforeEach
    void setUp() throws Exception {
        diagnosisRepository.deleteAll();
        given(aiClient.diagnose(any())).willReturn(objectMapper.readTree(AI));
    }

    @Test
    @DisplayName("BE01-001")
    void be01_001() throws Exception {
        MvcResult result = postRaw("""
                {"district":"마포구","dong":"연남동","industry":"한식"}
                """);
        obs("BE01-001", result);
        assertEquals(201, status(result), "status=" + status(result) + " body=" + brief(body(result)));
        assertFalse(body(result).contains("VALIDATION_ERROR"), body(result));
    }

    @Test
    @DisplayName("BE01-002")
    void be01_002() throws Exception {
        assertValidation("BE01-002", """
                {"dong":"연남동","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-003")
    void be01_003() throws Exception {
        assertValidation("BE01-003", """
                {"district":null,"dong":"연남동","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-004")
    void be01_004() throws Exception {
        assertValidation("BE01-004", """
                {"district":"","dong":"연남동","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-005")
    void be01_005() throws Exception {
        assertValidation("BE01-005", """
                {"district":"   ","dong":"연남동","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-006")
    void be01_006() throws Exception {
        assertValidation("BE01-006", """
                {"district":"마포구","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-007")
    void be01_007() throws Exception {
        assertValidation("BE01-007", """
                {"district":"마포구","dong":null,"industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-008")
    void be01_008() throws Exception {
        assertValidation("BE01-008", """
                {"district":"마포구","dong":"","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-009")
    void be01_009() throws Exception {
        assertValidation("BE01-009", """
                {"district":"마포구","dong":"   ","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-010")
    void be01_010() throws Exception {
        assertValidation("BE01-010", """
                {"district":"마포구","dong":"연남동"}
                """);
    }

    @Test
    @DisplayName("BE01-011")
    void be01_011() throws Exception {
        assertValidation("BE01-011", """
                {"district":"마포구","dong":"연남동","industry":null}
                """);
    }

    @Test
    @DisplayName("BE01-012")
    void be01_012() throws Exception {
        assertValidation("BE01-012", """
                {"district":"마포구","dong":"연남동","industry":""}
                """);
    }

    @Test
    @DisplayName("BE01-013")
    void be01_013() throws Exception {
        assertValidation("BE01-013", """
                {"district":"마포구","dong":"연남동","industry":"   "}
                """);
    }

    @Test
    @DisplayName("BE01-014")
    void be01_014() throws Exception {
        MvcResult result = postRaw("""
                {"district":"마포구","dong":"연남동","industry":123}
                """);
        int status = status(result);
        String responseBody = body(result);
        obs("BE01-014", result);
        if (status == 400) {
            assertTrue(responseBody.contains("VALIDATION_ERROR") || responseBody.contains("INVALID_JSON"),
                    brief(responseBody));
            return;
        }
        @SuppressWarnings("unchecked")
        org.mockito.ArgumentCaptor<Map<String, Object>> captor = org.mockito.ArgumentCaptor.forClass(Map.class);
        org.mockito.Mockito.verify(aiClient).diagnose(captor.capture());
        Object industry = captor.getValue().get("industry");
        System.out.println("OBS BE01-014 forwarded=" + industry);
        assertTrue(status >= 200 && status < 300, "status=" + status + " body=" + brief(responseBody));
        assertEquals("123", String.valueOf(industry), "숫자 industry 변환값=" + industry);
    }

    @Test
    @DisplayName("BE01-015")
    void be01_015() throws Exception {
        assertInvalidJson("BE01-015", "[]");
    }

    @Test
    @DisplayName("BE01-016")
    void be01_016() throws Exception {
        assertInvalidJson("BE01-016", "{'district':");
    }

    @Test
    @DisplayName("BE01-017")
    void be01_017() throws Exception {
        MvcResult result = mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.TEXT_PLAIN)
                        .content("{\"district\":\"마포구\",\"dong\":\"연남동\",\"industry\":\"한식\"}"))
                .andReturn();
        int status = status(result);
        obs("BE01-017", result);
        assertTrue(status == 415 || status == 400,
                "415/400이 아님 status=" + status + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE01-018")
    void be01_018() throws Exception {
        assertValidation("BE01-018", """
                {"District":"마포구","DOng":"연남동","industry":"한식"}
                """);
    }

    @Test
    @DisplayName("BE01-019")
    void be01_019() throws Exception {
        String district = "가".repeat(10000);
        given(aiClient.diagnose(any())).willAnswer(invocation -> {
            @SuppressWarnings("unchecked")
            Map<String, Object> sent = invocation.getArgument(0);
            ObjectNode node = (ObjectNode) objectMapper.readTree(AI);
            node.put("district", String.valueOf(sent.get("district")));
            return node;
        });
        String json = objectMapper.writeValueAsString(Map.of(
                "district", district, "dong", "연남동", "industry", "한식"));
        MvcResult result = postRaw(json);
        int status = status(result);
        String responseBody = body(result);
        int storedLength = status >= 200 && status < 300
                ? objectMapper.readTree(responseBody).path("district").asText("").length()
                : -1;
        System.out.println("OBS BE01-019 status=" + status + " storedLength=" + storedLength + " body=" + brief(responseBody));
        boolean rejected = status == 400 || status == 413 || status == 422;
        boolean truncated = status >= 200 && status < 300 && storedLength > 0 && storedLength <= 255;
        assertTrue(rejected || truncated,
                "입력 길이 제한 없음 status=" + status + " storedLength=" + storedLength + " body=" + brief(responseBody));
    }

    @Test
    @DisplayName("BE01-020")
    void be01_020() throws Exception {
        given(aiClient.diagnose(any())).willReturn(objectMapper.readTree("""
                {"district":"마포구","industry":"한식","status":"stable","is_danger":false,
                 "explanation":"기본 설명","explanation_source":"basic"}
                """));
        String json = objectMapper.writeValueAsString(Map.of(
                "district", "마포구", "dong", "<script>alert(1)</script>", "industry", "한식"));
        MvcResult result = postRaw(json);
        int status = status(result);
        String body = body(result);
        String contentType = String.valueOf(result.getResponse().getContentType());
        obs("BE01-020", result);
        boolean rejected = status >= 400 && status < 500;
        boolean sanitized = !body.contains("<script>");
        assertFalse(contentType.contains("text/html"), "HTML 응답 contentType=" + contentType);
        assertTrue(rejected || sanitized, "script가 그대로 반영됨 status=" + status + " body=" + brief(body));
    }

    @Test
    @DisplayName("BE01-021")
    void be01_021() throws Exception {
        String payload = "'; DROP TABLE diagnosis;--";
        String json = objectMapper.writeValueAsString(Map.of(
                "district", "마포구", "dong", "연남동", "industry", payload));
        MvcResult result = postRaw(json);
        int status = status(result);
        Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM diagnosis", Integer.class);
        obs("BE01-021", result);
        assertNotNull(count, "diagnosis 테이블 조회 실패");
        assertTrue(status == 400 || status == 422,
                "SQL 입력이 거절되지 않음 status=" + status + " rows=" + count + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE01-022")
    void be01_022() throws Exception {
        MvcResult result = postRaw("""
                {"district":"마포구","dong":"연남동","industry":"한식","extra":"value"}
                """);
        int status = status(result);
        String body = body(result);
        obs("BE01-022", result);
        assertEquals(201, status, "추가 필드 처리 status=" + status + " body=" + brief(body));
        JsonNode node = objectMapper.readTree(body);
        assertEquals("마포구", node.path("district").asText());
        assertEquals("연남동", node.path("dong").asText());
        assertEquals("한식", node.path("industry").asText());
        assertTrue(node.path("extra").isMissingNode(), "extra 필드가 응답에 포함됨");
    }

    @Test
    @DisplayName("BE01-023")
    void be01_023() throws Exception {
        given(aiClient.diagnose(any())).willAnswer(invocation -> {
            @SuppressWarnings("unchecked")
            Map<String, Object> sent = invocation.getArgument(0);
            ObjectNode node = (ObjectNode) objectMapper.readTree(AI);
            node.put("district", String.valueOf(sent.get("district")));
            node.put("dong", String.valueOf(sent.get("dong")));
            return node;
        });
        MvcResult result = postRaw("""
                {"district":"마포구","dong":"역삼동","industry":"한식"}
                """);
        int status = status(result);
        obs("BE01-023", result);
        assertEquals(400, status, "지역·동 조합 미검증 status=" + status + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE01-024")
    void be01_024() throws Exception {
        MvcResult result = postRaw("""
                {"industry":"한식"}
                """);
        int status = status(result);
        String body = body(result);
        obs("BE01-024", result);
        assertEquals(400, status, "status=" + status + " body=" + brief(body));
        assertTrue(body.contains("VALIDATION_ERROR"), body);
        assertTrue(body.contains("district"), body);
        assertTrue(body.contains("dong"), body);
    }

    private void assertValidation(String id, String json) throws Exception {
        MvcResult result = postRaw(json);
        obs(id, result);
        assertEquals(400, status(result), "status=" + status(result) + " body=" + brief(body(result)));
        assertTrue(body(result).contains("VALIDATION_ERROR"), body(result));
    }

    private void assertInvalidJson(String id, String json) throws Exception {
        MvcResult result = postRaw(json);
        obs(id, result);
        assertEquals(400, status(result), "status=" + status(result) + " body=" + brief(body(result)));
        assertTrue(body(result).contains("INVALID_JSON"), body(result));
    }

    private MvcResult postRaw(String json) throws Exception {
        return mockMvc.perform(post("/api/diagnoses")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(json))
                .andReturn();
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
