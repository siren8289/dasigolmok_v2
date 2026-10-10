package com.dasigolmok.diagnosis.repository;

import com.dasigolmok.diagnosis.entity.Diagnosis;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

/** 메서드 이름만 적으면 Spring Data JPA가 SQL을 만들어 준다. */
public interface DiagnosisRepository extends JpaRepository<Diagnosis, Long> {

    List<Diagnosis> findTop10ByOrderByIdDesc();
}
