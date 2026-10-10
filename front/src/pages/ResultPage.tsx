import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getDiagnosis, type Diagnosis } from "../api/api";
import { STATUS_INFO } from "../components/options";

// 기능 1: 진단 결과 화면 (주소의 id로 결과를 불러온다)
export default function ResultPage() {
  const { id } = useParams();
  const [result, setResult] = useState<Diagnosis | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;
    getDiagnosis(id)
      .then(setResult)
      .catch((e) => setError(e instanceof Error ? e.message : "결과를 불러오지 못했습니다."));
  }, [id]);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!result) return <p className="text-gray-500">불러오는 중...</p>;

  const status = STATUS_INFO[result.status] ?? STATUS_INFO.unknown;

  return (
    <div className="space-y-4">
      <section className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100">
        <p className="text-sm text-gray-500">{result.district} {result.dong} · {result.industry}</p>
        <p className="text-4xl font-bold my-2">폐업률 {result.closeRate}%</p>
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-bold ${status.color}`}>
          {status.label} · {result.changeName}
        </span>
        <p className="text-xs text-gray-400 mt-3">
          규칙: 폐업률 8% 이상 또는 상권축소면 위험 / 4% 이상 또는 다이나믹이면 주의
        </p>
      </section>

      <section className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100">
        <h3 className="font-bold mb-3">AI 예측</h3>
        <div className="grid grid-cols-2 gap-3 text-center">
          <div className="bg-gray-50 rounded-xl p-3">
            <p className="text-xs text-gray-500">ML 예상 폐업률</p>
            <p className="text-xl font-bold">{result.mlCloseRate}%</p>
          </div>
          <div className="bg-amber-50 rounded-xl p-3">
            <p className="text-xs text-gray-500">DL 예상 점포당 매출</p>
            <p className="text-xl font-bold">{result.dlSalesPerStore}만원</p>
          </div>
        </div>
        <p className="mt-3 text-sm text-gray-600">
          점포 {result.storeCount}개 · 개업률 {result.openRate}% · 유동인구 {Math.round(result.footTraffic).toLocaleString()}명
        </p>
      </section>

      <section className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100">
        <h3 className="font-bold mb-2">
          AI 설명 <span className="text-xs font-normal text-gray-400">({result.explanationSource === "gemini" ? "Gemini" : "기본 문장"})</span>
        </h3>
        <p className="text-sm leading-relaxed whitespace-pre-line">{result.explanation}</p>
      </section>

      <Link to="/" className="block text-center text-sm text-amber-800">← 다시 진단하기</Link>
    </div>
  );
}
