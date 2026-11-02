package com.dasigolmok.qa;

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
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doAnswer;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.doThrow;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

@SpringBootTest
@AutoConfigureMockMvc
class Be04RecommendHttpTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    DiagnosisRepository diagnosisRepository;

    @MockBean
    RestTemplate restTemplate;

    @BeforeEach
    void clean() {
        diagnosisRepository.deleteAll();
    }

    @Test
    @DisplayName("BE04-001")
    void be04_001() throws Exception {
        JsonNode options = objectMapper.readTree("""
                {"districts":["마포구"],"dongs":{"마포구":["연남동"]},"industries":["한식"]}
                """);
        doReturn(options).when(restTemplate).getForObject(anyString(), eq(JsonNode.class));
        MvcResult result = mockMvc.perform(get("/api/options")).andReturn();
        obs("BE04-001", result);
        assertEquals(200, status(result), brief(body(result)));
        assertEquals(options, objectMapper.readTree(body(result)));
    }

    @Test
    @DisplayName("BE04-002")
    void be04_002() throws Exception {
        JsonNode recommend = objectMapper.readTree("""
                {"district":"마포구","dong":"연남동","recommendations":[{"industry":"한식","score":1}]}
                """);
        doReturn(recommend).when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"연남동"}
                """);
        obs("BE04-002", result);
        assertEquals(200, status(result), brief(body(result)));
        assertEquals(recommend, objectMapper.readTree(body(result)));
    }

    @Test
    @DisplayName("BE04-003")
    void be04_003() throws Exception {
        assertValidation("BE04-003", """
                {"dong":"연남동"}
                """);
    }

    @Test
    @DisplayName("BE04-004")
    void be04_004() throws Exception {
        assertValidation("BE04-004", """
                {"district":" ","dong":"연남동"}
                """);
    }

    @Test
    @DisplayName("BE04-005")
    void be04_005() throws Exception {
        assertValidation("BE04-005", """
                {"district":"마포구"}
                """);
    }

    @Test
    @DisplayName("BE04-006")
    void be04_006() throws Exception {
        assertValidation("BE04-006", """
                {"district":"마포구","dong":" "}
                """);
    }

    @Test
    @DisplayName("BE04-007")
    void be04_007() throws Exception {
        MvcResult result = postRecommend("{\"district\":");
        obs("BE04-007", result);
        assertEquals(400, status(result), brief(body(result)));
        assertTrue(body(result).contains("INVALID_JSON"), body(result));
    }

    @Test
    @DisplayName("BE04-008")
    void be04_008() throws Exception {
        doThrow(HttpClientErrorException.create(
                HttpStatus.NOT_FOUND, "Not Found", HttpHeaders.EMPTY, new byte[0], StandardCharsets.UTF_8))
                .when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"없는동"}
                """);
        String body = body(result);
        obs("BE04-008", result);
        assertEquals(502, status(result), "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("AI_ERROR"), body);
        assertTrue(body.contains("message"), body);
    }

    @Test
    @DisplayName("BE04-009")
    void be04_009() throws Exception {
        doReturn(null).when(restTemplate).getForObject(anyString(), eq(JsonNode.class));
        MvcResult result = mockMvc.perform(get("/api/options")).andReturn();
        String body = body(result);
        obs("BE04-009", result);
        assertTrue(status(result) == 502 || status(result) == 500,
                "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("AI_ERROR") || body.contains("INTERNAL_ERROR"), body);
        assertFalse(body.isBlank(), "빈 응답");
    }

    @Test
    @DisplayName("BE04-010")
    void be04_010() throws Exception {
        JsonNode options = objectMapper.readTree("""
                {"districts":["마포구","강남구"],"dongs":{"마포구":["연남동","성산동"]},"industries":["한식","카페"]}
                """);
        doReturn(options).when(restTemplate).getForObject(anyString(), eq(JsonNode.class));
        MvcResult result = mockMvc.perform(get("/api/options")).andReturn();
        JsonNode actual = objectMapper.readTree(body(result));
        obs("BE04-010", result);
        assertEquals(200, status(result), brief(body(result)));
        assertEquals(options, actual);
        assertTrue(actual.path("districts").isArray());
        assertEquals(2, actual.path("districts").size());
        assertEquals("성산동", actual.path("dongs").path("마포구").get(1).asText());
    }

    @Test
    @DisplayName("BE04-011")
    void be04_011() throws Exception {
        JsonNode recommend = objectMapper.readTree("""
                {"all_industries":[{"industry":"한식","score":2.0,"status":"stable"},
                                   {"industry":"카페","score":1.0,"status":"caution"}]}
                """);
        doReturn(recommend).when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"연남동"}
                """);
        JsonNode actual = objectMapper.readTree(body(result));
        obs("BE04-011", result);
        assertEquals(200, status(result), brief(body(result)));
        assertEquals("한식", actual.path("all_industries").get(0).path("industry").asText());
        assertEquals("카페", actual.path("all_industries").get(1).path("industry").asText());
        assertEquals(2.0, actual.path("all_industries").get(0).path("score").asDouble(), 0.0001);
        assertEquals("stable", actual.path("all_industries").get(0).path("status").asText());
    }

    @Test
    @DisplayName("BE04-012")
    void be04_012() throws Exception {
        ObjectNode recommend = objectMapper.createObjectNode();
        var array = recommend.putArray("recommendations");
        for (int i = 1; i <= 5; i++) {
            array.addObject().put("industry", "업종" + i).put("rank", i);
        }
        doReturn(recommend).when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"연남동"}
                """);
        JsonNode actual = objectMapper.readTree(body(result));
        obs("BE04-012", result);
        assertEquals(200, status(result), brief(body(result)));
        assertTrue(actual.path("recommendations").size() <= 5, "size=" + actual.path("recommendations").size());
        assertEquals(5, actual.path("recommendations").size());
        assertEquals("업종1", actual.path("recommendations").get(0).path("industry").asText());
        assertEquals("업종5", actual.path("recommendations").get(4).path("industry").asText());
    }

    @Test
    @DisplayName("BE04-013")
    void be04_013() throws Exception {
        long before = diagnosisRepository.count();
        doThrow(HttpClientErrorException.create(
                HttpStatus.NOT_FOUND, "Not Found", HttpHeaders.EMPTY, new byte[0], StandardCharsets.UTF_8))
                .when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"없는동"}
                """);
        obs("BE04-013", result);
        assertTrue(status(result) >= 400, "status=" + status(result) + " body=" + brief(body(result)));
        assertEquals(before, diagnosisRepository.count(), "추천 실패 후 diagnosis 건수 변화");
    }

    @Test
    @DisplayName("BE04-014")
    void be04_014() throws Exception {
        doAnswer(invocation -> {
            @SuppressWarnings("unchecked")
            Map<String, Object> request = invocation.getArgument(1);
            ObjectNode node = objectMapper.createObjectNode();
            node.put("district", String.valueOf(request.get("district")));
            node.put("dong", String.valueOf(request.get("dong")));
            node.putArray("recommendations");
            return node;
        }).when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        String[][] pairs = {{"마포구", "연남동"}, {"강남구", "역삼동"}, {"종로구", "청운효자동"}, {"용산구", "이태원동"}};
        ExecutorService pool = Executors.newFixedThreadPool(4);
        try {
            List<Future<MvcResult>> futures = new ArrayList<>();
            for (String[] pair : pairs) {
                String json = objectMapper.writeValueAsString(Map.of("district", pair[0], "dong", pair[1]));
                futures.add(pool.submit(() -> postRecommend(json)));
            }
            for (int i = 0; i < pairs.length; i++) {
                MvcResult result = futures.get(i).get(10, TimeUnit.SECONDS);
                JsonNode node = objectMapper.readTree(body(result));
                System.out.println("OBS BE04-014 status=" + status(result)
                        + " district=" + node.path("district").asText() + " dong=" + node.path("dong").asText());
                assertEquals(200, status(result), brief(body(result)));
                assertEquals(pairs[i][0], node.path("district").asText());
                assertEquals(pairs[i][1], node.path("dong").asText());
            }
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    @DisplayName("BE04-015")
    void be04_015() throws Exception {
        doThrow(new ResourceAccessException("Read timed out", new SocketTimeoutException("Read timed out")))
                .when(restTemplate).getForObject(anyString(), eq(JsonNode.class));
        MvcResult result = mockMvc.perform(get("/api/options")).andReturn();
        String body = body(result);
        obs("BE04-015", result);
        assertEquals(502, status(result), "status=" + status(result) + " body=" + brief(body));
        assertTrue(body.contains("\"errorCode\""), body);
        assertTrue(body.contains("AI_ERROR"), body);
        assertTrue(body.contains("\"message\""), body);
        assertFalse(body.contains("SocketTimeoutException"), body);
    }

    @Test
    @DisplayName("BE04-016")
    void be04_016() throws Exception {
        MvcResult result = mockMvc.perform(get("/api/recommendations")).andReturn();
        obs("BE04-016", result);
        assertEquals(405, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE04-017")
    void be04_017() throws Exception {
        doAnswer(invocation -> {
            @SuppressWarnings("unchecked")
            Map<String, Object> request = invocation.getArgument(1);
            System.out.println("OBS BE04-017 aiKeys=" + request.keySet());
            assertFalse(request.containsKey("industry"), "industry가 AI로 전달됨 " + request);
            assertEquals(java.util.Set.of("district", "dong"), request.keySet());
            return objectMapper.readTree("{\"district\":\"" + request.get("district") + "\",\"recommendations\":[]}");
        }).when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"연남동","industry":"한식"}
                """);
        obs("BE04-017", result);
        assertEquals(200, status(result), "status=" + status(result) + " body=" + brief(body(result)));
    }

    @Test
    @DisplayName("BE04-018")
    void be04_018() throws Exception {
        doReturn(objectMapper.readTree("{\"district\":\"마포구\",\"dong\":\"역삼동\",\"recommendations\":[]}"))
                .when(restTemplate).postForObject(anyString(), any(), eq(JsonNode.class));
        MvcResult result = postRecommend("""
                {"district":"마포구","dong":"역삼동"}
                """);
        obs("BE04-018", result);
        assertEquals(400, status(result), "교차 지역이 통과 status=" + status(result) + " body=" + brief(body(result)));
    }

    private void assertValidation(String id, String json) throws Exception {
        MvcResult result = postRecommend(json);
        obs(id, result);
        assertEquals(400, status(result), "status=" + status(result) + " body=" + brief(body(result)));
        assertTrue(body(result).contains("VALIDATION_ERROR"), body(result));
    }

    private MvcResult postRecommend(String json) throws Exception {
        return mockMvc.perform(post("/api/recommendations")
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
