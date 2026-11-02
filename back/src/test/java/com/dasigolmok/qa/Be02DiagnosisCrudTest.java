package com.dasigolmok.qa;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.diagnosis.dto.DiagnosisRequest;
import com.dasigolmok.diagnosis.entity.Diagnosis;
import com.dasigolmok.diagnosis.repository.DiagnosisRepository;
import com.dasigolmok.diagnosis.service.DiagnosisService;
import com.dasigolmok.global.exception.ApiException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyMap;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;

@SpringBootTest
class Be02DiagnosisCrudTest {

    @Autowired
    DiagnosisService service;

    @Autowired
    DiagnosisRepository repository;

    @Autowired
    ObjectMapper objectMapper;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @MockBean
    AiClient aiClient;

    @BeforeEach
    void clean() {
        repository.deleteAll();
    }

    @Test
    @DisplayName("BE02-001")
    void be02_001() throws Exception {
        given(aiClient.diagnose(anyMap())).willReturn(fullAi());
        service.diagnose(request("마포구", "연남동", "한식"));
        @SuppressWarnings("unchecked")
        Map<String, Object> body = captureBody();
        System.out.println("OBS BE02-001 body=" + body);
        assertEquals("마포구", body.get("district"));
        assertEquals("연남동", body.get("dong"));
        assertEquals("한식", body.get("industry"));
        assertEquals(Set.of("district", "dong", "industry"), body.keySet());
    }

    @Test
    @DisplayName("BE02-002")
    void be02_002() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("district", "마포구");
        Diagnosis saved = diagnose(request("종로구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-002 district=" + saved.getDistrict());
        assertEquals("마포구", saved.getDistrict());
    }

    @Test
    @DisplayName("BE02-003")
    void be02_003() throws Exception {
        ObjectNode ai = fullAi();
        ai.remove("district");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-003 district=" + saved.getDistrict());
        assertEquals("마포구", saved.getDistrict());
    }

    @Test
    @DisplayName("BE02-004")
    void be02_004() throws Exception {
        ObjectNode ai = fullAi();
        ai.remove("dong");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-004 dong=" + saved.getDong());
        assertEquals("연남동", saved.getDong());
    }

    @Test
    @DisplayName("BE02-005")
    void be02_005() throws Exception {
        ObjectNode ai = fullAi();
        ai.remove("industry");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-005 industry=" + saved.getIndustry());
        assertEquals("한식", saved.getIndustry());
    }

