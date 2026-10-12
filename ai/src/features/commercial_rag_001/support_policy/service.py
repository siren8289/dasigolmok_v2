"""창업 지원 정책 검색 및 조건 확인(Support Policy Search) 서비스.

소상공인 및 창업 지원사업의 모집 기간, 지원 지역, 대상 업종을 정밀하게 필터링합니다.
종료된(마감된) 지원사업을 신청 가능하다고 잘못 안내하지 않도록 기간을 엄격하게 판정합니다.
"""
from datetime import datetime
from typing import List, Optional
import re

from src.features.commercial_rag_001.schemas import (
    SupportPolicyItem,
    SupportPolicyQuery,
    SupportPolicyResponse,
)

# [무엇을 하는지] 서울시 및 주요 자치구 창업 지원사업 원본 목록을 정의합니다.
# [왜 필요한지] 자치구별, 업종별 최신 지원금 및 마감된 지원사업을 판별하기 위한 데이터셋입니다.
POLICY_DATABASE = [
    {
        "id": "pol-seoul-safe-loan-2026",
        "title": "2026년 서울시 소상공인 안심창업 특별자금 지원",
        "organization": "서울신용보증재단",
        "target_district": None,  # 서울시 전역
        "target_industry": None,  # 전업종
        "start_date": "2026-01-05",
        "end_date": "2026-12-31",
        "support_amount": "최대 5,000만원 융자 (이차보전 2.0% 지원)",
        "description": "예비창업자 및 6개월 이내 초기창업자를 위한 저금리 특별 보증 대출",
        "eligibility": "서울시 내 사업자등록 예정인 예비창업자 또는 6개월 이내 창업자",
        "source_url": "https://www.seoulshinbo.co.kr",
    },
    {
        "id": "pol-mapo-youth-startup-2026",
        "title": "2026년 마포구 골목상권 활성화 청년창업 원스톱 지원사업",
        "organization": "마포구청 일자리경제과",
        "target_district": "마포구",
        "target_industry": "한식음식점, 커피-음료, 기타외식업",
        "start_date": "2026-03-01",
        "end_date": "2026-11-30",
        "support_amount": "최대 1,000만원 시설·간판 개선 무상 보조금 + 1:1 컨설팅",
        "description": "마포구 골목상권(연남동, 망원동, 서교동 등) 내 음식점 및 카페 창업 청년 대상 무상 보조금 지원",
        "eligibility": "마포구 내 점포 개업을 준비하는 만 19세~39세 예비 청년 창업가",
        "source_url": "https://www.mapo.go.kr",
    },
    {
        "id": "pol-gangnam-incubating-2026",
        "title": "2026년 강남구 스타트업 및 소상공인 사업화 촉진 지원사업",
        "organization": "강남구청 지역경제과",
        "target_district": "강남구",
        "target_industry": None,  # 전업종
        "start_date": "2026-01-15",
        "end_date": "2026-12-15",
        "support_amount": "점포 임차료 월 50만원 지원(최대 6개월) + 디지털 마케팅비",
        "description": "강남구 오피스 및 골목상권 신규 사업자를 위한 초기 임차료 지원",
        "eligibility": "강남구 관내 신규 사업자등록 예정자 및 1년 미만 소상공인",
        "source_url": "https://www.gangnam.go.kr",
    },
    {
        "id": "pol-seoul-smart-store-2026",
        "title": "2026년 서울시 스마트상점 기술보급 외식업 특별지원",
        "organization": "소상공인시장진흥공단",
        "target_district": None,
        "target_industry": "한식음식점, 중식음식점, 일식음식점, 양식음식점, 커피-음료",
        "start_date": "2026-02-01",
        "end_date": "2026-10-31",
        "support_amount": "키오스크·테이블오더·서빙로봇 도입 비용 최대 500만원(공급가액의 70%) 지원",
        "description": "외식업 소상공인의 인건비 절감과 매장 운영 효율화를 위한 스마트 기기 보급",
        "eligibility": "서울시 관내 일반음식점 및 휴게음식점 운영(예정) 소상공인",
        "source_url": "https://www.semas.or.kr",
    },
    {
        "id": "pol-seoul-closed-special-2024",
        "title": "[종료] 2024년 서울시 청년 희망창업 특례보증 특별지원",
        "organization": "서울신용보증재단",
        "target_district": None,
        "target_industry": None,
        "start_date": "2024-01-15",
        "end_date": "2024-06-30",
        "support_amount": "최대 3,000만원 무이자 대출 (접수 마감)",
        "description": "2024년 상반기 한시 지원사업으로 현재 모든 접수가 마감되었습니다.",
        "eligibility": "접수 마감 (신청 불가)",
        "source_url": "https://www.seoulshinbo.co.kr",
    },
    {
        "id": "pol-mapo-closed-localbrand-2025",
        "title": "[종료] 2025년 상반기 마포 로컬브랜드 상권 도약 패키지 지원사업",
        "organization": "마포구 상권활성화재단",
        "target_district": "마포구",
        "target_industry": None,
        "start_date": "2025-01-10",
        "end_date": "2025-04-30",
        "support_amount": "최대 2,000만원 사업화 지원금 (접수 마감)",
        "description": "2025년 4월 30일부로 접수 마감된 종료 사업입니다.",
        "eligibility": "접수 마감 (신청 불가)",
        "source_url": "https://www.mapo.go.kr",
    },
]


