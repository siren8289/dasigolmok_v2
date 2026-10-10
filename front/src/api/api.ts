// Spring 서버와 통신하는 함수를 한 곳에 모았다.

const API_URL: string = import.meta.env.VITE_API_URL ?? "http://localhost:8080";

export type DongOption = {
  district: string;
  dong: string;
  dong_code: string;
};

export type IndustryOption = {
  industry: string;
  industry_code: string;
};

export type Options = {
  districts: string[];
  dongs: DongOption[];
  industries: IndustryOption[];
};

export type DiagnoseInput = {
  district: string;
  dong: string;
  industry: string;
};

export type Diagnosis = DiagnoseInput & {
  id: number;
  quarter: string;
  storeCount: number;
  openRate: number;
  closeRate: number;
  franchiseRatio: number;
  footTraffic: number;
  changeCode: string;
  changeName: string;
  operateMonths: number;
  salesPerStore: number;
  mlCloseRate: number;
  dlSalesPerStore: number;
  status: string;
  danger: boolean;
  explanation: string;
  explanationSource: string;
};

export type IndustryItem = {
  industry: string;
  store_count: number;
  close_rate: number;
  ml_close_rate: number;
  dl_sales_per_store: number;
  change_name: string;
  status: string;
  is_danger: boolean;
  score: number;
};

export type Recommendation = {
  district: string;
  dong: string;
  change_name: string;
  recommendations: IndustryItem[];
  all_industries: IndustryItem[];
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(API_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let message = "요청에 실패했습니다.";
    try {
      const body = await response.json();
      message = body.message ?? body.detail ?? message;
    } catch {
      // JSON이 아니면 기본 문장을 쓴다.
    }
    throw new Error(message);
  }
  return response.json();
}

export function getOptions() {
  return request<Options>("/api/options");
}

export function createDiagnosis(input: DiagnoseInput) {
  return request<Diagnosis>("/api/diagnoses", { method: "POST", body: JSON.stringify(input) });
}

export function getDiagnosis(id: string) {
  return request<Diagnosis>(`/api/diagnoses/${id}`);
}

export function getRecommendations(input: { district: string; dong: string }) {
  return request<Recommendation>("/api/recommendations", {
    method: "POST",
    body: JSON.stringify(input),
  });
}