    @Test
    @DisplayName("BE02-006")
    void be02_006() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("quarter", "20244");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-006 quarter=" + saved.getQuarter());
        assertEquals("20244", saved.getQuarter());
    }

    @Test
    @DisplayName("BE02-007")
    void be02_007() throws Exception {
        assertDouble("BE02-007", "store_count", 25, saved -> saved.getStoreCount());
    }

    @Test
    @DisplayName("BE02-008")
    void be02_008() throws Exception {
        assertDouble("BE02-008", "open_rate", 3.4, Diagnosis::getOpenRate);
    }

    @Test
    @DisplayName("BE02-009")
    void be02_009() throws Exception {
        assertDouble("BE02-009", "close_rate", 6.2, Diagnosis::getCloseRate);
    }

    @Test
    @DisplayName("BE02-010")
    void be02_010() throws Exception {
        assertDouble("BE02-010", "franchise_ratio", 0.2, Diagnosis::getFranchiseRatio);
    }

    @Test
    @DisplayName("BE02-011")
    void be02_011() throws Exception {
        assertDouble("BE02-011", "foot_traffic", 3000, Diagnosis::getFootTraffic);
    }

    @Test
    @DisplayName("BE02-012")
    void be02_012() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("change_code", "HL");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-012 changeCode=" + saved.getChangeCode());
        assertEquals("HL", saved.getChangeCode());
    }

    @Test
    @DisplayName("BE02-013")
    void be02_013() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("change_name", "상권축소");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-013 changeName=" + saved.getChangeName());
        assertEquals("상권축소", saved.getChangeName());
    }

    @Test
    @DisplayName("BE02-014")
    void be02_014() throws Exception {
        assertDouble("BE02-014", "operate_months", 23.1, Diagnosis::getOperateMonths);
    }

    @Test
    @DisplayName("BE02-015")
    void be02_015() throws Exception {
        assertDouble("BE02-015", "sales_per_store", 800.5, Diagnosis::getSalesPerStore);
    }

    @Test
    @DisplayName("BE02-016")
    void be02_016() throws Exception {
        assertDouble("BE02-016", "ml_close_rate", 5.1, Diagnosis::getMlCloseRate);
    }

    @Test
    @DisplayName("BE02-017")
    void be02_017() throws Exception {
        assertDouble("BE02-017", "dl_sales_per_store", 730.5, Diagnosis::getDlSalesPerStore);
    }

    @Test
    @DisplayName("BE02-018")
    void be02_018() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("status", "danger");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-018 status=" + saved.getStatus());
        assertEquals("danger", saved.getStatus());
    }

    @Test
    @DisplayName("BE02-019")
    void be02_019() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("is_danger", true);
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-019 danger=" + saved.isDanger());
        assertTrue(saved.isDanger());
    }

    @Test
    @DisplayName("BE02-020")
    void be02_020() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("explanation", "기본 설명");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-020 explanation=" + saved.getExplanation());
        assertEquals("기본 설명", saved.getExplanation());
    }

    @Test
    @DisplayName("BE02-021")
    void be02_021() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("explanation_source", "basic");
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        System.out.println("OBS BE02-021 source=" + saved.getExplanationSource());
        assertEquals("basic", saved.getExplanationSource());
    }

    @Test
    @DisplayName("BE02-022")
    void be02_022() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("close_rate", "5.0");
        long before = repository.count();
        try {
            Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
            System.out.println("OBS BE02-022 closeRate=" + saved.getCloseRate() + " id=" + saved.getId());
            assertNull(saved.getCloseRate(), "문자열 숫자가 숫자로 저장됨");
            fail("null 처리만 하고 결측 보완/거절 없이 저장 id=" + saved.getId() + " closeRate=" + saved.getCloseRate());
        } catch (ApiException | IllegalArgumentException ex) {
            System.out.println("OBS BE02-022 rejected=" + ex.getMessage());
            assertEquals(before, repository.count());
        }
    }

    @Test
    @DisplayName("BE02-023")
    void be02_023() throws Exception {
        given(aiClient.diagnose(anyMap())).willReturn(objectMapper.readTree("{}"));
        long before = repository.count();
        try {
            Diagnosis saved = service.diagnose(request("마포구", "연남동", "한식"));
            System.out.println("OBS BE02-023 saved id=" + saved.getId()
                    + " status='" + saved.getStatus() + "' closeRate=" + saved.getCloseRate()
                    + " danger=" + saved.isDanger());
            fail("빈 AI 응답을 성공 저장 id=" + saved.getId()
                    + " status='" + saved.getStatus() + "' closeRate=" + saved.getCloseRate());
        } catch (ApiException | IllegalArgumentException ex) {
            System.out.println("OBS BE02-023 rejected=" + ex.getMessage());
            assertEquals(before, repository.count());
        }
    }

    @Test
    @DisplayName("BE02-024")
    void be02_024() throws Exception {
        ObjectNode ai = fullAi();
        ai.put("explanation", "가".repeat(4000));
        long before = repository.count();
        try {
            Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
            int len = saved.getExplanation() == null ? -1 : saved.getExplanation().length();
            System.out.println("OBS BE02-024 length=" + len);
            assertTrue(len > 0 && len <= 2000, "절단/검증 없이 저장 length=" + len);
        } catch (ApiException | IllegalArgumentException ex) {
            System.out.println("OBS BE02-024 rejected=" + ex.getClass().getSimpleName());
            assertEquals(before, repository.count());
        } catch (DataAccessException ex) {
            String message = ex.getMostSpecificCause() == null ? ex.getMessage() : ex.getMostSpecificCause().getMessage();
            System.out.println("OBS BE02-024 dbError=" + ex.getClass().getSimpleName() + " " + message);
            fail("DB 길이 초과가 검증·절단보다 먼저 발생: " + ex.getClass().getSimpleName() + " " + brief(message));
        }
    }

    @Test
    @DisplayName("BE02-025")
    void be02_025() {
        given(aiClient.diagnose(anyMap())).willThrow(ApiException.aiError("AI 서버 호출에 실패했습니다.", new IllegalStateException("down")));
        long before = repository.count();
        ApiException ex = assertThrows(ApiException.class, () -> service.diagnose(request("마포구", "연남동", "한식")));
        System.out.println("OBS BE02-025 error=" + ex.getErrorCode() + " count=" + repository.count());
        assertEquals(before, repository.count());
        assertEquals(HttpStatus.BAD_GATEWAY, ex.getStatus());
    }

    @Test
    @DisplayName("BE02-026")
    void be02_026() throws Exception {
        restartAt(1);
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), fullAi());
        Diagnosis found = service.get(1L);
        System.out.println("OBS BE02-026 id=" + found.getId() + " dong=" + found.getDong());
        assertEquals(1L, saved.getId());
        assertEquals(saved.getId(), found.getId());
        assertEquals("연남동", found.getDong());
        assertEquals("한식", found.getIndustry());
    }

    @Test
    @DisplayName("BE02-027")
    void be02_027() {
        ApiException ex = assertThrows(ApiException.class, () -> service.get(9999999L));
        System.out.println("OBS BE02-027 status=" + ex.getStatus().value() + " code=" + ex.getErrorCode());
        assertEquals(HttpStatus.NOT_FOUND, ex.getStatus());
        assertEquals("NOT_FOUND", ex.getErrorCode());
    }

    @Test
    @DisplayName("BE02-028")
    void be02_028() throws Exception {
        List<Long> ids = new ArrayList<>();
        for (int i = 1; i <= 12; i++) {
            ObjectNode ai = fullAi();
            ai.put("dong", "동" + i);
            ids.add(diagnose(request("마포구", "동" + i, "한식"), ai).getId());
        }
        List<Diagnosis> recent = service.recent();
        System.out.println("OBS BE02-028 size=" + recent.size() + " first=" + recent.get(0).getId()
                + " last=" + recent.get(recent.size() - 1).getId());
        assertEquals(10, recent.size());
        for (int i = 0; i < recent.size() - 1; i++) {
            assertTrue(recent.get(i).getId() > recent.get(i + 1).getId());
        }
        assertEquals(ids.get(ids.size() - 1), recent.get(0).getId());
        assertTrue(recent.stream().noneMatch(item -> item.getId().equals(ids.get(0))));
        assertTrue(recent.stream().noneMatch(item -> item.getId().equals(ids.get(1))));
    }

    @Test
    @DisplayName("BE02-029")
    void be02_029() throws Exception {
        given(aiClient.diagnose(anyMap())).willAnswer(invocation -> {
            @SuppressWarnings("unchecked")
            Map<String, Object> body = invocation.getArgument(0);
            ObjectNode ai = fullAi();
            ai.put("district", String.valueOf(body.get("district")));
            ai.put("dong", String.valueOf(body.get("dong")));
            ai.put("industry", String.valueOf(body.get("industry")));
            return ai;
        });
        ExecutorService pool = Executors.newFixedThreadPool(10);
        try {
            List<Future<Diagnosis>> futures = new ArrayList<>();
            for (int i = 0; i < 10; i++) {
                int n = i;
                futures.add(pool.submit(() -> service.diagnose(request("마포구", "병렬" + n, "한식"))));
            }
            Set<Long> ids = new HashSet<>();
            for (Future<Diagnosis> future : futures) {
                Diagnosis saved = future.get(10, TimeUnit.SECONDS);
                assertTrue(ids.add(saved.getId()), "중복 id=" + saved.getId());
            }
            System.out.println("OBS BE02-029 ids=" + ids.size() + " rows=" + repository.count());
            assertEquals(10, ids.size());
            assertEquals(10, repository.count());
        } finally {
            pool.shutdownNow();
        }
    }

    @Test
    @DisplayName("BE02-030")
    void be02_030() {
        given(aiClient.diagnose(anyMap())).willThrow(ApiException.aiError(
                "AI 서버 호출에 실패했습니다.",
                new IllegalStateException("HTTP 404")));
        long before = repository.count();
        ApiException ex = assertThrows(ApiException.class, () -> service.diagnose(request("없는구", "없는동", "한식")));
        System.out.println("OBS BE02-030 code=" + ex.getErrorCode() + " rows=" + repository.count());
        assertEquals(before, repository.count());
        assertTrue(ex.getStatus().is4xxClientError() || ex.getStatus().is5xxServerError());
    }

    private Diagnosis diagnose(DiagnosisRequest request, JsonNode ai) {
        given(aiClient.diagnose(anyMap())).willReturn(ai);
        return service.diagnose(request);
    }

    private void assertDouble(String id, String field, double expected, java.util.function.Function<Diagnosis, Double> reader) throws Exception {
        ObjectNode ai = fullAi();
        ai.put(field, expected);
        Diagnosis saved = diagnose(request("마포구", "연남동", "한식"), ai);
        Double actual = reader.apply(saved);
        System.out.println("OBS " + id + " " + field + "=" + actual);
        assertNotNull(actual);
        assertEquals(expected, actual, 0.0001);
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> captureBody() {
        org.mockito.ArgumentCaptor<Map<String, Object>> captor = org.mockito.ArgumentCaptor.forClass(Map.class);
        verify(aiClient).diagnose(captor.capture());
        return captor.getValue();
    }

    private ObjectNode fullAi() throws Exception {
        return (ObjectNode) objectMapper.readTree("""
                {"district":"마포구","dong":"연남동","industry":"한식","quarter":"20244",
                 "store_count":25,"open_rate":3.4,"close_rate":6.2,"franchise_ratio":0.2,
                 "foot_traffic":3000,"change_code":"HL","change_name":"상권축소",
                 "operate_months":23.1,"sales_per_store":800.5,
                 "ml_close_rate":5.1,"dl_sales_per_store":730.5,
                 "status":"danger","is_danger":true,
                 "explanation":"기본 설명","explanation_source":"basic"}
                """);
    }

    private static DiagnosisRequest request(String district, String dong, String industry) {
        DiagnosisRequest request = new DiagnosisRequest();
        request.setDistrict(district);
        request.setDong(dong);
        request.setIndustry(industry);
        return request;
    }

    private void restartAt(int id) {
        repository.deleteAll();
        jdbcTemplate.execute("ALTER TABLE diagnosis ALTER COLUMN id RESTART WITH " + id);
    }

    private static String brief(String value) {
        if (value == null) {
            return "null";
        }
        String one = value.replaceAll("\\s+", " ");
        return one.length() > 180 ? one.substring(0, 180) : one;
    }
}
