/**
 * Sovereign AI Client for the UI layer.
 * Communicates with the Python AI Gateway via the Neural Bridge.
 */
export class SovereignAIClient {
  private static instance: SovereignAIClient;
  private ws: WebSocket | null = null;
  private readonly token: string = 'sovereign-dev-token'; // In production, retrieve from secure storage

  private constructor() {}

  public static getInstance(): SovereignAIClient {
    if (!SovereignAIClient.instance) {
      SovereignAIClient.instance = new SovereignAIClient();
    }
    return SovereignAIClient.instance;
  }

  /**
   * Requests a completion from a specific provider.
   * All requests are hash-chained and audited by the backend.
   */
  public async requestCompletion(
    provider: 'deepseek' | 'qwen' | 'minimax',
    messages: { role: string; content: string }[],
    parameters: Record<string, any> = {}
  ): Promise<any> {
    const response = await fetch('/api/v1/ai/completion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify({
        provider,
        messages,
        parameters
      })
    });

    if (!response.ok) {
      throw new Error(`AI Request failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Subscribes to AI events from the Neural Bus.
   */
  public subscribeToAIEvents(callback: (event: any) => void): void {
    if (!this.ws) {
      this.ws = new WebSocket(`ws://localhost:8000/ws/organism/neural-bus?token=${this.token}`);
    }

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type.startsWith('AI')) {
        callback(data);
      }
    };
  }
}
