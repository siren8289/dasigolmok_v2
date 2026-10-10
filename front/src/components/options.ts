// 여러 화면에서 같이 쓰는 스타일·이름표

export const STATUS_INFO: Record<string, { label: string; color: string }> = {
  stable: { label: "안정", color: "bg-emerald-100 text-emerald-800" },
  warning: { label: "주의", color: "bg-amber-100 text-amber-800" },
  danger: { label: "위험", color: "bg-red-100 text-red-800" },
  unknown: { label: "판단 불가", color: "bg-gray-100 text-gray-700" },
};

export const INPUT_STYLE =
  "w-full px-3 py-2 bg-white border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-700";
