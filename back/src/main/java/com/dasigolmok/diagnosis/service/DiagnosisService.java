package com.dasigolmok.diagnosis.service;

import com.dasigolmok.ai.AiClient;
import com.dasigolmok.diagnosis.dto.DiagnosisRequest;
import com.dasigolmok.diagnosis.entity.Diagnosis;
import com.dasigolmok.diagnosis.repository.DiagnosisRepository;
import com.dasigolmok.global.exception.ApiException;
import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 메인 기능 1: 골목 상권 진단
 *   1. 프론트 입력을 AI 서버에 보낸다
 *   2. AI 결과를 DB에 저장한다
 *   3. 저장된 결과를 돌려준다
 */
@Service
public class DiagnosisService {

    private final AiClient aiClient;
    private final DiagnosisRepository diagnosisRepository;

    public DiagnosisService(AiClient aiClient, DiagnosisRepository diagnosisRepository) {
        this.aiClient = aiClient;
        this.diagnosisRepository = diagnosisRepository;
    }

    public Diagnosis diagnose(DiagnosisRequest request) {
        Map<String, Object> body = new HashMap<>();
        body.put("district", request.getDistrict());
        body.put("dong", request.getDong());
        body.put("industry", request.getIndustry());
        JsonNode ai = aiClient.diagnose(body);

        Diagnosis diagnosis = new Diagnosis();
        diagnosis.setDistrict(ai.path("district").asText(request.getDistrict()));
        diagnosis.setDong(ai.path("dong").asText(request.getDong()));
        diagnosis.setIndustry(ai.path("industry").asText(request.getIndustry()));
        diagnosis.setQuarter(ai.path("quarter").asText(null));
        diagnosis.setStoreCount(readNumber(ai, "store_count"));
        diagnosis.setOpenRate(readNumber(ai, "open_rate"));
        diagnosis.setCloseRate(readNumber(ai, "close_rate"));
        diagnosis.setFranchiseRatio(readNumber(ai, "franchise_ratio"));
        diagnosis.setFootTraffic(readNumber(ai, "foot_traffic"));
        diagnosis.setChangeCode(ai.path("change_code").asText(null));
        diagnosis.setChangeName(ai.path("change_name").asText(null));
        diagnosis.setOperateMonths(readNumber(ai, "operate_months"));
        diagnosis.setSalesPerStore(readNumber(ai, "sales_per_store"));
        diagnosis.setMlCloseRate(readNumber(ai, "ml_close_rate"));
        diagnosis.setDlSalesPerStore(readNumber(ai, "dl_sales_per_store"));
        diagnosis.setStatus(ai.path("status").asText());
        diagnosis.setDanger(ai.path("is_danger").asBoolean());
        diagnosis.setExplanation(ai.path("explanation").asText());
        diagnosis.setExplanationSource(ai.path("explanation_source").asText());

        return diagnosisRepository.save(diagnosis);
    }

    public Diagnosis get(Long id) {
        Diagnosis diagnosis = diagnosisRepository.findById(id).orElse(null);
        if (diagnosis == null) {
            throw ApiException.notFound("진단 기록이 없습니다. id=" + id);
        }
        return diagnosis;
    }

    public List<Diagnosis> recent() {
        return diagnosisRepository.findTop10ByOrderByIdDesc();
    }

    private Double readNumber(JsonNode node, String field) {
        JsonNode value = node.path(field);
        if (value.isNumber()) {
            return value.asDouble();
        }
        return null;
    }
}
