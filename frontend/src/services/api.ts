export interface AnalysisResult {
  metadata: {
    body_type: string;
    skin_color: string;
  };
}

export interface HeadSwapResult {
  image_url: string;
  success: boolean;
  message?: string;
  warning?: string;
  output_image?: string;
}

export class ApiService {
  private static readonly BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5003';

  static async analyzeUserImage(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append('image', file);

    const response = await fetch(`${this.BASE_URL}/api/analyze-user-image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return await response.json();
  }

  static async swapHead(file: File, referenceImagePath: string): Promise<HeadSwapResult> {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('reference_image', referenceImagePath);

    const response = await fetch(`${this.BASE_URL}/api/swap-head`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Head swap failed: ${response.statusText}`);
    }

    const result = await response.json();
    
    // Transform the response to match HeadSwapResult interface
    return {
      image_url: result.output_image || result.pregenerated_image_url,
      success: true,
      message: result.warning || 'Success'
    };
  }
} 