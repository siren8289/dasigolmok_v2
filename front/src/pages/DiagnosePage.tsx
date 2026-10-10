import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createDiagnosis, getOptions, type Options } from "../api/api";
import { INPUT_STYLE } from "../components/options";

// 기능 1: 골목 상권 진단 입력 화면
export default function DiagnosePage() {
  const navigate = useNavigate();
  const [options, setOptions] = useState<Options | null>(null);
  const [district, setDistrict] = useState("마포구");
  const [dong, setDong] = useState("연남동");
  const [industry, setIndustry] = useState("한식음식점");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getOptions()
      .then((data) => {
        setOptions(data);
        if (data.districts.includes("마포구")) setDistrict("마포구");
        else if (data.districts[0]) setDistrict(data.districts[0]);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "목록을 불러오지 못했습니다."));
  }, []);

  // 구를 바꾸면, 그 구의 첫 번째 동으로 맞춘다.
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
      const result = await createDiagnosis({ district, dong, industry });
      navigate(`/diagnoses/${result.id}`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "진단에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  }

  const dongs = options?.dongs.filter((item) => item.district === district) ?? [];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-amber-100 space-y-4">
      <h2 className="text-xl font-bold">골목 상권 진단</h2>
      <p className="text-sm text-gray-500">
        행정동과 업종을 고르면, 폐업률(ML)·점포당 매출(DL)·쉬운 설명(LLM)을 보여 줍니다.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
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

        <label className="block text-sm">
          업종
          <select className={INPUT_STYLE} value={industry} onChange={(e) => setIndustry(e.target.value)}>
            {(options?.industries ?? [{ industry, industry_code: "" }]).map((item) => (
              <option key={item.industry} value={item.industry}>{item.industry}</option>
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
        {loading ? "AI가 분석하는 중..." : "진단하기"}
      </button>
    </div>
  );
}
