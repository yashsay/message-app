import DarkVeil from "./components/DarkVeil/DarkVeil";
import MessageList from "./components/MessageList";
import Header from "./components/layout/Header";

function App() {

  return (
    <div>
      <DarkVeil />
      <div
        style={{
          width: "100vw",
          minHeight: "100vh",
          overflowX: "hidden",
          position: "relative",
        }}
      >
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
export default App;
