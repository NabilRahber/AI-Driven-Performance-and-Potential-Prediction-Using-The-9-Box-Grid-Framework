export default function ModelInfo({ info }) {
  if (!info || !info.models) return null

  return (
    <div className="glass-card" style={{ padding: 0 }}>
      <div className="section-title">Model Comparison</div>
      <div className="model-cards" style={{ padding: '0 24px 20px' }}>
        {Object.entries(info.models).map(([name, data]) => (
          <div
            key={name}
            className={`model-card ${name === info.best_model ? 'best' : ''}`}
          >
            <div className="model-name">{name}</div>
            <div className="model-acc">{data.accuracy}%</div>
            {name === info.best_model && (
              <div className="model-badge">★ Best Model</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
