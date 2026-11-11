import { useCallback, useEffect, useRef, useState } from "react";

const CHAVE_HISTORICO = "previsao_historico";
const HISTORICO_MAX = 4;

function lerHistorico() {
  try {
    return JSON.parse(localStorage.getItem(CHAVE_HISTORICO)) || [];
  } catch {
    return [];
  }
}

export function useClima() {
  const [clima, setClima] = useState(null);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [historico, setHistorico] = useState(lerHistorico);
  const controllerRef = useRef(null);

  useEffect(() => {
    localStorage.setItem(CHAVE_HISTORICO, JSON.stringify(historico));
  }, [historico]);

  const buscar = useCallback(async (cidade) => {
    controllerRef.current?.abort();
    const controller = new AbortController();
    controllerRef.current = controller;

    setErro("");
    setCarregando(true);

    try {
      const resposta = await fetch(
        `/api/clima?cidade=${encodeURIComponent(cidade)}`,
        { signal: controller.signal }
      );
      const dados = await resposta.json();

      if (!resposta.ok) {
        setErro(dados.erro || "Erro ao buscar o clima.");
        return;
      }

      setClima(dados);
      setHistorico((atual) =>
        [dados.nome, ...atual.filter((c) => c.toLowerCase() !== dados.nome.toLowerCase())]
          .slice(0, HISTORICO_MAX)
      );
    } catch (e) {
      if (e.name === "AbortError") return;
      console.error("Falha na busca de clima:", e);
      setErro("Não foi possível conectar ao servidor. Tente novamente.");
    } finally {
      if (controllerRef.current === controller) setCarregando(false);
    }
  }, []);

  return { clima, erro, carregando, historico, buscar };
}