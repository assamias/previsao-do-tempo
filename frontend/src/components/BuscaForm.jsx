import { useState } from "react";

export default function BuscaForm({ onBuscar, carregando }) {
  const [cidade, setCidade] = useState("");

  function enviar(e) {
    e.preventDefault();
    const valor = cidade.trim();
    if (valor) onBuscar(valor);
  }

  return (
    <form onSubmit={enviar} autoComplete="off">
      <input
        type="text"
        aria-label="Nome da cidade"
        value={cidade}
        onChange={(e) => setCidade(e.target.value)}
        placeholder="Buscar cidade..."
        required
      />
      <button type="submit" disabled={carregando}>
        {carregando ? "..." : "Buscar"}
      </button>
    </form>
  );
}