import { Routes, Route } from "react-router-dom";

import AlertsSidebar from "./Components/AlertsSideBar";
import AssetsCard from "./Components/AssetsCards";
import Navbar from "./Components/Navbar";
import StatusCard from "./Components/StatusCards";

import AssetDiagnosis from "./pages/AssetDiagnosis";
import VibrationStream from "./Components/vibrationStream";
import Footer from "./Components/Footer";
import Config from "./pages/Config";

export default function App() {
  return (
    <div className="bg-light min-h-screen text-slate-900">
      <Navbar />

      <Routes>
        <Route
          path="/"
          element={
            <main className="max-w-[1440px] mx-auto px-6 py-8">
              <StatusCard />
              <div className="grid grid-cols-12 gap-8">
                <div className="col-span-12 lg:col-span-9 space-y-8">
                  <AssetsCard />
                  <VibrationStream />
                </div>
                <div className="col-span-12 lg:col-span-3">
                  <AlertsSidebar />
                </div>
              </div>
            </main>
          }
        />

        <Route path="/diagnosis" element={<AssetDiagnosis />} />
        <Route path="/config" element={<Config />} />
      </Routes>
      <Footer />
    </div>
  );
}
