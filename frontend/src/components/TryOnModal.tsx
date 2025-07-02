import { useState, useRef, useEffect } from 'react';
import { ApiService, AnalysisResult, HeadSwapResult } from '../services/api';

interface TryOnModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedColor: string;
}

export function TryOnModal({ isOpen, onClose, selectedColor }: TryOnModalProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState<'upload' | 'result'>('upload');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [result, setResult] = useState<HeadSwapResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [revealProgress, setRevealProgress] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const revealRef = useRef<HTMLDivElement>(null);
  const revealDuration = 20000;
  const [referenceImageUrl, setReferenceImageUrl] = useState<string | null>(null);
  const [isDiffusing, setIsDiffusing] = useState(false);
  const maxReveal = 0.65; // Reveal up to 65% (just below the neck)
  const [apiResult, setApiResult] = useState<HeadSwapResult | null>(null);

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select a valid image file');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    // Store the file in state
    setUploadedFile(file);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImage(e.target?.result as string);
      setError(null);
    };
    reader.readAsDataURL(file);
  };

  const handleSwapHead = async () => {
    setIsLoading(true);
    setError(null);
    setShowResult(false);
    setRevealProgress(0);
    setIsDiffusing(true);
    setApiResult(null);
    try {
      // Step 1: Analyze
      const analysisResult = await ApiService.analyzeUserImage(uploadedFile!);
      setAnalysis(analysisResult);
      // Step 2: Headswap
      const referenceImagePath = `bodytypes/headswapper/${analysisResult.metadata.body_type}/jordan_red_hoodie_reference_${analysisResult.metadata.skin_color}.png`;
      setReferenceImageUrl(`/images/${referenceImagePath}`);
      // Start reveal animation up to maxReveal
      let start = Date.now();
      let animationFrame: number;
      let finished = false;
      let revealDone = false;
      let apiDone = false;
      let result: HeadSwapResult | null = null;
      const finish = () => {
        setRevealProgress(1); // Instantly reveal the full image
        setTimeout(() => {
          setResult(result!);
          setShowResult(true);
          setIsLoading(false);
          setIsDiffusing(false);
        }, 200);
      };
      const animate = () => {
        if (finished) return;
        const elapsed = Date.now() - start;
        let progress = Math.min(elapsed / revealDuration, 1) * maxReveal;
        setRevealProgress(progress);
        if (progress < maxReveal && !apiDone) {
          animationFrame = requestAnimationFrame(animate);
        } else {
          revealDone = true;
          if (apiDone) {
            finished = true;
            finish();
          }
        }
      };
      animationFrame = requestAnimationFrame(animate);
      // Start API call in parallel
      ApiService.swapHead(uploadedFile!, referenceImagePath).then((apiResult) => {
        result = apiResult;
        setApiResult(apiResult);
        apiDone = true;
        if (!revealDone) {
          // If reveal is not done, finish it instantly
          setRevealProgress(1);
          revealDone = true;
        }
        if (revealDone) {
          finished = true;
          finish();
        }
      });
    } catch (err) {
      setIsLoading(false);
      setIsDiffusing(false);
      setError(err instanceof Error ? err.message : 'Try-On failed');
    }
  };

  const handleReset = () => {
    setCurrentStep('upload');
    setUploadedImage(null);
    setUploadedFile(null);
    setAnalysis(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Try-On with AI</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Progress Steps (only Upload and Result) */}
        <div className="flex justify-center mb-6">
          <div className="flex space-x-4">
            <div className={`flex items-center ${currentStep === 'upload' ? 'text-blue-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${currentStep === 'upload' ? 'border-blue-600 bg-blue-600 text-white' : 'border-gray-300'}`}>
                1
              </div>
              <span className="ml-2 text-sm">Upload Photo</span>
            </div>
            <div className={`flex items-center ${currentStep === 'result' ? 'text-green-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${currentStep === 'result' ? 'border-green-600 bg-green-600 text-white' : 'border-gray-300'}`}>
                2
              </div>
              <span className="ml-2 text-sm">Result</span>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Step 1: Upload */}
        {currentStep === 'upload' && !isDiffusing && !showResult && (
          <div className="text-center">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
              />
              {!uploadedImage ? (
                <div>
                  <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <p className="mt-2 text-sm text-gray-600">
                    Click to upload a photo of yourself
                  </p>
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                  >
                    Choose File
                  </button>
                </div>
              ) : (
                <div>
                  <img
                    src={uploadedImage}
                    alt="Uploaded"
                    className="mx-auto max-h-64 rounded"
                  />
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="mt-4 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                  >
                    Change Photo
                  </button>
                </div>
              )}
            </div>
            {uploadedImage && (
              <button
                onClick={handleSwapHead}
                disabled={isLoading}
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {isLoading ? 'Processing...' : 'Try On'}
              </button>
            )}
          </div>
        )}

        {/* Step 2: Diffusion Reveal + Result */}
        {isDiffusing && referenceImageUrl && !showResult && (
          <div className="flex flex-col items-center justify-center min-h-[400px]">
            <div className="mb-4 text-lg font-semibold text-gray-700">Generating your Try-On...</div>
            <div
              ref={revealRef}
              style={{
                width: '100%',
                maxWidth: 350,
                height: 500,
                overflow: 'hidden',
                position: 'relative',
                background: '#f3f4f6',
                borderRadius: 12,
                boxShadow: '0 2px 16px rgba(0,0,0,0.08)'
              }}
            >
              <img
                src={referenceImageUrl}
                alt="Diffusing..."
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  position: 'absolute',
                  left: 0,
                  bottom: 0,
                  clipPath: `inset(${100 - revealProgress * 100}% 0% 0% 0%)`,
                  transition: 'clip-path 0.2s linear',
                }}
              />
              <div style={{
                position: 'absolute',
                left: 0,
                bottom: 0,
                width: '100%',
                height: 6,
                background: '#e5e7eb',
                borderRadius: 3,
                overflow: 'hidden',
              }}>
                <div style={{
                  width: `${(revealProgress / maxReveal) * 100}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #60a5fa, #38bdf8)',
                  transition: 'width 0.2s linear',
                }} />
              </div>
            </div>
            <div className="mt-4 text-sm text-gray-500">AI is working its magic... ({Math.round((revealProgress / maxReveal) * 100)}%)</div>
          </div>
        )}
        {showResult && result && (
          <div className="text-center">
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded mb-4">
              <h3 className="font-semibold">Try-On Complete!</h3>
              <p className="text-sm mt-1">See how you look in the {selectedColor} quarter-zip pullover</p>
              {result.warning && (
                <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-3 py-2 rounded mt-2 text-xs">
                  ⚠️ {result.warning}
                </div>
              )}
            </div>
            <div className="flex justify-center mb-6">
              <div>
                <img src={result.output_image} alt="Result" className="mx-auto max-h-[500px] rounded shadow-lg" style={{ maxWidth: '100%', width: 'auto', height: 'auto' }} />
              </div>
            </div>
            <button
              onClick={handleReset}
              className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
            >
              Try Another Photo
            </button>
          </div>
        )}
      </div>
    </div>
  );
} 