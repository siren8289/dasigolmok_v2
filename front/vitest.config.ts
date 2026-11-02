import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    fileParallelism: false,
    reporters: ["default", "json"],
    outputFile: { json: "../qa/automation/results/fe-vitest.json" },
  },
});
