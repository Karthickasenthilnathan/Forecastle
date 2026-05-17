import { ArrowPathIcon, SparklesIcon } from '@heroicons/react/24/outline'
import ProductPicker from '../controls/ProductPicker'
import HorizonSelector from '../controls/HorizonSelector'

export default function Header({
  products,
  selectedProductId,
  onProductChange,
  horizon,
  onHorizonChange,
  onGenerate,
  isGenerating,
  apiUnavailable,
}) {
  return (
    <header className="topbar">
      <div className="title-group">
        <p>Production forecast console</p>
        <h1>Demand outlook</h1>
      </div>

      <div className="toolbar">
        {apiUnavailable ? <span className="status-pill">API unavailable</span> : <span className="status-pill live">API live</span>}
        <ProductPicker products={products} value={selectedProductId} onChange={onProductChange} />
        <HorizonSelector value={horizon} onChange={onHorizonChange} />
        <button className="primary-action" type="button" onClick={onGenerate} disabled={isGenerating}>
          {isGenerating ? <ArrowPathIcon className="spin" /> : <SparklesIcon />}
          <span>{isGenerating ? 'Generating' : 'Generate'}</span>
        </button>
      </div>
    </header>
  )
}
