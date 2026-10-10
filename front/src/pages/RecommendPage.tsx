import { useEffect, useState } from "react";
import { getOptions, getRecommendations, type Options, type Recommendation } from "../api/api";
import { INPUT_STYLE, STATUS_INFO } from "../components/options";

// 기능 2: 같은 동의 업종 추천
export default function RecommendPage() {
  const [options, setOptions] = useState<Options | null>(null);
  const [district, setDistrict] = useState("마포구");
  const [dong, setDong] = useState("연남동");
  const [result, setResult] = useState<Recommendation | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getOptions()
      .then(setOptions)
      .catch((e) => setError(e instanceof Error ? e.message : "목록을 불러오지 못했습니다."));
  }, []);

  useEffect(() => {
    if (!options) return;
    const dongs = options.dongs.filter((item) => item.district === district);
    if (dongs.length > 0 && !dongs.some((item) => item.dong === dong)) {
      setDong(dongs[0].dong);
    }
  }, [district, options, dong]);

  async function handleSubmit() {
    setLoading(true);
    setError("");
    try {
      setResult(await getRecommendations({ district, dong }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "추천에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  }

  const dongs = options?.dongs.filter((item) => item.district === district) ?? [];

  return (
    <div className="space-y-4">
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100 space-y-4">
        <h2 className="text-xl font-bold">업종 추천</h2>
        <p className="text-sm text-gray-500">
          한 행정동 안의 업종을 AI가 점수 매겨, 폐업률이 낮고 매출이 나은 순으로 보여 줍니다.
        </p>

        <div className="grid grid-cols-2 gap-4">
          <label className="block text-sm">
            자치구
            <select className={INPUT_STYLE} value={district} onChange={(e) => setDistrict(e.target.value)}>
              {(options?.districts ?? [district]).map((name) => (
                <option key={name} value={name}>{name}</option>
              ))}
            </select>
          </label>
          <label className="block text-sm">
            행정동
            <select className={INPUT_STYLE} value={dong} onChange={(e) => setDong(e.target.value)}>
              {(dongs.length ? dongs : [{ dong, dong_code: "", district }]).map((item) => (
                <option key={item.dong} value={item.dong}>{item.dong}</option>
              ))}
            </select>
          </label>
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full py-3 rounded-xl bg-amber-800 text-white font-bold disabled:opacity-50"
        >
          {loading ? "업종을 계산하는 중..." : "추천 받기"}
        </button>
      </div>

      {result && (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100">
          <p className="font-bold mb-1">{result.dong} · {result.change_name}</p>
          <p className="text-sm text-gray-500 mb-4">점수 = 예상 매출/100 − 예상 폐업률×8 (높을수록 추천)</p>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b">
                <th className="py-2">업종</th>
                <th>예상 폐업률</th>
                <th>예상 매출</th>
                <th>단계</th>
              </tr>
            </thead>
            <tbody>
              {result.all_industries.map((item) => {
                const status = STATUS_INFO[item.status] ?? STATUS_INFO.unknown;
                return (
                  <tr key={item.industry} className="border-b last:border-0">
                    <td className="py-2 font-medium">{item.industry}</td>
                    <td>{item.ml_close_rate}%</td>
                    <td>{item.dl_sales_per_store}만원</td>
                    <td>
                      <span className={`px-2 py-0.5 rounded-full text-xs ${status.color}`}>{status.label}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
