package com.dasigolmok.diagnosis;

import com.dasigolmok.ai.AiClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/** AI 서버는 가짜(Mock)로 바꾸고, Spring의 저장·조회 흐름만 확인한다. */
@SpringBootTest
@AutoConfigureMockMvc
class DiagnosisControllerTest {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    ObjectMapper objectMapper;

    @MockBean
    AiClient aiClient;

    private static final String REQUEST = """
            {"district":"마포구","dong":"연남동","industry":"한식음식점"}
            """;

    @Test
    void createAndGet() throws Exception {
        given(aiClient.diagnose(any())).willReturn(objectMapper.readTree("""
                {"district":"마포구","dong":"연남동","industry":"한식음식점","quarter":"20254",
                 "store_count":70,"open_rate":3.0,"close_rate":2.0,"franchise_ratio":0.1,
                 "foot_traffic":800000,"change_code":"LH","change_name":"상권확장",
                 "operate_months":90,"sales_per_store":1200.0,
                 "ml_close_rate":2.4,"dl_sales_per_store":1100.0,
                 "status":"stable","is_danger":false,
                 "explanation":"안정 단계입니다.","explanation_source":"basic"}
                """));

        mockMvc.perform(post("/api/diagnoses").contentType(MediaType.APPLICATION_JSON).content(REQUEST))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists())
                .andExpect(jsonPath("$.status").value("stable"))
                .andExpect(jsonPath("$.mlCloseRate").value(2.4));

        mockMvc.perform(get("/api/diagnoses"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].dong").value("연남동"));
    }

    @Test
    void blankDongReturns400() throws Exception {
        String bad = """
                {"district":"마포구","dong":"","industry":"한식음식점"}
                """;
        mockMvc.perform(post("/api/diagnoses").contentType(MediaType.APPLICATION_JSON).content(bad))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errorCode").value("VALIDATION_ERROR"));
    }
}
