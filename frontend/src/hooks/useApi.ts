import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getStatistics, getJobs, getJobById, deleteJob, processDocument } from "../api/services";

export const useStatistics = () => {
  return useQuery({
    queryKey: ["statistics"],
    queryFn: getStatistics,
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useJobs = (page: number, limit: number, workflowAction?: string, status?: string, vendorName?: string) => {
  return useQuery({
    queryKey: ["jobs", page, limit, workflowAction, status, vendorName],
    queryFn: () => getJobs(page, limit, workflowAction, status, vendorName),
    refetchInterval: 10000,
  });
};

export const useJobDetails = (jobId: string) => {
  return useQuery({
    queryKey: ["job", jobId],
    queryFn: () => getJobById(jobId),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const data = query.state?.data;
      if (data && !["COMPLETED", "FAILED"].includes(data.status)) {
        return 3000;
      }
      return false;
    },
  });
};

export const useProcessDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: processDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
      queryClient.invalidateQueries({ queryKey: ["statistics"] });
    },
  });
};

export const useDeleteJob = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteJob,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["jobs"] });
      queryClient.invalidateQueries({ queryKey: ["statistics"] });
    },
  });
};
