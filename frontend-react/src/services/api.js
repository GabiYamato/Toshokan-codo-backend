import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

class APIService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getModules() {
    try {
      const response = await this.client.get('/api/modules');
      return response.data;
    } catch (error) {
      console.error('Error fetching modules:', error);
      throw error;
    }
  }

  async buildApp(prompt, sessionId = null) {
    try {
      const response = await this.client.post('/api/build', {
        prompt,
        session_id: sessionId,
      });
      return response.data;
    } catch (error) {
      console.error('Error building app:', error);
      throw error;
    }
  }

  async getBuildStatus(sessionId) {
    try {
      const response = await this.client.get(`/api/build/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting build status:', error);
      throw error;
    }
  }

  async getFiles(sessionId) {
    try {
      const response = await this.client.get(`/api/files/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting files:', error);
      throw error;
    }
  }

  async getFileContent(sessionId, filePath) {
    try {
      const response = await this.client.get(`/api/file/${sessionId}/${filePath}`);
      return response.data;
    } catch (error) {
      console.error('Error getting file content:', error);
      throw error;
    }
  }

  async sendChatMessage(message) {
    try {
      const response = await this.client.post('/api/chat', message);
      return response.data;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }

  async getChatHistory(sessionId) {
    try {
      const response = await this.client.get(`/api/chat/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  }
}

export default new APIService();
