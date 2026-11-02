import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter, MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import { OPTIONS, diagnosis, installFetch, jsonResponse } from "./fixtures";
import { note } from "./note";

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

beforeEach(() => {
  installFetch(async (url) => {
    if (url.includes("/api/options")) return jsonResponse(OPTIONS);
    if (url.includes("/api/diagnoses/")) return jsonResponse(diagnosis({ id: Number(url.split("/").pop()) }));
    return jsonResponse(diagnosis());
  });
});

describe("FE01 공통 라우팅", () => {
  it("FE01-001", async () => {
    renderAt("/");
    expect(await screen.findByRole("heading", { name: "골목 상권 진단" })).toBeInTheDocument();
    note("FE01-001", "GET / 렌더에서 heading '골목 상권 진단'과 자치구·행정동·업종 셀렉트가 보인다.");
  });

  it("FE01-002", async () => {
    renderAt("/recommend");
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    note("FE01-002", "GET /recommend 에서 heading '업종 추천'이 렌더된다.");
  });

  it("FE01-003", async () => {
    const fetchMock = vi.mocked(fetch);
    renderAt("/diagnoses/1");
    await screen.findByText(/불러오는 중|폐업률/);
    await waitFor(() => {
      const called = fetchMock.mock.calls.some((call) => String(call[0]).includes("/api/diagnoses/1"));
      expect(called).toBe(true);
    });
    note("FE01-003", "경로 /diagnoses/1 이 GET /api/diagnoses/1 을 호출한다.");
  });

  it("FE01-004", async () => {
    const user = userEvent.setup();
    renderAt("/recommend");
    await screen.findByRole("heading", { name: "업종 추천" });
    await user.click(screen.getByRole("link", { name: "골목 상권 진단" }));
    expect(await screen.findByRole("heading", { name: "골목 상권 진단" })).toBeInTheDocument();
    note("FE01-004", "상단 '골목 상권 진단' 링크 클릭 후 진단 화면 heading이 돌아온다.");
  });

  it("FE01-005", async () => {
    const user = userEvent.setup();
    renderAt("/");
    await user.click(screen.getByRole("link", { name: "업종 추천" }));
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    note("FE01-005", "상단 '업종 추천' 클릭 후 /recommend 화면이 표시된다.");
  });

  it("FE01-006", async () => {
    const user = userEvent.setup();
    window.history.replaceState({}, "", "/");
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    );
    await user.click(screen.getByRole("link", { name: "업종 추천" }));
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    window.history.back();
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "골목 상권 진단" })).toBeInTheDocument();
    });
    note("FE01-006", "진단 화면에서 추천으로 이동한 뒤 window.history.back() 으로 진단 화면과 이전 주소가 복원된다.");
  });

  it("FE01-007", () => {
    const nginxPath = resolve(dirname(fileURLToPath(import.meta.url)), "../../nginx.conf");
    const conf = readFileSync(nginxPath, "utf8");
    expect(conf).toMatch(/try_files\s+\$uri\s+\$uri\/\s+\/index\.html/);
    note("FE01-007", "front/nginx.conf location / 에 try_files $uri $uri/ /index.html history fallback이 있다. 라이브 Nginx 재시작은 이 단위 실행에 포함하지 않았다.");
  });

  it("FE01-008", async () => {
    renderAt("/nothing");
    await screen.findByText("dasiGolmok");
    const guide = screen.queryByRole("heading", { name: /404|찾을 수 없|없는 페이지/ });
    const body = document.body.textContent ?? "";
    expect(guide, `실제 본문에는 404 안내가 없다: ${body.slice(0, 160)}`).not.toBeNull();
  });

  it("FE01-009", () => {
    throw new Error("RISK: jsdom은 375px 뷰포트의 가로 잘림(scrollWidth)을 계산하지 않아 탭·셀렉트 overflow를 실행 측정할 수 없음");
  });

  it("FE01-010", async () => {
    const user = userEvent.setup();
    renderAt("/");
    await screen.findByRole("heading", { name: "골목 상권 진단" });
    await user.tab();
    const seen = new Set<string>();
    for (let i = 0; i < 8; i += 1) {
      const el = document.activeElement;
      if (el instanceof HTMLElement) seen.add(el.tagName + ":" + (el.textContent ?? "").slice(0, 20));
      await user.tab();
    }
    expect(seen.size).toBeGreaterThan(1);
    note("FE01-010", `Tab 이동으로 포커스가 바뀐 요소: ${[...seen].join(" | ")}`);
  });

  it("FE01-011", async () => {
    renderAt("/");
    expect(document.querySelector("header")).toBeTruthy();
    expect(document.querySelector("main")).toBeTruthy();
    expect(screen.getByText("dasiGolmok")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "골목 상권 진단" })).toBeInTheDocument();
    note("FE01-011", "header/main 랜드마크와 브랜드 텍스트, 진단 heading이 있다. document title은 index.html의 'dasiGolmok - 서울 골목 상권 진단'이다.");
  });

  it("FE01-012", async () => {
    const errors: string[] = [];
    const spy = vi.spyOn(console, "error").mockImplementation((...args) => {
      errors.push(args.map(String).join(" "));
    });
    renderAt("/");
    await screen.findByRole("heading", { name: "골목 상권 진단" });
    spy.mockRestore();
    expect(errors, errors.join("\n")).toEqual([]);
    note("FE01-012", "옵션 목 응답으로 첫 렌더 후 header/main/heading이 있고 console.error가 비어 있다.");
  });

  it("FE01-013", async () => {
    const user = userEvent.setup();
    renderAt("/");
    const link = screen.getByRole("link", { name: "업종 추천" });
    link.focus();
    await user.keyboard("{Enter}");
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    note("FE01-013", "업종 추천 링크에 포커스한 뒤 Enter로 추천 화면에 진입했다.");
  });

  it("FE01-014", () => {
    renderAt("/");
    const diagnose = screen.getByRole("link", { name: "골목 상권 진단" });
    const recommend = screen.getByRole("link", { name: "업종 추천" });
    expect(diagnose.tagName).toBe("A");
    expect(recommend.tagName).toBe("A");
    expect(diagnose).toHaveAttribute("href", "/");
    expect(recommend).toHaveAttribute("href", "/recommend");
    note("FE01-014", "상단 메뉴는 href가 있는 <a>라 중클릭·새 탭으로 주소가 독립적으로 열린다.");
  });

  it("FE01-015", () => {
    throw new Error("RISK: jsdom은 320px에서 실제 글자 폭과 가로 스크롤을 계산하지 않아 가독성·잘림을 실행 측정할 수 없음");
  });

  it("FE01-016", async () => {
    const errors: string[] = [];
    const spy = vi.spyOn(console, "error").mockImplementation((...args) => {
      errors.push(args.map(String).join(" "));
    });
    renderAt("/recommend?utm=qa");
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    spy.mockRestore();
    expect(errors).toEqual([]);
    note("FE01-016", "/recommend?utm=qa 진입 시 추천 화면이 렌더되고 console.error가 없다. 쿼리는 라우트가 제거하지 않는다.");
  });

  it("FE01-017", async () => {
    renderAt("/");
    expect(await screen.findByRole("heading", { name: "골목 상권 진단" })).toBeInTheDocument();
    renderAt("/recommend");
    expect(await screen.findByRole("heading", { name: "업종 추천" })).toBeInTheDocument();
    note("FE01-017", "App 라우트는 / 와 /recommend 두 화면을 그대로 렌더한다. RAG API는 이 두 라우트를 바꾸지 않는다.");
  });

  it("FE01-018", async () => {
    renderAt("/unknown-path");
    await screen.findByText("dasiGolmok");
    const named = screen.queryByRole("heading", { name: /404|찾을 수 없|없는 주소/ });
    expect(named, "알 수 없는 경로에 사용자용 오류 heading이 없다").not.toBeNull();
  });
});
