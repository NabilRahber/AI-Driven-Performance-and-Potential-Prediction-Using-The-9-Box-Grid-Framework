const GRID_DATA = [
  // Row 2 (High Performance) - top row visually
  { row: 2, col: 0, label: 'Solid Performer', cls: 'high-low' },
  { row: 2, col: 1, label: 'High Performer', cls: 'high-med' },
  { row: 2, col: 2, label: 'Star', cls: 'high-high' },
  // Row 1 (Medium Performance)
  { row: 1, col: 0, label: 'Talent Risk', cls: 'med-low' },
  { row: 1, col: 1, label: 'Core Player', cls: 'med-med' },
  { row: 1, col: 2, label: 'High Potential', cls: 'med-high' },
  // Row 0 (Low Performance) - bottom row visually
  { row: 0, col: 0, label: 'Bad Hire', cls: 'low-low' },
  { row: 0, col: 1, label: 'Up or Out', cls: 'low-med' },
  { row: 0, col: 2, label: 'Rough Diamond', cls: 'low-high' },
]

export default function NineBoxGrid({ prediction }) {
  const activeRow = prediction?.grid_position?.row
  const activeCol = prediction?.grid_position?.col

  return (
    <div style={{ position: 'relative', paddingLeft: 28 }}>
      <div className="axis-title-y">Performance →</div>
      <div style={{ display: 'flex', gap: 8 }}>
        <div className="y-labels">
          <span className="y-label">High</span>
          <span className="y-label">Medium</span>
          <span className="y-label">Low</span>
        </div>
        <div style={{ flex: 1 }}>
          <div className="nine-box-grid">
            {GRID_DATA.map((cell, i) => {
              const isActive = activeRow === cell.row && activeCol === cell.col
              return (
                <div
                  key={i}
                  className={`grid-cell ${cell.cls} ${isActive ? 'active' : ''}`}
                >
                  <span className="cell-label">{cell.label}</span>
                  {isActive && prediction && (
                    <span style={{
                      fontSize: '0.65rem',
                      marginTop: 4,
                      opacity: 0.8,
                      fontWeight: 700,
                      color: 'var(--accent-primary)'
                    }}>
                      ● HERE
                    </span>
                  )}
                </div>
              )
            })}
          </div>
          <div className="x-labels">
            <span className="x-label">Low</span>
            <span className="x-label">Medium</span>
            <span className="x-label">High</span>
          </div>
          <div className="axis-title">Potential →</div>
        </div>
      </div>
    </div>
  )
}
