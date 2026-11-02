import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes, useNavigate } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import ResultPage from "../pages/ResultPage";
import { diagnosis, installFetch, jsonResponse } from "./fixtures";
import { note } from "./note";

function Go() {
  const navigate = useNavigate();
  return <button onClick={() => navigate("/diagnoses/2")}>다른 결과</button>;
}

async function settle() {
  await waitFor(() => {
    expect(document.querySelector("p.text-4xl")).toBeTruthy();
  });
}

function renderResult(path = "/diagnoses/12") {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/" element={<p>진단 입력 홈</p>} />
        <Route path="/diagnoses/:id" element={<><ResultPage /><Go /></>} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("FE03 진단 결과", () => {
  it("FE03-001", async () => {
    const fetchMock = installFetch(async (url) => jsonResponse(diagnosis({ id: 12 })));
    renderResult("/diagnoses/12");
    await settle();
    expect(fetchMock.mock.calls.some((call) => String(call[0]).endsWith("/api/diagnoses/12"))).toBe(true);
    note("FE03-001", "GET /api/diagnoses/12 가 호출된다.");
  });

  it("FE03-002", async () => {
    installFetch(() => new Promise<Response>(() => {}));
    renderResult();
    expect(await screen.findByText("불러오는 중...")).toBeInTheDocument();
    note("FE03-002", "미응답 동안 '불러오는 중...'이 보인다.");
  });

  it("FE03-003", async () => {
    installFetch(async () => jsonResponse({ message: "진단을 찾을 수 없습니다." }, 404));
    renderResult();
    expect(await screen.findByText("진단을 찾을 수 없습니다.")).toBeInTheDocument();
    note("FE03-003", "404 message가 오류 문장으로 표시된다.");
  });

  it("FE03-004", async () => {
    installFetch(async () => jsonResponse(diagnosis()));
    renderResult();
    expect(await screen.findByText("마포구 연남동 · 한식음식점")).toBeInTheDocument();
    note("FE03-004", "상단에 마포구, 연남동, 한식음식점이 한 줄에 있다.");
  });

  it("FE03-005", async () => {
    installFetch(async () => jsonResponse(diagnosis({ closeRate: 5.6 })));
    renderResult();
    expect(await screen.findByText("폐업률 5.6%")).toBeInTheDocument();
    note("FE03-005", "'폐업률 5.6%' 문자열이 있다.");
  });

  function chipOf(container: HTMLElement) {
    const chip = container.querySelector("span.rounded-full");
    if (!chip) throw new Error("상태 칩이 없다");
    return chip;
  }

  it("FE03-006", async () => {
    installFetch(async () => jsonResponse(diagnosis({ status: "stable" })));
    const { container } = renderResult();
    await settle();
    const chip = chipOf(container);
    expect(chip.textContent).toContain("안정");
    expect(chip.className).toContain("bg-emerald-100");
    note("FE03-006", "stable 칩 문구는 안정이고 emerald 클래스가 붙는다.");
  });

  it("FE03-007", async () => {
    installFetch(async () => jsonResponse(diagnosis({ status: "warning" })));
    const { container } = renderResult();
    await settle();
    const chip = chipOf(container);
    expect(chip.textContent).toContain("주의");
    expect(chip.className).toContain("bg-amber-100");
    note("FE03-007", "warning 칩 문구는 주의이고 amber 클래스가 붙는다.");
  });

  it("FE03-008", async () => {
    installFetch(async () => jsonResponse(diagnosis({ status: "danger" })));
    const { container } = renderResult();
    await settle();
    const chip = chipOf(container);
    expect(chip.textContent).toContain("위험");
    expect(chip.className).toContain("bg-red-100");
    note("FE03-008", "danger 칩 문구는 위험이고 red 클래스가 붙는다.");
  });

  it("FE03-009", async () => {
    installFetch(async () => jsonResponse(diagnosis({ status: "unknown" })));
    const { container } = renderResult();
    await settle();
    const chip = chipOf(container);
    expect(chip.textContent).toContain("판단 불가");
    expect(chip.className).toContain("bg-gray-100");
    note("FE03-009", "unknown 칩 문구는 판단 불가다.");
  });

  it("FE03-010", async () => {
    installFetch(async () => jsonResponse(diagnosis({ status: "weird" })));
    const { container } = renderResult();
    await settle();
    const chip = chipOf(container);
    expect(chip.textContent).toContain("판단 불가");
    expect(chip.className).toContain("bg-gray-100");
    note("FE03-010", "알 수 없는 status=weird 는 unknown 스타일·판단 불가로 떨어진다.");
  });

  it("FE03-011", async () => {
    installFetch(async () => jsonResponse(diagnosis({ changeName: "상권축소", status: "danger" })));
    const { container } = renderResult();
    await settle();
    expect(chipOf(container).textContent).toContain("상권축소");
    note("FE03-011", "상태 칩 텍스트에 상권축소가 포함된다.");
  });

  it("FE03-012", async () => {
    installFetch(async () => jsonResponse(diagnosis({ mlCloseRate: 7.34 })));
    renderResult();
    expect(await screen.findByText("7.34%")).toBeInTheDocument();
    note("FE03-012", "ML 예상 폐업률 7.34%가 표시된다.");
  });

  it("FE03-013", async () => {
    installFetch(async () => jsonResponse(diagnosis({ dlSalesPerStore: 650.2 })));
    renderResult();
    expect(await screen.findByText("650.2만원")).toBeInTheDocument();
    note("FE03-013", "DL 예상 매출 650.2만원이 표시된다.");
  });

  it("FE03-014", async () => {
    installFetch(async () => jsonResponse(diagnosis({ storeCount: 30 })));
    renderResult();
    expect(await screen.findByText(/점포 30개/)).toBeInTheDocument();
    note("FE03-014", "'점포 30개'가 표시된다.");
  });

  it("FE03-015", async () => {
    installFetch(async () => jsonResponse(diagnosis({ openRate: 2.1 })));
    renderResult();
    expect(await screen.findByText(/개업률 2\.1%/)).toBeInTheDocument();
    note("FE03-015", "'개업률 2.1%'가 표시된다.");
  });

  it("FE03-016", async () => {
    installFetch(async () => jsonResponse(diagnosis({ footTraffic: 1099.9 })));
    renderResult();
    expect(await screen.findByText(/유동인구 1,100명/)).toBeInTheDocument();
    note("FE03-016", "Math.round(1099.9) 후 toLocaleString으로 유동인구 1,100명이다.");
  });

  it("FE03-017", async () => {
    installFetch(async () => jsonResponse(diagnosis({ explanationSource: "basic" })));
    renderResult();
    await settle();
    expect(document.body.textContent).toContain("기본 문장");
    note("FE03-017", "explanationSource=basic 이면 '기본 문장'이 보인다.");
  });

  it("FE03-018", async () => {
    installFetch(async () => jsonResponse(diagnosis({ explanationSource: "gemini" })));
    renderResult();
    await settle();
    expect(document.body.textContent).toContain("Gemini");
    note("FE03-018", "explanationSource=gemini 이면 'Gemini'가 보인다.");
  });

  it("FE03-019", async () => {
    installFetch(async () => jsonResponse(diagnosis({ explanation: "한 줄\n두 줄" })));
    renderResult();
    const paragraph = await screen.findByText(/한 줄/);
    expect(paragraph).toHaveClass("whitespace-pre-line");
    expect(paragraph.textContent).toContain("두 줄");
    note("FE03-019", "설명 노드에 whitespace-pre-line 이 있고 두 줄 텍스트가 유지된다.");
  });

  it("FE03-020", async () => {
    const user = userEvent.setup();
    installFetch(async () => jsonResponse(diagnosis()));
    renderResult();
    await settle();
    await user.click(screen.getByRole("link", { name: /다시 진단하기/ }));
    expect(await screen.findByText("진단 입력 홈")).toBeInTheDocument();
    note("FE03-020", "'다시 진단하기' 링크가 / 화면으로 이동한다.");
  });

  it("FE03-021", async () => {
    installFetch(async () => jsonResponse(diagnosis({ closeRate: null as unknown as number })));
    renderResult();
    await settle();
    const guide = screen.queryByText(/결측|값 없음|알 수 없음/);
    expect(guide, `결측 안내 없음. 본문=${document.body.textContent?.slice(0, 200)}`).not.toBeNull();
  });

  it("FE03-022", async () => {
    const user = userEvent.setup();
    let release: (value: Response) => void = () => {};
    const pending = new Promise<Response>((resolve) => {
      release = resolve;
    });
    installFetch(async (url) => {
      if (url.endsWith("/api/diagnoses/1")) return jsonResponse(diagnosis({ id: 1, explanation: "결과-1", closeRate: 1 }));
      if (url.endsWith("/api/diagnoses/2")) return pending;
      return jsonResponse(diagnosis());
    });
    renderResult("/diagnoses/1");
    expect(await screen.findByText("결과-1")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "다른 결과" }));
    await waitFor(() => expect(screen.queryByText("결과-1")).toBeNull());
    release(jsonResponse(diagnosis({ id: 2, explanation: "결과-2", closeRate: 2 })));
  });

  it("FE03-023", async () => {
    const payload = '<img src=x onerror="alert(1)"><script>alert(1)</script>';
    installFetch(async () => jsonResponse(diagnosis({ explanation: payload })));
    const { container } = renderResult();
    expect(await screen.findByText(payload)).toBeInTheDocument();
    expect(container.querySelector("script")).toBeNull();
    expect(container.querySelector("img")).toBeNull();
    note("FE03-023", "설명의 HTML/script는 텍스트로만 보이고 script·img 요소는 만들어지지 않는다.");
  });

  it("FE03-024", async () => {
    installFetch(async () => jsonResponse(diagnosis({ explanation: "" })));
    renderResult();
    await settle();
    expect(document.querySelector("p.text-4xl")?.textContent).toContain("폐업률");
    expect(document.body.textContent).toContain("기본 문장");
    note("FE03-024", "빈 설명이어도 폐업률과 출처 라벨이 남고 예외가 없다.");
  });
});
