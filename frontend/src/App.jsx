import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import YapList from "./components/YapList";
function App() {
  return (
    <div className="App">
      <h1>Yapper</h1>
      <YapList />
    </div>
  );
}

export default App;
