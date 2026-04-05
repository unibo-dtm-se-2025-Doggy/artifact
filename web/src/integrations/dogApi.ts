export type BreedIdentificationResult = {
  breed: string;
  advice: string;
};

type ApiDetail = {
  msg?: string;
};

type ApiErrorResponse = {
  error?: string;
  detail?: ApiDetail[];
};

export interface IDogApiClient {
  identifyBreed(file: File): Promise<BreedIdentificationResult>;
}

const getErrorMessage = (data: unknown): string | null => {
  if (typeof data !== "object" || data === null) return null;

  const payload = data as ApiErrorResponse;
  if (payload.error) return payload.error;

  const detail = payload.detail;
  if (Array.isArray(detail) && detail.length > 0 && detail[0]?.msg) {
    return String(detail[0].msg);
  }
  return null;
};

export class DogApiClient implements IDogApiClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string = import.meta.env.VITE_API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async identifyBreed(file: File): Promise<BreedIdentificationResult> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseUrl}/api/v1/dog-from-photo`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || `AI server error: ${response.status}`);
    }

    const data = await response.json();
    const apiError = getErrorMessage(data);
    if (apiError) throw new Error(apiError);

    return { breed: data.breed, advice: data.advice };
  }
}

export const dogApiClient = new DogApiClient();
