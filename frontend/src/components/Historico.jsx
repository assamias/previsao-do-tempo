export default function Historico({ cidades, onSelecionar }) {
  if (cidades.length === 0) return null;

  return (
    <div className="historico">
      {cidades.map((cidade) => (
        <button key={cidade} type="button" onClick={() => onSelecionar(cidade)}>
          {cidade}
        </button>
      ))}
    </div>
  );
}