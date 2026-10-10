"""데이터 파이프라인 실행: 수집 → 전처리 → 저장

사용법 (저장소 루트에서)
    python -m data.etl.run
    python -m data.etl.run --skip-download   # 이미 raw/ 가 있을 때
"""
import argparse

from data.etl.fetch import (
    fetch_semas_dongs,
    fetch_semas_stores,
    fetch_semas_upjong,
    fetch_seoul_table,
)
from data.etl.load import (
    load_raw_table,
    save_json,
    save_processed,
    save_raw_json,
    save_raw_table,
)
from data.etl.transform import (
    clean_change,
    clean_pop,
    clean_sales,
    clean_store,
    make_dong_stats,
    make_options,
    merge_tables,
)


def _get_seoul(key, skip_download):
    """서울시 표를 받거나, 이미 받아 둔 파일을 읽는다."""
    if skip_download:
        cached = load_raw_table(key)
        if cached is not None:
            print(f"  캐시 사용: {key} ({len(cached)}행)")
            return cached
    table = fetch_seoul_table(key)
    save_raw_table(table, key)
    return table


def _try_semas():
    """소상공인 API. 인증키가 없거나 실패하면 빈 목록으로 넘어간다."""
    try:
        print("  소상공인 API: 업종")
        large, middle = fetch_semas_upjong()
        save_raw_json(large + middle, "semas_upjong")

        print("  소상공인 API: 서울 행정동")
        dongs = fetch_semas_dongs()
        save_raw_json(dongs, "semas_dongs")

        print("  소상공인 API: 샘플 업소 (역삼1동)")
        stores = fetch_semas_stores()
        save_raw_json(stores, "semas_stores_sample")
        return large, dongs
    except Exception as error:
        print(f"  소상공인 API를 건너뜁니다: {error}")
        return [], []


def run(skip_download=False):
    print("[1/3] 수집")
    large, dongs = _try_semas()

    raw_store = _get_seoul("store", skip_download)
    raw_sales = _get_seoul("sales", skip_download)
    raw_pop = _get_seoul("pop", skip_download)
    raw_change = _get_seoul("change", skip_download)

    print("[2/3] 전처리")
    store = clean_store(raw_store)
    sales = clean_sales(raw_sales)
    pop = clean_pop(raw_pop)
    change = clean_change(raw_change)
    print(f"  점포 {len(store)} / 매출 {len(sales)} / 유동인구 {len(pop)} / 변화지표 {len(change)}")

    train = merge_tables(store, sales, pop, change)
    stats = make_dong_stats(train)
    options = make_options(train, dongs, large)
    print(f"  학습용 {len(train)}행, 최신 통계 {len(stats)}행, 행정동 {len(options['dongs'])}개")

    print("[3/3] 저장")
    print("  ", save_processed(train, "train"))
    print("  ", save_processed(stats, "dong_stats"))
    print("  ", save_json(options, "options"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="서울 골목 상권 공공데이터 수집·전처리")
    parser.add_argument("--skip-download", action="store_true", help="이미 받은 raw CSV 를 재사용")
    args = parser.parse_args()
    run(skip_download=args.skip_download)
