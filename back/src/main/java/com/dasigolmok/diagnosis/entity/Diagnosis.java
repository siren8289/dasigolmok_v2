package com.dasigolmok.diagnosis.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;

/**
 * 진단 기록 1건 = diagnosis 테이블의 한 줄.
 * 사용자 선택값과 AI 결과를 함께 저장해서, 나중에 결과 화면을 다시 볼 수 있게 한다.
 */
@Entity
@Table(name = "diagnosis")
public class Diagnosis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String district;
    private String dong;
    private String industry;
    private String quarter;

    private Double storeCount;
    private Double openRate;
    private Double closeRate;
    private Double franchiseRatio;
    private Double footTraffic;
    private String changeCode;
    private String changeName;
    private Double operateMonths;
    private Double salesPerStore;

    private Double mlCloseRate;
    private Double dlSalesPerStore;
    private String status;
    private boolean danger;

    @Column(length = 2000)
    private String explanation;
    private String explanationSource;

    private LocalDateTime createdAt = LocalDateTime.now();

    public Diagnosis() {
    }

    public Long getId() { return id; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getDong() { return dong; }
    public void setDong(String dong) { this.dong = dong; }

    public String getIndustry() { return industry; }
    public void setIndustry(String industry) { this.industry = industry; }

    public String getQuarter() { return quarter; }
    public void setQuarter(String quarter) { this.quarter = quarter; }

    public Double getStoreCount() { return storeCount; }
    public void setStoreCount(Double storeCount) { this.storeCount = storeCount; }

    public Double getOpenRate() { return openRate; }
    public void setOpenRate(Double openRate) { this.openRate = openRate; }

    public Double getCloseRate() { return closeRate; }
    public void setCloseRate(Double closeRate) { this.closeRate = closeRate; }

    public Double getFranchiseRatio() { return franchiseRatio; }
    public void setFranchiseRatio(Double franchiseRatio) { this.franchiseRatio = franchiseRatio; }

    public Double getFootTraffic() { return footTraffic; }
    public void setFootTraffic(Double footTraffic) { this.footTraffic = footTraffic; }

    public String getChangeCode() { return changeCode; }
    public void setChangeCode(String changeCode) { this.changeCode = changeCode; }

    public String getChangeName() { return changeName; }
    public void setChangeName(String changeName) { this.changeName = changeName; }

    public Double getOperateMonths() { return operateMonths; }
    public void setOperateMonths(Double operateMonths) { this.operateMonths = operateMonths; }

    public Double getSalesPerStore() { return salesPerStore; }
    public void setSalesPerStore(Double salesPerStore) { this.salesPerStore = salesPerStore; }

    public Double getMlCloseRate() { return mlCloseRate; }
    public void setMlCloseRate(Double mlCloseRate) { this.mlCloseRate = mlCloseRate; }

    public Double getDlSalesPerStore() { return dlSalesPerStore; }
    public void setDlSalesPerStore(Double dlSalesPerStore) { this.dlSalesPerStore = dlSalesPerStore; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public boolean isDanger() { return danger; }
    public void setDanger(boolean danger) { this.danger = danger; }

    public String getExplanation() { return explanation; }
    public void setExplanation(String explanation) { this.explanation = explanation; }

    public String getExplanationSource() { return explanationSource; }
    public void setExplanationSource(String explanationSource) { this.explanationSource = explanationSource; }

    public LocalDateTime getCreatedAt() { return createdAt; }
}
