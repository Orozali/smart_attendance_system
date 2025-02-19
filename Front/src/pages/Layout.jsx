import Navbar from "../components/NavBar/Navbar";
import Footer from "../components/Footer/Footer";
import { Outlet } from "react-router-dom";
export default function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />

      <main>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
