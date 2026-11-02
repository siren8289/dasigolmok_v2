package com.dasigolmok.qa;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.diagnosis.repository.DiagnosisRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
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

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

@SpringBootTest
@AutoConfigureMockMvc
class Be03DiagnosisHttpTest {

    private static final String REQUEST = """
            {"district":"마포구","dong":"연남동","industry":"한식"}
            """;

    private static final String AI = """
            {"district":"마포구","dong":"연남동","industry":"한식","quarter":"20244",
             "store_count":25,"open_rate":3.4,"close_rate":6.2,"status":"stable","is_danger":false,
             "explanation":"연남동 기본 설명","explanation_source":"basic"}
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
    @DisplayName("BE03-001")
    void be03_001() throws Exception {
        MvcResult result = postDiagnosis(REQUEST);
        obs("BE03-001", result);
        assertEquals(201, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-002")
    void be03_002() throws Exception {
        jdbcTemplate.execute("ALTER TABLE diagnosis ALTER COLUMN id RESTART WITH 10");
        MvcResult result = postDiagnosis(REQUEST);
        JsonNode node = objectMapper.readTree(body(result));
        obs("BE03-002", result);
        assertEquals(201, status(result), brief(body(result)));
        assertEquals(10, node.path("id").asInt(), "id=" + node.path("id").asText() + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-003")
    void be03_003() throws Exception {
        jdbcTemplate.update(
                "INSERT INTO diagnosis (id, district, dong, industry, danger) VALUES (?,?,?,?,?)",
                10, "마포구", "연남동", "한식", false);
        MvcResult result = mockMvc.perform(get("/api/diagnoses/10")).andReturn();
        JsonNode node = objectMapper.readTree(body(result));
        obs("BE03-003", result);
        assertEquals(200, status(result), brief(body(result)));
        assertEquals("마포구", node.path("district").asText());
        assertEquals("연남동", node.path("dong").asText());
        assertEquals("한식", node.path("industry").asText());
    }

    @Test
    @DisplayName("BE03-004")
    void be03_004() throws Exception {
        postDiagnosis(REQUEST);
        MvcResult result = mockMvc.perform(get("/api/diagnoses")).andReturn();
        JsonNode node = objectMapper.readTree(body(result));
        obs("BE03-004", result);
        assertEquals(200, status(result), brief(body(result)));
        assertTrue(node.isArray(), "List가 아님 body=" + brief(body(result)));
        assertTrue(node.size() >= 1, "빈 목록");
    }

    @Test
    @DisplayName("BE03-005")
    void be03_005() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/abc")).andReturn();
        String body = body(result);
        obs("BE03-005", result);
        assertEquals(400, status(result), "type mismatch status=" + status(result) + " body=" + brief(body));
        assertTrue(body.toLowerCase().contains("mismatch")
                        || body.contains("abc")
                        || body.contains("Long")
                        || body.contains("타입")
                        || body.contains("형식"),
                "type mismatch 안내 없음 body=" + brief(body));
    }

    @Test
    @DisplayName("BE03-006")
    void be03_006() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/0")).andReturn();
        obs("BE03-006", result);
        assertEquals(404, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-007")
    void be03_007() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/-1")).andReturn();
        obs("BE03-007", result);
        assertEquals(404, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-008")
    void be03_008() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/99999999999999999999")).andReturn();
        obs("BE03-008", result);
        assertEquals(400, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-009")
    void be03_009() throws Exception {
        MvcResult result = postDiagnosis(REQUEST);
        String contentType = String.valueOf(result.getResponse().getContentType());
        obs("BE03-009", result);
        assertTrue(contentType.contains("application/json"), "contentType=" + contentType);
    }

    @Test
    @DisplayName("BE03-010")
    void be03_010() throws Exception {
        MvcResult result = mockMvc.perform(delete("/api/diagnoses/1")).andReturn();
        obs("BE03-010", result);
        assertEquals(405, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE03-011")
    void be03_011() throws Exception {
        MvcResult result = postDiagnosis("""
                {"district":"","dong":"","industry":""}
                """);
        String body = body(result);
        obs("BE03-011", result);
        assertEquals(400, status(result), "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("district"), body);
        assertTrue(body.contains("dong"), body);
        assertTrue(body.contains("industry"), body);
    }

    @Test
    @DisplayName("BE03-012")
    void be03_012() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/diagnoses/424242")).andReturn();
        String body = body(result);
        obs("BE03-012", result);
        assertEquals(404, status(result), "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("NOT_FOUND"), body);
    }

    @Test
    @DisplayName("BE03-013")
    void be03_013() throws Exception {
        MvcResult result = postDiagnosis(REQUEST);
        String body = body(result);
        obs("BE03-013", result);
        assertEquals(201, status(result), brief(body));
        assertTrue(body.contains("연남동"), body);
        assertTrue(body.contains("기본 설명"), body);
        assertFalseReplacement(body);
    }

    @Test
    @DisplayName("BE03-014")
    void be03_014() throws Exception {
        MvcResult created = postDiagnosis(REQUEST);
        long id = objectMapper.readTree(body(created)).path("id").asLong();
        MvcResult result = mockMvc.perform(get("/api/diagnoses/" + id)).andReturn();
        int code = status(result);
        obs("BE03-014", result);
        assertTrue(code == 401 || code == 403,
                "인증 없이 진단 조회 status=" + code + " body=" + brief(body(result)));
    }

    private void assertFalseReplacement(String body) {
        assertTrue(!body.contains("???") && !body.contains("占"), "한글 깨짐 body=" + brief(body));
    }

    private MvcResult postDiagnosis(String json) throws Exception {
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
        System.out.println("OBS " + id + " status=" + status(result)
                + " contentType=" + result.getResponse().getContentType()
                + " body=" + brief(body(result)));
    }

    private static String brief(String value) {
        if (value == null) {
            return "null";
        }
        String one = value.replaceAll("\\s+", " ");
        return one.length() > 180 ? one.substring(0, 180) : one;
    }
}
