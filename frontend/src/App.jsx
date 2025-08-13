import MessageList from "./components/MessageList";
import Header from "./components/layout/Header";

function App() {
  useEffect(() => {
    const handleScroll = () => {
      const parallax = document.querySelector(".parallax-bg");
      if (parallax) {
        parallax.style.transform = `translateY(${window.scrollY * 0.15}px)`;
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div
      style={{
        width: "100vw",
        minHeight: "100vh",
        overflowX: "hidden",
        background:
          "linear-gradient(120deg, #f8fafc 0%, #b5ead7 50%, #fbc2eb 100%)",
        transition: "background 0.5s",
      }}
    >
      <div
        style={{
          width: "100vw",
          minHeight: "100vh",
          overflowX: "hidden",
          position: "relative",
        }}
      >
        <div className="animated-bg">
          <div className="parallax-bg" />
          <img src="/noise.svg" alt="noise" className="noise-bg" />
        </div>
        <Header />
        <div
          style={{
            maxWidth: 900,
            margin: "0 auto",
            padding: "2rem",
            background: "transparent",
            position: "relative",
            zIndex: 2,
          }}
        >
          <MessageList />
        </div>
      </div>
    </div>
  );
}

import { useEffect } from "react";
export default App;
