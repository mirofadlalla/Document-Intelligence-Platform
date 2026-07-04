import { useState } from "react";
import { Link } from "react-router-dom";
import { useJobs } from "../hooks/useApi";
import { Card, CardContent, CardHeader } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Skeleton } from "../components/ui/Skeleton";
import { Search, ChevronLeft, ChevronRight, Inbox } from "lucide-react";

export function HistoryPage() {
  const [page, setPage] = useState(1);
  const [vendorName, setVendorName] = useState("");
  const limit = 10;

  const { data: jobs, isLoading } = useJobs(page, limit, undefined, undefined, vendorName || undefined);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Processing History</h2>
        <p className="text-muted-foreground">
          View past extraction jobs and their workflow routing results.
        </p>
      </div>

      <Card>
        <CardHeader className="py-4">
          <div className="flex items-center space-x-2">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search by vendor..."
                className="flex h-9 w-full rounded-md border border-input bg-transparent pl-9 pr-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                value={vendorName}
                onChange={(e) => {
                  setVendorName(e.target.value);
                  setPage(1);
                }}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <table className="w-full text-sm text-left text-muted-foreground">
              <thead className="text-xs text-foreground uppercase bg-muted/50 border-b">
                <tr>
                  <th className="px-4 py-3">Processed At</th>
                  <th className="px-4 py-3">Vendor</th>
                  <th className="px-4 py-3">Invoice</th>
                  <th className="px-4 py-3">Workflow</th>
                  <th className="px-4 py-3">Confidence</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  Array.from({ length: 5 }).map((_, i) => (
                    <tr key={i} className="border-b">
                      <td className="px-4 py-3"><Skeleton className="h-4 w-24" /></td>
                      <td className="px-4 py-3"><Skeleton className="h-4 w-32" /></td>
                      <td className="px-4 py-3"><Skeleton className="h-4 w-20" /></td>
                      <td className="px-4 py-3"><Skeleton className="h-4 w-24" /></td>
                      <td className="px-4 py-3"><Skeleton className="h-4 w-12" /></td>
                      <td className="px-4 py-3"><Skeleton className="h-4 w-16 ml-auto" /></td>
                    </tr>
                  ))
                ) : jobs && jobs.length > 0 ? (
                  jobs.map((job) => (
                    <tr key={job.job_id} className="border-b hover:bg-muted/50 transition-colors">
                      <td className="px-4 py-3 font-medium text-foreground">
                        {new Date(job.created_at).toLocaleString()}
                      </td>
                      <td className="px-4 py-3">{job.extraction?.vendor_name || "-"}</td>
                      <td className="px-4 py-3">{job.extraction?.invoice_number || "-"}</td>
                      <td className="px-4 py-3">
                        {job.workflow_action === "APPROVE" && <Badge variant="success">Approved</Badge>}
                        {job.workflow_action === "ROUTE_TO_HUMAN_REVIEW" && <Badge variant="warning">Review</Badge>}
                        {job.workflow_action === "REJECT" && <Badge variant="destructive">Rejected</Badge>}
                        {!job.workflow_action && <Badge variant="secondary">{job.status}</Badge>}
                      </td>
                      <td className="px-4 py-3">
                        {job.validation?.confidence_score !== undefined 
                          ? `${(job.validation.confidence_score * 100).toFixed(0)}%` 
                          : "-"}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Link to={`/jobs/${job.job_id}`}>
                          <Button variant="ghost" size="sm">Details</Button>
                        </Link>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={6} className="px-4 py-12 text-center">
                      <div className="flex flex-col items-center justify-center text-muted-foreground">
                         <Inbox className="h-8 w-8 mb-2 opacity-50" />
                         <p>No jobs found.</p>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <div className="flex items-center justify-between mt-4">
            <span className="text-sm text-muted-foreground">
              Page {page}
            </span>
            <div className="space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1 || isLoading}
              >
                <ChevronLeft className="h-4 w-4 mr-1" /> Prev
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setPage((p) => p + 1)}
                disabled={!jobs || jobs.length < limit || isLoading}
              >
                Next <ChevronRight className="h-4 w-4 ml-1" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
