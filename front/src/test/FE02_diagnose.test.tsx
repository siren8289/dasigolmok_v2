import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DiagnosePage from "../pages/DiagnosePage";
import ResultPage from "../pages/ResultPage";
import { OPTIONS, diagnosis, htmlResponse, installFetch, jsonResponse } from "./fixtures";
import { note } from "./note";

function renderPage() {
  return render(
    <MemoryRouter initialEntries={["/"]}>
      <Routes>
        <Route path="/" element={<DiagnosePage />} />
        <Route path="/diagnoses/:id" element={<ResultPage />} />
      </Routes>
    </MemoryRouter>,
  );
}

function posts(fetchMock: ReturnType<typeof vi.fn>) {
  return fetchMock.mock.calls.filter((call) => String(call[0]).includes("/api/diagnoses") && (call[1] as RequestInit | undefined)?.method === "POST");
}

beforeEach(() => {
  installFetch(async (url, init) => {
    if (url.includes("/api/options")) return jsonResponse(OPTIONS);
    if (url.includes("/api/diagnoses")) return jsonResponse(diagnosis({ id: 12 }), 201);
    throw new Error("unexpected " + url + " " + init?.method);
  });
});

describe("FE02 진단 입력", () => {
  it("FE02-001", async () => {
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    expect(screen.getByRole("combobox", { name: "자치구" })).toHaveValue("마포구");
    note("FE02-001", "옵션 로드 후 자치구 값이 마포구다.");
  });

  it("FE02-002", async () => {
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("연남동");
    note("FE02-002", "최초 행정동 값이 연남동이다.");
  });

  it("FE02-003", async () => {
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    expect(screen.getByRole("combobox", { name: "업종" })).toHaveValue("한식음식점");
    note("FE02-003", "최초 업종 값이 한식음식점이다.");
  });

  it("FE02-004", async () => {
    const fetchMock = vi.mocked(fetch);
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    const optionCalls = fetchMock.mock.calls.filter((call) => String(call[0]).includes("/api/options"));
    expect(optionCalls).toHaveLength(1);
    note("FE02-004", "StrictMode 없이 마운트하면 GET /api/options 가 1회다.");
  });

  it("FE02-005", async () => {
    renderPage();
    await screen.findByRole("option", { name: "마포구" });
    expect(screen.getByRole("combobox", { name: "자치구" })).toHaveValue("마포구");
    note("FE02-005", "districts에 마포구가 있으면 선택이 마포구로 유지된다.");
  });

  it("FE02-006", async () => {
    installFetch(async (url) => {
      if (url.includes("/api/options")) {
        return jsonResponse({ ...OPTIONS, districts: ["강남구"], dongs: OPTIONS.dongs.filter((d) => d.district === "강남구") });
      }
      return jsonResponse(diagnosis());
    });
    renderPage();
    await waitFor(() => expect(screen.getByRole("combobox", { name: "자치구" })).toHaveValue("강남구"));
    note("FE02-006", "마포구가 없으면 첫 자치구 강남구로 바뀐다.");
  });

  it("FE02-007", async () => {
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse({ districts: [], dongs: [], industries: [] });
      return jsonResponse(diagnosis());
    });
    renderPage();
    await waitFor(() => expect(vi.mocked(fetch).mock.calls.some((c) => String(c[0]).includes("/api/options"))).toBe(true));
    const guide = screen.queryByText(/목록이 비어|선택할 수 없|불러올 지역이 없/);
    expect(guide, `빈 목록 안내 없음. 본문=${document.body.textContent?.slice(0, 180)}`).not.toBeNull();
  });

  it("FE02-008", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "강남구" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    const dong = await screen.findByRole("combobox", { name: "행정동" });
    const labels = [...dong.querySelectorAll("option")].map((o) => o.textContent);
    expect(labels).toEqual(["역삼동", "삼성동"]);
    note("FE02-008", "강남구로 바꾸면 행정동 선택지가 역삼동·삼성동이다.");
  });

  it("FE02-009", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "연남동" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("역삼동"));
    note("FE02-009", "연남동은 강남구 목록에 없어 첫 동 역삼동으로 바뀐다.");
  });

  it("FE02-010", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "망원동" });
    await user.selectOptions(screen.getByRole("combobox", { name: "행정동" }), "망원동");
    expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("망원동");
    note("FE02-010", "마포구 목록에 망원동이 있으면 선택 후 첫 동으로 되돌리지 않는다.");
  });

  it("FE02-011", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "망원동" });
    await user.selectOptions(screen.getByRole("combobox", { name: "행정동" }), "망원동");
    expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("망원동");
    note("FE02-011", "연남동에서 망원동으로 행정동 값이 바뀐다.");
  });

  it("FE02-012", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "커피-음료" });
    await user.selectOptions(screen.getByRole("combobox", { name: "업종" }), "커피-음료");
    expect(screen.getByRole("combobox", { name: "업종" })).toHaveValue("커피-음료");
    note("FE02-012", "업종 값이 커피-음료로 바뀐다.");
  });

  it("FE02-013", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.mocked(fetch);
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    await waitFor(() => expect(posts(fetchMock).length).toBe(1));
    const body = JSON.parse(String((posts(fetchMock)[0][1] as RequestInit).body));
    expect(body).toEqual({ district: "마포구", dong: "연남동", industry: "한식음식점" });
    note("FE02-013", "POST /api/diagnoses body에 district, dong, industry 세 필드가 실렸다.");
  });

  it("FE02-014", async () => {
    const user = userEvent.setup();
    let release: (value: Response) => void = () => {};
    const pending = new Promise<Response>((resolve) => {
      release = resolve;
    });
    const fetchMock = installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return pending;
    });
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    const button = screen.getByRole("button", { name: "AI가 분석하는 중..." });
    expect(button).toBeDisabled();
    await user.click(button);
    expect(posts(fetchMock)).toHaveLength(1);
    release(jsonResponse(diagnosis({ id: 12 }), 201));
    note("FE02-014", "응답 대기 중 버튼이 disabled이고 POST는 1회만 나갔다.");
  });

  it("FE02-015", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return new Promise<Response>(() => {});
    });
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    expect(screen.getByRole("button", { name: "AI가 분석하는 중..." })).toBeInTheDocument();
    note("FE02-015", "대기 중 버튼 문구가 'AI가 분석하는 중...'이다.");
  });

  it("FE02-016", async () => {
    const user = userEvent.setup();
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    expect(await screen.findByText(/폐업률 5\.6%/)).toBeInTheDocument();
    note("FE02-016", "id=12 응답 후 결과 화면(폐업률)이 같은 라우터의 /diagnoses/12 로 표시된다.");
  });

  it("FE02-017", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse({ message: "해당 상권을 찾을 수 없습니다." }, 404);
    });
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    expect(await screen.findByText("해당 상권을 찾을 수 없습니다.")).toBeInTheDocument();
    note("FE02-017", "404 JSON message가 화면에 그대로 표시된다.");
  });

  it("FE02-018", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return htmlResponse(500);
    });
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    expect(await screen.findByText("요청에 실패했습니다.")).toBeInTheDocument();
    note("FE02-018", "HTML 500은 JSON 파싱에 실패해 기본 문구 '요청에 실패했습니다.'를 보여 준다.");
  });

  it("FE02-019", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse(OPTIONS);
      return jsonResponse({ message: "일시 오류" }, 502);
    });
    renderPage();
    await screen.findByRole("option", { name: "한식음식점" });
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    await screen.findByText("일시 오류");
    const button = screen.getByRole("button", { name: "진단하기" });
    expect(button).toBeEnabled();
    note("FE02-019", "오류로 Promise가 끝나면 버튼이 다시 '진단하기'이고 활성화된다.");
  });

  it("FE02-020", async () => {
    installFetch(async (url) => {
      if (url.includes("/api/options")) return jsonResponse({ message: "옵션 장애" }, 503);
      return jsonResponse(diagnosis());
    });
    renderPage();
    expect(await screen.findByText("옵션 장애")).toBeInTheDocument();
    note("FE02-020", "GET /api/options 503의 message '옵션 장애'가 표시된다.");
  });

  it("FE02-021", async () => {
    const user = userEvent.setup();
    const fetchMock = installFetch(async (url) => {
      if (url.includes("/api/options")) {
        return jsonResponse({ ...OPTIONS, districts: ["마포구", ""] });
      }
      return jsonResponse(diagnosis({ id: 12 }), 201);
    });
    renderPage();
    await screen.findByRole("option", { name: "마포구" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "");
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    await waitFor(() => expect(posts(fetchMock).length + screen.queryAllByText(/유효하지|비어/).length).toBeGreaterThan(0));
    const sent = posts(fetchMock);
    const blocked = sent.length === 0 && screen.queryByText(/유효하지|선택|비어/);
    expect(blocked, `빈 자치구 제출이 차단되지 않음. POST ${sent.length}건`).toBeTruthy();
  });

  it("FE02-022", async () => {
    const user = userEvent.setup();
    const fetchMock = vi.mocked(fetch);
    renderPage();
    await screen.findByRole("option", { name: "강남구" });
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "강남구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("역삼동"));
    await user.selectOptions(screen.getByRole("combobox", { name: "자치구" }), "마포구");
    await waitFor(() => expect(screen.getByRole("combobox", { name: "행정동" })).toHaveValue("연남동"));
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    await waitFor(() => expect(posts(fetchMock).length).toBe(1));
    const body = JSON.parse(String((posts(fetchMock)[0][1] as RequestInit).body));
    expect(body.district).toBe("마포구");
    expect(body.dong).not.toBe("역삼동");
    note("FE02-022", "마포구로 돌아오면 역삼동은 유지되지 않고 연남동으로 교정된 뒤 제출된다.");
  });

  it("FE02-023", async () => {
    const user = userEvent.setup();
    installFetch(async (url) => {
      if (url.includes("/api/options")) {
        return jsonResponse({
          ...OPTIONS,
          industries: [...OPTIONS.industries, { industry: "NOT_EXIST", industry_code: "X" }],
        });
      }
      return jsonResponse({ message: "지원하지 않는 업종입니다." }, 400);
    });
    renderPage();
    await screen.findByRole("option", { name: "NOT_EXIST" });
    await user.selectOptions(screen.getByRole("combobox", { name: "업종" }), "NOT_EXIST");
    await user.click(screen.getByRole("button", { name: "진단하기" }));
    expect(await screen.findByText("지원하지 않는 업종입니다.")).toBeInTheDocument();
    note("FE02-023", "NOT_EXIST 제출 후 서버 message '지원하지 않는 업종입니다.'가 사용자에게 표시된다. 제출 전 별도 클라이언트 차단 문구는 없다.");
  });

  it("FE02-024", async () => {
    let release: (value: Response) => void = () => {};
    const pending = new Promise<Response>((resolve) => {
      release = resolve;
    });
    installFetch(async (url) => {
      if (url.includes("/api/options")) return pending;
      return jsonResponse(diagnosis());
    });
    renderPage();
    const district = screen.getByRole("combobox", { name: "자치구" });
    const optionsBefore = [...district.querySelectorAll("option")].map((o) => o.textContent);
    expect(optionsBefore).toEqual(["마포구"]);
    release(jsonResponse(OPTIONS));
    await screen.findByRole("option", { name: "강남구" });
    note("FE02-024", "옵션 응답 전에는 대체 선택지가 기본 마포구뿐이라 다른 구를 먼저 고르는 경합을 UI에서 재현할 수 있다 보기 어렵다.");
    throw new Error("RISK: 옵션 도착 전 셀렉트 선택지가 현재 구 하나뿐이고, 응답 콜백은 요청 세대 가드 없이 setDistrict를 호출한다. 오래된 응답이 사용자 선택을 덮는 시나리오는 이 UI에서 재현되지 않았다.");
  });
});
