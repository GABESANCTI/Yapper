import { useEffect, useState } from "react";
import api from "../api/yapperApi";
import YapCard from "../components/YapCard";

export default function Home() {
  const [yaps, setYaps] = useState([]);

  useEffect(() => {
    api.get("yaps/").then((res) => {
      setYaps(res.data.results); // se paginado
    });
  }, []);

  return (
    <div>
      <h1>Timeline</h1>
      {yaps.map((yap) => (
        <YapCard key={yap.id} yap={yap} />
      ))}
    </div>
  );
}
