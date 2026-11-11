const ICONE_URL = (codigo) => `https://openweathermap.org/img/wn/${codigo}@4x.png`;

export default function Resultado({ clima }) {
  return (
    <section className="resultado" key={clima.nome}>
      <div className="local">{clima.nome}, {clima.pais}</div>
      <div className="data">Agora</div>

      <div className="principal">
        <img src={ICONE_URL(clima.icone)} alt={clima.descricao} />
        <div className="temperatura">
          {clima.temperatura}
          <sup>°C</sup>
        </div>
      </div>

      <p className="descricao">{clima.descricao}</p>

      <div className="detalhes">
        <div className="item"><span>Sensação</span><strong>{clima.sensacao}°C</strong></div>
        <div className="item"><span>Umidade</span><strong>{clima.umidade}%</strong></div>
        <div className="item"><span>Vento</span><strong>{clima.vento} km/h</strong></div>
        <div className="item"><span>Pressão</span><strong>{clima.pressao} hPa</strong></div>
      </div>
    </section>
  );
}