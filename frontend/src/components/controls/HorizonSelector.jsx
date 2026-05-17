import { HORIZONS } from '../../utils/constants'

export default function HorizonSelector({ value, onChange }) {
  return (
    <div className="segmented" role="group" aria-label="Forecast horizon">
      {HORIZONS.map((weeks) => (
        <button
          className={value === weeks ? 'active' : ''}
          key={weeks}
          type="button"
          onClick={() => onChange(weeks)}
        >
          {weeks}W
        </button>
      ))}
    </div>
  )
}