def check_policy_status(start_date_str: str, end_date_str: str, target_date_str: Optional[str] = None) -> tuple[str, bool]:
    """[무엇을 하는지] 정책의 시작일, 종료일과 기준 날짜를 비교해 상태(open/closed/upcoming)와 신청 가능 여부를 계산합니다.

    [왜 필요한지] 마감된 지원사업을 신청 가능하다고 잘못 안내하는 심각한 오안내를 원천 방지하기 위함입니다.
    """
    if target_date_str:
        try:
            today = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        except ValueError:
            today = datetime.now().date()
    else:
        today = datetime.now().date()

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        # 날짜 형식이 올바르지 않으면 안전하게 마감 처리
        return "closed", False

    if today < start_date:
        return "upcoming", False
    elif today > end_date:
        return "closed", False
    else:
        return "open", True


def get_all_policy_items(target_date: Optional[str] = None) -> List[SupportPolicyItem]:
    """[무엇을 하는지] 원본 정책 데이터를 읽어 기준 날짜 기준의 상태(open/closed)가 반영된 SupportPolicyItem 목록을 만듭니다.

    [왜 필요한지] 모든 지원 정책에 일관된 날짜 검증 규칙을 적용하기 위함입니다.
    """
    items: List[SupportPolicyItem] = []
    for p in POLICY_DATABASE:
        status, is_open = check_policy_status(p["start_date"], p["end_date"], target_date)
        item = SupportPolicyItem(
            id=p["id"],
            title=p["title"],
            organization=p["organization"],
            target_district=p["target_district"],
            target_industry=p["target_industry"],
            start_date=p["start_date"],
            end_date=p["end_date"],
            status=status,
            is_open=is_open,
            support_amount=p.get("support_amount"),
            description=p["description"],
            eligibility=p.get("eligibility"),
            source_url=p.get("source_url"),
            score=0.0,
        )
        items.append(item)
    return items


def search_policies(query_obj: SupportPolicyQuery) -> SupportPolicyResponse:
    """[무엇을 하는지] 지역, 업종, 신청 가능 여부, 검색 키워드에 따라 맞춤 창업 지원 정책을 검색합니다.

    [왜 필요한지] 사장님이 본인의 지역과 업종에 해당하며 '지금 실제로 신청 가능한' 혜택만 정확하게 확인할 수 있도록 돕기 위함입니다.
    """
    all_policies = get_all_policy_items(query_obj.target_date)
    filtered: List[SupportPolicyItem] = []

    tokens = set(re.findall(r"[\w가-힣]+", query_obj.query.lower())) if query_obj.query else set()

    for policy in all_policies:
        # 1. 종료 정책 필터: only_open이 True이면 마감되거나 아직 시작 안 한 공고는 제외
        if query_obj.only_open and not policy.is_open:
            continue

        # 2. 지역 필터: 정책의 대상 지역이 지정되어 있고, 요청 지역과 다르면 제외
        if query_obj.district and policy.target_district:
            if query_obj.district not in policy.target_district:
                continue

        # 3. 업종 필터: 정책의 대상 업종이 지정되어 있고, 요청 업종과 다르면 제외
        if query_obj.industry and policy.target_industry:
            if query_obj.industry not in policy.target_industry:
                continue

        # 4. 키워드 적합도 점수 계산
        score = 1.0  # 기본 적합도
        if policy.target_district and query_obj.district and query_obj.district in policy.target_district:
            score += 0.5  # 관할 자치구 맞춤 정책 우대
        if policy.target_industry and query_obj.industry and query_obj.industry in policy.target_industry:
            score += 0.5  # 맞춤 업종 우대

        if tokens:
            full_text = f"{policy.title} {policy.description} {policy.organization}".lower()
            policy_tokens = set(re.findall(r"[\w가-힣]+", full_text))
            overlap = tokens.intersection(policy_tokens)
            score += len(overlap) * 0.3

        policy_copy = policy.model_copy()
        policy_copy.score = round(score, 2)
        filtered.append(policy_copy)

    # 점수 높은 순으로 정렬
    filtered.sort(key=lambda p: p.score or 0.0, reverse=True)
    results = filtered[:query_obj.top_k]

    return SupportPolicyResponse(
        policies=results,
        total_count=len(results),
    )
