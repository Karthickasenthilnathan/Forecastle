export default function ProductPicker({ products = [], value, onChange }) {
  return (
    <label className="select-control">
      <span>Product</span>
      <select value={value || ''} onChange={(event) => onChange(Number(event.target.value))}>
        {products.map((product) => (
          <option key={product.id} value={product.id}>
            {product.sku} · {product.name}
          </option>
        ))}
      </select>
    </label>
  )
}
