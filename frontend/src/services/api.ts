// API service for the JD Sports frontend
// This provides the interface for communicating with the backend
// Backend URL is configured via NEXT_PUBLIC_API_URL environment variable

export interface AnalysisResult {
  metadata: {
    gender: string;
    body_type: string;
    skin_color: string;
  };
  success: boolean;
  message: string;
}

export interface HeadSwapResult {
  output_image: string;
  analysis: AnalysisResult;
  pregenerated_image_url: string;
  warning?: string;
}

export class ApiService {
  private static baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5003';

  static async analyzeUserImage(file: File): Promise<AnalysisResult> {
    // Create FormData to send the file
    const formData = new FormData();
    
    // Ensure the file has a proper name with extension
    let fileName = file.name;
    if (!fileName || !fileName.includes('.')) {
      // If no filename or no extension, create one based on MIME type
      const extension = file.type.split('/')[1] || 'jpg';
      fileName = `uploaded_image.${extension}`;
    }
    
    // Create a new File object with the proper name
    const fileWithName = new File([file], fileName, { type: file.type });
    formData.append('image', fileWithName);

    console.log('Sending analyze request to:', `${this.baseUrl}/api/analyze-user-image`);
    console.log('File size:', file.size, 'bytes');
    console.log('File type:', file.type);
    console.log('File name:', fileName);

    try {
      const response = await fetch(`${this.baseUrl}/api/analyze-user-image`, {
        method: 'POST',
        body: formData,
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Error response:', errorData);
        throw new Error(`Analysis failed: ${response.statusText} - ${errorData.error || ''}`);
      }

      const result = await response.json();
      console.log('Analysis result:', result);
      return result;
    } catch (error) {
      console.error('Analysis error:', error);
      throw new Error('Failed to analyze image. Please try again.');
    }
  }

  static async swapHead(file: File, referenceImagePath: string): Promise<HeadSwapResult> {
    const formData = new FormData();
    
    // Ensure the file has a proper name with extension
    let fileName = file.name;
    if (!fileName || !fileName.includes('.')) {
      // If no filename or no extension, create one based on MIME type
      const extension = file.type.split('/')[1] || 'jpg';
      fileName = `uploaded_image.${extension}`;
    }
    
    // Create a new File object with the proper name
    const fileWithName = new File([file], fileName, { type: file.type });
    formData.append('image', fileWithName);
    formData.append('reference_image', referenceImagePath);

    console.log('Sending swap-head request to:', `${this.baseUrl}/api/swap-head`);
    console.log('File size:', file.size, 'bytes');
    console.log('File type:', file.type);
    console.log('File name:', fileName);
    console.log('Reference image path:', referenceImagePath);

    try {
      const response = await fetch(`${this.baseUrl}/api/swap-head`, {
        method: 'POST',
        body: formData,
      });

      console.log('Swap-head response status:', response.status);
      console.log('Swap-head response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Swap-head error response:', errorData);
        throw new Error(`Head swap failed: ${response.statusText} - ${errorData.error || ''}`);
      }

      const result = await response.json();
      console.log('Swap-head result:', result);
      return result;
    } catch (error) {
      console.error('Head swap error:', error);
      throw new Error('Failed to process try-on. Please try again.');
    }
  }
} 