import axios from "axios";
import type {
  Claim,
  Document,
  ChatMessage,
  CreateClaimRequest,
} from "../types";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_V1 = `${API_URL}/api/v1`;

const api = axios.create({
  baseURL: API_V1,
  headers: {
    "Content-Type": "application/json",
  },
});

// Claims API
export const claimsApi = {
  create: async (data: CreateClaimRequest): Promise<Claim> => {
    const response = await api.post<Claim>("/claims/", data);
    return response.data;
  },

  getById: async (id: number): Promise<Claim> => {
    const response = await api.get<Claim>(`/claims/${id}`);
    return response.data;
  },

  getByUser: async (userId: string): Promise<Claim[]> => {
    const response = await api.get<Claim[]>(`/claims/user/${userId}`);
    return response.data;
  },

  list: async (): Promise<Claim[]> => {
    const response = await api.get<Claim[]>("/claims/");
    return response.data;
  },
};

// Documents API
export const documentsApi = {
  upload: async (
    file: File,
    claimId: number,
    documentType: string,
  ): Promise<Document> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("claim_id", claimId.toString());
    formData.append("document_type", documentType);

    const response = await api.post<Document>("/documents/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  },

  getByClaimId: async (claimId: number): Promise<Document[]> => {
    const response = await api.get<Document[]>(`/documents/claim/${claimId}`);
    return response.data;
  },

  getById: async (id: number): Promise<Document> => {
    const response = await api.get<Document>(`/documents/${id}`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/documents/${id}`);
  },
};

// Chatbot API
export const chatbotApi = {
  sendMessage: async (
    message: string,
    sessionId?: string,
  ): Promise<ChatMessage> => {
    const response = await api.post<ChatMessage>("/chatbot/chat", {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  submitFeedback: async (
    messageId: number,
    isHelpful: boolean,
  ): Promise<void> => {
    await api.post("/chatbot/feedback", null, {
      params: { message_id: messageId, is_helpful: isHelpful },
    });
  },
};

export default api;
