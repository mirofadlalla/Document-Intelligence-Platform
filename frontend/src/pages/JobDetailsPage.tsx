import { useParams, Link } from "react-router-dom";
import { useJobDetails } from "../hooks/useApi";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Skeleton } from "../components/ui/Skeleton";
import { ChevronLeft, CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { ProcessResultView } from "../components/workflow/ProcessResultView";
import type { ProcessResponse } from "../types";

export function JobDetailsPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const { data: job, isLoading, error } = useJobDetails(jobId!);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
        <h2 className="text-xl font-semibold">Job not found</h2>
        <p className="text-muted-foreground mt-2">The requested job could not be found or an error occurred.</p>
        <Link to="/history">
          <Button className="mt-4" variant="outline">Back to History</Button>
        </Link>
      </div>
    );
  }

  // Map to ProcessResponse for the shared view
  const processResponse: ProcessResponse | null = job.extraction && job.validation && job.workflow_action ? {
    metadata: job.metadata,
    extraction: job.extraction,
    validation: job.validation,
    workflow_action: job.workflow_action
  } : null;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to="/history">
            <Button variant="ghost" size="icon">
              <ChevronLeft className="h-5 w-5" />
            </Button>
          </Link>
          <div>
            <h2 className="text-2xl font-bold tracking-tight">Job Details</h2>
            <p className="text-sm text-muted-foreground font-mono mt-1">{job.job_id}</p>
          </div>
        </div>
        <Badge variant={job.status === "COMPLETED" ? "success" : job.status === "FAILED" ? "destructive" : "secondary"}>
          {job.status}
        </Badge>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <TimelineItem title="Received" time={job.created_at} isDone={true} />
                <TimelineItem title="Processing" time={job.updated_at} isDone={["PARSING", "EXTRACTING", "VALIDATING", "COMPLETED"].includes(job.status)} />
                <TimelineItem title="Completed" time={job.updated_at} isDone={job.status === "COMPLETED"} isError={job.status === "FAILED"} />
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Metadata</CardTitle>
            </CardHeader>
            <CardContent>
               <dl className="space-y-2 text-sm">
                 <div>
                   <dt className="text-muted-foreground">Source Email</dt>
                   <dd className="font-medium">{job.metadata.source_email}</dd>
                 </div>
                 <div>
                   <dt className="text-muted-foreground mt-2">Attachments ({job.attachments.length})</dt>
                   <dd className="font-medium">
                     {job.attachments.map((a, i) => <div key={i} className="truncate">{a.filename}</div>)}
                   </dd>
                 </div>
               </dl>
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2">
          {processResponse ? (
            <ProcessResultView result={processResponse} />
          ) : (
            <Card>
              <CardContent className="py-12 flex flex-col items-center justify-center text-muted-foreground">
                {job.status === "FAILED" ? (
                   <>
                     <AlertCircle className="h-8 w-8 mb-2 text-destructive" />
                     <p className="text-destructive font-semibold">Processing Failed</p>
                     <p className="text-sm mt-1">{job.error_message}</p>
                   </>
                ) : (
                   <>
                     <Clock className="h-8 w-8 mb-2 animate-pulse text-primary" />
                     <p>Processing is currently in stage: {job.status}</p>
                   </>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

function TimelineItem({ title, time, isDone, isError }: { title: string, time: string, isDone: boolean, isError?: boolean }) {
  return (
    <div className="flex items-start space-x-3">
       {isError ? (
         <AlertCircle className="h-5 w-5 mt-0.5 text-destructive shrink-0" />
       ) : isDone ? (
         <CheckCircle2 className="h-5 w-5 mt-0.5 text-green-500 shrink-0" />
       ) : (
         <div className="h-5 w-5 mt-0.5 rounded-full border-2 border-muted-foreground shrink-0" />
       )}
       <div>
         <p className={`font-medium ${isDone || isError ? "text-foreground" : "text-muted-foreground"}`}>{title}</p>
         <p className="text-xs text-muted-foreground">{new Date(time).toLocaleString()}</p>
       </div>
    </div>
  );
}
