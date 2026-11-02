import { beforeEach, describe, expect, it, vi } from "vitest";
import { htmlResponse, installFetch, jsonResponse } from "./fixtures";
import { note } from "./note";

async function loadApi() {
  vi.resetModules();
  return import("../api/api");
}

beforeEach(() => {
  vi.unstubAllEnvs();
  vi.resetModules();
});

describe("FE05 HTTP 클라이언트", () => {
  it("FE05-001", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ ok: true }));
    const api = await loadApi();
    await api.getOptions();
    expect(String(fetchMock.mock.calls[0][0])).toBe("http://localhost:8080/api/options");
    note("FE05-001", "VITE_API_URL 미설정 시 fetch URL이 http://localhost:8080/api/options 이다.");
  });

  it("FE05-002", async () => {
    vi.stubEnv("VITE_API_URL", "");
    const fetchMock = installFetch(async () => jsonResponse({ ok: true }));
    const api = await loadApi();
    await api.getOptions();
    expect(String(fetchMock.mock.calls[0][0])).toBe("/api/options");
    note("FE05-002", "VITE_API_URL='' 이면 상대 경로 /api/options 로 현재 origin에 요청한다.");
  });

  it("FE05-003", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ districts: [], dongs: [], industries: [] }));
    const api = await loadApi();
    await api.getOptions();
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/options");
    expect((fetchMock.mock.calls[0][1] as RequestInit | undefined)?.method).toBeUndefined();
    note("FE05-003", "getOptions()는 GET /api/options 이다.");
  });

  it("FE05-004", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ id: 1 }));
    const api = await loadApi();
    await api.createDiagnosis({ district: "마포구", dong: "연남동", industry: "한식음식점" });
    const init = fetchMock.mock.calls[0][1] as RequestInit;
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/diagnoses");
    expect(init.method).toBe("POST");
    note("FE05-004", "createDiagnosis()는 POST /api/diagnoses 이다.");
  });

  it("FE05-005", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ id: 17 }));
    const api = await loadApi();
    await api.getDiagnosis("17");
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/diagnoses/17");
    note("FE05-005", "getDiagnosis('17')는 GET /api/diagnoses/17 이다.");
  });

  it("FE05-006", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ all_industries: [] }));
    const api = await loadApi();
    await api.getRecommendations({ district: "마포구", dong: "연남동" });
    const init = fetchMock.mock.calls[0][1] as RequestInit;
    expect(String(fetchMock.mock.calls[0][0])).toContain("/api/recommendations");
    expect(init.method).toBe("POST");
    note("FE05-006", "getRecommendations()는 POST /api/recommendations 이다.");
  });

  it("FE05-007", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ id: 1 }));
    const api = await loadApi();
    await api.createDiagnosis({ district: "마포구", dong: "연남동", industry: "한식음식점" });
    await api.getRecommendations({ district: "마포구", dong: "연남동" });
    for (const call of fetchMock.mock.calls) {
      const headers = new Headers((call[1] as RequestInit).headers);
      expect(headers.get("Content-Type")).toBe("application/json");
    }
    note("FE05-007", "POST 두 건 모두 Content-Type application/json 이다.");
  });

  it("FE05-008", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ id: 1 }));
    const api = await loadApi();
    await api.createDiagnosis({ district: "마포구", dong: "연남동", industry: "한식음식점" });
    expect((fetchMock.mock.calls[0][1] as RequestInit).body).toBe(
      JSON.stringify({ district: "마포구", dong: "연남동", industry: "한식음식점" }),
    );
    note("FE05-008", "한글 district/dong/industry가 JSON 문자열에 그대로 들어간다.");
  });

  it("FE05-009", async () => {
    installFetch(async () => jsonResponse({ districts: ["마포구"], dongs: [], industries: [] }, 200));
    const api = await loadApi();
    const data = await api.getOptions();
    expect(data.districts).toEqual(["마포구"]);
    note("FE05-009", "HTTP 200 JSON이 호출자에게 그대로 반환된다.");
  });

  it("FE05-010", async () => {
    installFetch(async () => jsonResponse({ id: 12, district: "마포구" }, 201));
    const api = await loadApi();
    const data = await api.createDiagnosis({ district: "마포구", dong: "연남동", industry: "한식음식점" });
    expect(data.id).toBe(12);
    note("FE05-010", "HTTP 201 JSON도 ok로 보고 data를 반환한다.");
  });

  it("FE05-011", async () => {
    installFetch(async () => jsonResponse({ message: "오류" }, 400));
    const api = await loadApi();
    await expect(api.getOptions()).rejects.toThrow("오류");
    note("FE05-011", "400 body.message '오류'가 Error message로 전달된다.");
  });

  it("FE05-012", async () => {
    installFetch(async () => jsonResponse({ detail: "검증 실패" }, 422));
    const api = await loadApi();
    await expect(api.getOptions()).rejects.toThrow("검증 실패");
    note("FE05-012", "message가 없으면 detail '검증 실패'를 쓴다.");
  });

  it("FE05-013", async () => {
    installFetch(async () => htmlResponse(500));
    const api = await loadApi();
    await expect(api.getOptions()).rejects.toThrow("요청에 실패했습니다.");
    note("FE05-013", "HTML 500은 기본 문구 '요청에 실패했습니다.'다.");
  });

  it("FE05-014", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw new Error("network down");
    }));
    const api = await loadApi();
    await expect(api.getOptions()).rejects.toThrow("network down");
    note("FE05-014", "fetch reject는 호출자 catch로 그대로 전파된다.");
  });

  it("FE05-015", async () => {
    installFetch(async () => new Response("", { status: 200, headers: { "Content-Type": "application/json" } }));
    const api = await loadApi();
    await expect(api.getOptions(), "빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다").rejects.toThrow("요청에 실패했습니다.");
  });

  it("FE05-016", async () => {
    vi.stubEnv("VITE_API_URL", "https://host/");
    const fetchMock = installFetch(async () => jsonResponse({ ok: true }));
    const api = await loadApi();
    await api.getOptions();
    const url = String(fetchMock.mock.calls[0][0]);
    expect(url, `실제 URL ${url}`).not.toContain("//api");
  });

  it("FE05-017", async () => {
    installFetch(async () => jsonResponse({ message: "token=SECRET-TOKEN-123 failed" }, 500));
    const api = await loadApi();
    try {
      await api.getOptions();
      expect.fail("오류가 발생해야 한다");
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      expect(message, `실제 메시지에 토큰이 남아 있다: ${message}`).not.toContain("SECRET-TOKEN-123");
    }
  });

  it("FE05-018", async () => {
    const fetchMock = installFetch(async () => jsonResponse({ message: "bad id" }, 400));
    const api = await loadApi();
    await api.getDiagnosis("1/../../").catch(() => undefined);
    const url = String(fetchMock.mock.calls[0][0]);
    expect(url, `실제 URL ${url}`).not.toContain("/../");
  });
});
