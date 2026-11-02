import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import RecommendPage from "../pages/RecommendPage";
import { OPTIONS, industryItem, installFetch, jsonResponse, recommendation } from "./fixtures";
import { note } from "./note";

function renderPage() {
  return render(
    <MemoryRouter>
      <RecommendPage />
    </MemoryRouter>,
  );
}

function recommendPosts(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls.filter((call) => String(call[0]).includes("/api/recommendations"));
}

beforeEach(() => {
  installFetch(async (url) => {
    if (url.includes("/api/options")) return jsonResponse(OPTIONS);
    if (url.includes("/api/recommendations")) return jsonResponse(recommendation());
    throw new Error(url);
  });
});

describe("FE04 업종 추천", () => {
  it("FE04-001", async () => {
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    expect(screen.getByRole("combobox", { name: "자치구" })).toHaveValue("마포구");
    expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("연남동");
    note("FE04-001", "첫 진입 기본값은 마포구/연남동이다.");
  });

  it("FE04-002", async () => {
    const fetchMock = vi.mocked(fetch);
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    expect(fetchMock.mock.calls.filter((c) => String(c[0]).includes("/api/options"))).toHaveLength(1);
    note("FE04-002", "마운트 시 GET /api/options 가 호출된다.");
  });

  it("FE04-003", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "강남구" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    const labels = [...screen.getByRole("combobox", { name: "행정동" }).querySelectorAll("option")].map((o) => o.textContent);
    expect(labels).toEqual(["역삼동", "삼성동"]);
    note("FE04-003", "강남구 선택 후 동 목록이 역삼동·삼성동으로 다시 계산된다.");
  });

  it("FE04-004", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("역삼동"));
    note("FE04-004", "기존 연남동이 새 구에 없으면 첫 행정동 역삼동으로 바뀐다.");
  });

  it("FE04-005", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "망원동" });
    await user.selectOptions(screen.getByRole("combobox", { name: "행정동" }), "망원동");
    expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("망원동");
    note("FE04-005", "현재 동이 마포구 목록에 있으면 망원동 선택을 유지한다.");
  });

  it("FE04-006", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.mocked(fetch);
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    await waitFor(() => expect(recommendPosts(fetchMock)).toHaveLength(1));
    const init = recommendPosts(fetchMock)[0][1] as RequestInit;
    expect(init.method).toBe("POST");
    expect(JSON.parse(String(init.body))).toEqual({ district: "마포구", dong: "연남동" });
    note("FE04-006", "POST /api/recommendations 에 마포구/연남동이 전송된다.");
  });

  it("FE04-007", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return new Promise<Response>(() => {});
    });
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    const button = screen.getByRole("button", { name: "업종을 계산하는 중..." });
    expect(button).toBeDisabled();
    note("FE04-007", "지연 중 버튼이 disabled이고 문구는 '업종을 계산하는 중...'이다.");
  });

  it("FE04-008", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("button", { name: "추천 받기" });
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("한식음식점")).toBeInTheDocument();
    expect(screen.getByText("커피-음료")).toBeInTheDocument();
    expect(screen.getByText("호프-간이주점")).toBeInTheDocument();
    expect(screen.getAllByRole("row")).toHaveLength(4);
    note("FE04-008", "all_industries 3개가 헤더 1행 + 본문 3행으로 표시된다.");
  });

  it("FE04-009", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse(recommendation({ all_industries: [], recommendations: [] }));
    });
    renderPage();
    await screen.findByRole("button", { name: "추천 받기" });
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    await screen.findByText("연남동 · 상권축소");
    const guide = screen.queryByText(/추천 결과가 없|업종이 없습니다|빈 목록/);
    expect(guide, "빈 all_industries에 대한 안내 문구가 없다").not.toBeNull();
  });

  it("FE04-010", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    const badge = await screen.findByText("안정");
    expect(badge.className).toContain("bg-emerald-100");
    note("FE04-010", "status=stable 행에 안정 뱃지가 있다.");
  });

  it("FE04-011", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    const badge = await screen.findByText("주의");
    expect(badge.className).toContain("bg-amber-100");
    note("FE04-011", "status=warning 행에 주의 뱃지가 있다.");
  });

  it("FE04-012", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    const badge = await screen.findByText("위험");
    expect(badge.className).toContain("bg-red-100");
    note("FE04-012", "status=danger 행에 위험 뱃지가 있다.");
  });

  it("FE04-013", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse(recommendation({ all_industries: [industryItem({ industry: "기타", status: "OTHER" })] }));
    });
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    const badge = await screen.findByText("판단 불가");
    expect(badge.className).toContain("bg-gray-100");
    note("FE04-013", "status=OTHER 는 판단 불가 뱃지로 떨어진다.");
  });

  it("FE04-014", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("4.2%")).toBeInTheDocument();
    note("FE04-014", "ml_close_rate 4.2가 '4.2%'로 표시된다.");
  });

  it("FE04-015", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("620.1만원")).toBeInTheDocument();
    note("FE04-015", "dl_sales_per_store 620.1이 '620.1만원'으로 표시된다.");
  });

  it("FE04-016", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("연남동 · 상권축소")).toBeInTheDocument();
    note("FE04-016", "결과 헤더에 행정동과 상권변화명이 함께 있다.");
  });

  it("FE04-017", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse({ message: "추천 서버 오류" }, 500);
    });
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("추천 서버 오류")).toBeInTheDocument();
    note("FE04-017", "500 message가 화면에 표시된다.");
  });

  it("FE04-018", async () => {
    const user = userEvent.setup();
    const fetchMock = installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return new Promise<Response>(() => {});
    });
    renderPage();
    await screen.findByRole("button", { name: "추천 받기" });
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    const button = screen.getByRole("button", { name: "업종을 계산하는 중..." });
    await user.click(button);
    expect(recommendPosts(fetchMock)).toHaveLength(1);
    note("FE04-018", "느린 응답 동안 두 번째 클릭은 막혀 POST가 1회다.");
  });

  it("FE04-019", async () => {
    const user = userEvent.setup();
    const fetchMock = installFetch(async (url, init) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      const body = JSON.parse(String(init?.body));
      return jsonResponse(recommendation({ district: body.district, dong: body.dong, change_name: body.dong === "역삼동" ? "상권확장" : "상권축소" }));
    });
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("연남동 · 상권축소")).toBeInTheDocument();
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("역삼동"));
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("역삼동 · 상권확장")).toBeInTheDocument();
    expect(recommendPosts(fetchMock)).toHaveLength(2);
    note("FE04-019", "지역을 바꾼 뒤 다시 누르면 최신 역삼동 결과로 헤더가 바뀐다.");
  });

  it("FE04-020", async () => {
    const user = userEvent.setup();
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("연남동 · 상권축소")).toBeInTheDocument();
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("역삼동"));
    expect(screen.queryByText("연남동 · 상권축소"), "구를 바꿨는데 이전 동 결과 표가 그대로 남아 있다").toBeNull();
  });

  it("FE04-021", async () => {
    const user = userEvent.setup();
    const all = Array.from({ length: 10 }, (_, i) => industryItem({ industry: `업종${i}` }));
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse(recommendation({ recommendations: all.slice(0, 5), all_industries: all }));
    });
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    expect(await screen.findByText("업종0")).toBeInTheDocument();
    expect(screen.getByText("업종9")).toBeInTheDocument();
    expect(screen.getAllByRole("row")).toHaveLength(11);
    const top = screen.queryByText(/상위 추천|TOP|recommendations/);
    expect(top, "10행은 렌더되지만 recommendations 5개를 구분하는 상위 추천 표시가 없다").not.toBeNull();
  });

  it("FE04-022", () => {
    throw new Error("RISK: jsdom은 375px에서 30자 업종명의 테이블 가로 overflow를 계산하지 못한다");
  });

  it("FE04-023", async () => {
    const user = userEvent.setup();
    const errors: string[] = [];
    const spy = vi.spyOn(console, "error").mockImplementation((...args) => {
      errors.push(args.map(String).join(" "));
    });
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse(recommendation({
        all_industries: [industryItem({ industry: "한식음식점" }), industryItem({ industry: "한식음식점", ml_close_rate: 8 })],
      }));
    });
    renderPage();
    await user.click(await screen.findByRole("button", { name: "추천 받기" }));
    await screen.findAllByText("한식음식점");
    spy.mockRestore();
    const dup = errors.filter((line) => line.includes("same key"));
    expect(dup, dup.join("\n")).toEqual([]);
  });

  it("FE04-024", async () => {
    const user = userEvent.setup();
    const fetchMock = installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse({ message: "목록 실패" }, 503);
      return jsonResponse(recommendation());
    });
    renderPage();
    expect(await screen.findByText("목록 실패")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "추천 받기" }));
    await waitFor(() => expect(recommendPosts(fetchMock).length).toBe(1));
    const body = JSON.parse(String((recommendPosts(fetchMock)[0][1] as RequestInit).body));
    expect(body).toEqual({ district: "마포구", dong: "연남동" });
    expect(await screen.findByText("연남동 · 상권축소")).toBeInTheDocument();
    note("FE04-024", "옵션 503 안내 뒤에도 기본값 마포구/연남동은 유효해 추천 POST가 나가고 결과가 교체된다.");
  });
});
