import { useEffect } from "react";
import BuscaForm from "./components/BuscaForm.jsx";
import Historico from "./components/Historico.jsx";
import Resultado from "./components/Resultado.jsx";
import { useClima } from "./hooks/useClima.js";

export default function App() {
  const { clima, erro, carregando, historico, buscar } = useClima();

  // Aplica o tema no body conforme o clima
  useEffect(() => {
    document.body.className = clima?.tema || "";
  }, [clima]);

  return (
    <main className="card">
      <header>
        <h1>Previsão do Tempo</h1>
      </header>

      <BuscaForm onBuscar={buscar} carregando={carregando} />
      <Historico cidades={historico} onSelecionar={buscar} />

      {erro && (
        <div className="erro" role="alert">
          {erro}
        </div>
      )}
      {clima && !erro && <Resultado clima={clima} />}
    </main>
  );
}