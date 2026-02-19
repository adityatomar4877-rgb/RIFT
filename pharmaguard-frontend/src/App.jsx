import { useState } from 'react'
import { analyzeVCF } from './api'
import DrugInput from './components/DrugInput'
import FileUpload from './components/FileUpload'
import ResultCard from './components/ResultCard'

export default function App() {
  const [file, setFile]       = useState(null)
  const [drug, setDrug]       = useState('')
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const canAnalyze = file && drug && !loading

  const handleAnalyze = async () => {
    if (!canAnalyze) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeVCF(file, drug)
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDrugSelect = (selectedDrug) => {
    setDrug(selectedDrug)
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/50 backdrop-blur sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-cyan-400">PharmaGuard</h1>
            <p className="text-gray-500 text-xs">Pharmacogenomic Risk Prediction System</p>
          </div>
          <span className="text-xs text-gray-600 border border-gray-700 px-2 py-1 rounded">
            RIFT 2026
          </span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">

        {/* Hero */}
        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-2">
            Predict Drug Risk from Genetic Data
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            Upload a VCF file and select a drug to get CPIC-aligned pharmacogenomic
            risk predictions with AI-generated clinical explanations.
          </p>
        </div>

        {/* Input Panel */}
        <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <FileUpload onFileSelect={setFile} />
            <DrugInput onSelect={handleDrugSelect} />
          </div>

          {/* Selected drug pill */}
          {drug && (
            <div className="mb-4 flex items-center gap-2">
              <span className="text-gray-500 text-sm">Selected drug:</span>
              <span className="bg-cyan-900/40 border border-cyan-700 text-cyan-300 
                               text-sm px-3 py-0.5 rounded-full font-mono">
                {drug}
              </span>
              <button
                onClick={() => { setDrug(''); setResult(null) }}
                className="text-gray-600 hover:text-gray-400 text-xs ml-1"
              >
                ✕ clear
              </button>
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={!canAnalyze}
            className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:opacity-30 disabled:cursor-not-allowed
                       text-black font-bold py-3 rounded-xl transition-all text-lg"
          >
            {loading
              ? <span className="flex items-center justify-center gap-2">
                  <span className="animate-spin">⟳</span> Analyzing...
                </span>
              : 'Analyze Pharmacogenomic Risk'}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-950 border border-red-700 rounded-xl text-red-300 text-sm">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Results */}
        {result && <ResultCard data={result} />}

        {/* Footer */}
        <footer className="mt-12 text-center text-gray-700 text-xs">
          PharmaGuard · RIFT 2026 Hackathon · Pharmacogenomics / Explainable AI Track
        </footer>
      </main>
    </div>
  )
}
