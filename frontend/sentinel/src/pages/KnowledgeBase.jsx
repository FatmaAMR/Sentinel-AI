import { useMemo, useState } from "react";
import KnowledgeNav from "../Components/Knowledge/KnowledgeNav";
import PageHeader from "../Components/Knowledge/PageHeader";
import UploadCard from "../Components/Knowledge/UploadCard";
import DocumentLibrary from "../Components/Knowledge/DocumentLibrary";
import ContextExplorer from "../Components/Knowledge/ContextExplorer";
import StatsRow from "../Components/Knowledge/StatsRow";
import CTASection from "../Components/Knowledge/CTASection";
import KnowledgeFooter from "../Components/Knowledge/KnowledgeFooter";

export default function KnowledgeBase() {
  const [dark, setDark] = useState(false);

  useMemo(() => {
    const root = document.documentElement;
    if (dark) root.classList.add("dark");
    else root.classList.remove("dark");
  }, [dark]);

  return (
    <div className="bg-light dark:bg-dark text-slate-900 dark:text-slate-100 min-h-screen flex flex-col transition-colors">
      <KnowledgeNav dark={dark} onToggleDark={() => setDark((v) => !v)} />

      <main className="max-w-7xl mx-auto px-6 py-12 flex-1">
        <PageHeader />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-8">
            <UploadCard />
            <DocumentLibrary />
          </div>

          <div className="lg:col-span-4">
            <ContextExplorer />
          </div>
        </div>

        <StatsRow />
        <CTASection />
      </main>

      <KnowledgeFooter />
    </div>
  );
}
