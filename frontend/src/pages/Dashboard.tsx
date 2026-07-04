import { useStatistics } from "../hooks/useApi";
import { UploadPanel } from "../components/forms/UploadPanel";
import { StatisticCard } from "../components/cards/StatisticCard";
import { FileText, CheckCircle, AlertTriangle, XCircle, Activity } from "lucide-react";

export function Dashboard() {
  const { data: stats, isLoading } = useStatistics();

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Overview of document processing pipeline and new submissions.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <StatisticCard
          title="Total Jobs"
          value={stats?.total_jobs || 0}
          icon={FileText}
          isLoading={isLoading}
        />
        <StatisticCard
          title="Approved"
          value={stats?.approved_jobs || 0}
          icon={CheckCircle}
          isLoading={isLoading}
        />
        <StatisticCard
          title="Human Review"
          value={stats?.review_jobs || 0}
          icon={AlertTriangle}
          isLoading={isLoading}
        />
        <StatisticCard
          title="Rejected"
          value={stats?.rejected_jobs || 0}
          icon={XCircle}
          isLoading={isLoading}
        />
        <StatisticCard
          title="Avg Confidence"
          value={`${((stats?.average_confidence || 0) * 100).toFixed(1)}%`}
          icon={Activity}
          isLoading={isLoading}
        />
      </div>

      <div className="grid gap-4">
        <UploadPanel />
      </div>
    </div>
  );
}
