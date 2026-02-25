import AppHeader from "../Components/Diagnosis/AppHeader";
import LeftRail from "../Components/Diagnosis/LeftRail";
import AssetTopBar from "../Components/Diagnosis/AssetTopBar";
import TelemetryPanel from "../Components/Diagnosis/TelemetryPanel";
import DiagnosisPanel from "../Components/Diagnosis/DiagnosisPanel";
import AppFooter from "../Components/Diagnosis/AppFooter";

export default function AssetDiagnosis() {
  return (
    <div className="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 min-h-screen flex flex-col">
      <AppHeader />

      <main className="flex-1 flex overflow-hidden">
        <LeftRail />

        <div className="flex-1 flex flex-col min-w-0">
          <AssetTopBar />

          <div className="flex-1 flex gap-0 p-0 overflow-hidden">
            <TelemetryPanel />
            <DiagnosisPanel />
          </div>
        </div>
      </main>

      <AppFooter />
    </div>
  );
}
