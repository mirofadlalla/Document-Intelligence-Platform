import { apiClient } from "./client";
import type { ProcessingJob, ProcessResponse, Statistics } from "../types";

export const getStatistics = async (): Promise<Statistics> => {
  const { data } = await apiClient.get<Statistics>("/statistics");
  return data;
};

export const getJobs = async (
  page: number = 1,
  limit: number = 20,
  workflowAction?: string,
  status?: string,
  vendorName?: string
): Promise<ProcessingJob[]> => {
  const params = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
  });
  if (workflowAction) params.append("workflow_action", workflowAction);
  if (status) params.append("status", status);
  if (vendorName) params.append("vendor_name", vendorName);

  const { data } = await apiClient.get<ProcessingJob[]>(`/jobs?${params.toString()}`);
  return data;
};

export const getJobById = async (jobId: string): Promise<ProcessingJob> => {
  const { data } = await apiClient.get<ProcessingJob>(`/jobs/${jobId}`);
  return data;
};

export const deleteJob = async (jobId: string): Promise<{ status: string }> => {
  const { data } = await apiClient.delete<{ status: string }>(`/jobs/${jobId}`);
  return data;
};

export const processDocument = async (formData: FormData): Promise<ProcessResponse> => {
  const { data } = await apiClient.post<ProcessResponse>("/process", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return data;
};
