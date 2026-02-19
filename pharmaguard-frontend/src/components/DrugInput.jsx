const DRUGS = [
  'WARFARIN',
  'CODEINE',
  'CLOPIDOGREL',
  'SIMVASTATIN',
  'AZATHIOPRINE',
  'FLUOROURACIL',
]

const DRUG_DESCRIPTIONS = {
  WARFARIN:      'Anticoagulant — CYP2C9',
  CODEINE:       'Opioid analgesic — CYP2D6',
  CLOPIDOGREL:   'Antiplatelet — CYP2C19',
  SIMVASTATIN:   'Statin — SLCO1B1',
  AZATHIOPRINE:  'Immunosuppressant — TPMT',
  FLUOROURACIL:  'Chemotherapy — DPYD',
}

export default function DrugInput({ onSelect }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-400 mb-2">
        Select Drug
      </label>
      <div className="grid grid-cols-2 gap-2">
        {DRUGS.map((drug) => (
          <button
            key={drug}
            type="button"
            onClick={() => onSelect(drug)}
            className="text-left p-3 rounded-lg border border-gray-700 bg-gray-900 
                       hover:border-cyan-500 hover:bg-cyan-900/10 transition-all
                       focus:outline-none focus:border-cyan-400 group"
          >
            <p className="text-white text-sm font-medium group-hover:text-cyan-300">
              {drug}
            </p>
            <p className="text-gray-500 text-xs mt-0.5">
              {DRUG_DESCRIPTIONS[drug]}
            </p>
          </button>
        ))}
      </div>
    </div>
  )
}
