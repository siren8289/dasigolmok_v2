package com.dasigolmok.domain.area.service;

import com.dasigolmok.domain.area.dto.AreaContextResponse;
import com.dasigolmok.domain.area.repository.AreaContextQueryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class AreaContextService {

    private final AreaContextQueryRepository areaContextQueryRepository;

    /**
     * Optional Area Context for Story detail. Failures never affect the Story path.
     */
    public AreaContextResponse findForPlace(String placeId) {
        if (placeId == null || placeId.isBlank()) {
            return null;
        }
        try {
            return areaContextQueryRepository.findByPlaceId(placeId).orElse(null);
        } catch (Exception e) {
            log.warn("Area context unavailable for placeId={} (graceful degradation)", placeId, e);
            return null;
        }
    }
}
