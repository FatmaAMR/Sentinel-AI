import { useEffect, useState } from "react";
import TopNav from "../Components/HistoryTrends/TopNav";
import FiltersSidebar from "../Components/HistoryTrends/FiltersSidebar";
import AIInsightCard from "../Components/HistoryTrends/AIInsightCard";
import TrendVisualization from "../Components/HistoryTrends/TrendVisualization";
import HistoricalTimeline from "../Components/HistoryTrends/HistoricalTimeline";
import BottomStats from "../Components/HistoryTrends/BottomStats";
import StatusFooter from "../Components/HistoryTrends/StatusFooter";

export default function HistoryTrends() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const root = document.documentElement;
    if (dark) root.classList.add("dark");
    else root.classList.remove("dark");
  }, [dark]);

  return (
    <div className="bg-light dark:bg-[#0F172A] text-slate-900 dark:text-slate-100 min-h-screen transition-colors duration-200">
      <TopNav dark={dark} onToggleDark={() => setDark((v) => !v)} />

      <main className="max-w-[1600px] mx-auto p-6 grid grid-cols-12 gap-6">
        <aside className="col-span-12 lg:col-span-3 space-y-6">
          <FiltersSidebar />
          <AIInsightCard />
        </aside>

        <div className="col-span-12 lg:col-span-9 space-y-6">
          <TrendVisualization />
          <HistoricalTimeline />
          <BottomStats />
        </div>
      </main>

      <StatusFooter />
    </div>
  );
}
