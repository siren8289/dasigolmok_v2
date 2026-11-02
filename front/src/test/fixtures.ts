import { vi } from "vitest";
import type { Diagnosis, Options, Recommendation } from "../api/api";

export const OPTIONS: Options = {
  districts: ["강남구", "마포구"],
  dongs: [
    { district: "마포구", dong: "연남동", dong_code: "11440660" },
    { district: "마포구", dong: "망원동", dong_code: "11440670" },
    { district: "강남구", dong: "역삼동", dong_code: "11680640" },
    { district: "강남구", dong: "삼성동", dong_code: "11680580" },
  ],
  industries: [
    { industry: "한식음식점", industry_code: "CS100001" },
    { industry: "커피-음료", industry_code: "CS100002" },
  ],
};

export function diagnosis(over: Partial<Diagnosis> = {}): Diagnosis {
  return {
    id: 12,
    district: "마포구",
    dong: "연남동",
    industry: "한식음식점",
    quarter: "20254",
    storeCount: 30,
    openRate: 2.1,
    closeRate: 5.6,
    franchiseRatio: 0.1,
    footTraffic: 1099.9,
    changeCode: "HL",
    changeName: "상권축소",
    operateMonths: 40,
    salesPerStore: 500,
    mlCloseRate: 7.34,
    dlSalesPerStore: 650.2,
    status: "stable",
    danger: false,
    explanation: "한 줄\n두 줄",
    explanationSource: "basic",
    ...over,
  };
}

export function industryItem(over: Partial<Recommendation["all_industries"][number]> = {}) {
  return {
    industry: "한식음식점",
    store_count: 10,
    close_rate: 3,
    ml_close_rate: 4.2,
    dl_sales_per_store: 620.1,
    change_name: "상권축소",
    status: "stable",
    is_danger: false,
    score: 1,
    ...over,
  };
}

export function recommendation(over: Partial<Recommendation> = {}): Recommendation {
  return {
    district: "마포구",
    dong: "연남동",
    change_name: "상권축소",
    recommendations: [industryItem()],
    all_industries: [
      industryItem(),
      industryItem({ industry: "커피-음료", status: "warning", ml_close_rate: 5, dl_sales_per_store: 400 }),
      industryItem({ industry: "호프-간이주점", status: "danger", ml_close_rate: 9, dl_sales_per_store: 300 }),
    ],
    ...over,
  };
}

export function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

export function htmlResponse(status: number, body = "<html>err</html>"): Response {
  return new Response(body, { status, headers: { "Content-Type": "text/html" } });
}

export function installFetch(
  handler: (url: string, init?: RequestInit) => Promise<Response> | Response,
) {
  const fn = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    return handler(String(input), init);
  });
  vi.stubGlobal("fetch", fn);
  return fn;
}
