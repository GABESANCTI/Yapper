export default function YapCard({ yap }) {
  return (
    <div style={{ border: "1px solid #ccc", marginBottom: "10px", padding: "10px" }}>
      <p><strong>{yap.author}</strong></p>
      <p>{yap.conteudo}</p>
      <p><small>{new Date(yap.criado_em).toLocaleString()}</small></p>
    </div>
  );
}
// This component displays a single Yap card with author, content, and creation date.