import type { ProcessResponse } from "../../types";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { CheckCircle2, AlertCircle, XCircle } from "lucide-react";

export function ProcessResultView({ result }: { result: ProcessResponse }) {
  const getWorkflowBadge = (action: string) => {
    switch (action) {
      case "APPROVE":
        return <Badge variant="success">Approved</Badge>;
      case "ROUTE_TO_HUMAN_REVIEW":
        return <Badge variant="warning">Human Review</Badge>;
      case "REJECT":
        return <Badge variant="destructive">Rejected</Badge>;
      default:
        return <Badge>{action}</Badge>;
    }
  };

  return (
    <div className="grid gap-6 md:grid-cols-2">
      {/* Metadata & Extraction */}
      <div className="space-y-6">
        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle>Extraction Summary</CardTitle>
              {getWorkflowBadge(result.workflow_action)}
            </div>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt className="text-muted-foreground font-medium">Vendor</dt>
                <dd className="font-semibold">{result.extraction.vendor_name || "N/A"}</dd>
              </div>
              <div>
                <dt className="text-muted-foreground font-medium">Invoice Number</dt>
                <dd className="font-semibold">{result.extraction.invoice_number || "N/A"}</dd>
              </div>
              <div>
                <dt className="text-muted-foreground font-medium">Raw Total</dt>
                <dd>${result.extraction.raw_total?.toFixed(2) || "0.00"}</dd>
              </div>
              <div>
                <dt className="text-muted-foreground font-medium">Discount</dt>
                <dd>{result.extraction.applied_discount_percentage || 0}%</dd>
              </div>
              <div>
                <dt className="text-muted-foreground font-medium">Calculated Final</dt>
                <dd className="font-bold text-primary">${result.validation.final_calculated_total?.toFixed(2) || "0.00"}</dd>
              </div>
              <div>
                <dt className="text-muted-foreground font-medium">Confidence Score</dt>
                <dd className="font-medium text-blue-600 dark:text-blue-400">
                  {(result.validation.confidence_score * 100).toFixed(0)}%
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Raw Output</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="rounded-md bg-muted p-4 overflow-auto max-h-[300px]">
              <pre className="text-xs text-foreground">
                {JSON.stringify(result.extraction, null, 2)}
              </pre>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Validation */}
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Validation Results</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <ValidationRule
                name="Required Fields Valid"
                isValid={result.validation.required_fields_valid}
              />
              <ValidationRule
                name="Invoice Number Valid"
                isValid={result.validation.invoice_number_valid}
              />
              <ValidationRule
                name="Vendor Exists"
                isValid={result.validation.vendor_exists}
              />
              <ValidationRule
                name="Price Calculation Valid"
                isValid={result.validation.price_calculation_valid}
              />
              <ValidationRule
                name="Line Items Match Delivery"
                isValid={result.validation.line_items_match_delivery}
              />
            </div>

            {result.validation.errors.length > 0 && (
              <div className="mt-4 p-3 border border-destructive/50 bg-destructive/10 rounded-md">
                <h4 className="text-sm font-semibold flex items-center text-destructive mb-2">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  Errors
                </h4>
                <ul className="text-xs space-y-1 text-destructive">
                  {result.validation.errors.map((err, idx) => (
                    <li key={idx}>• {err}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.validation.warnings.length > 0 && (
              <div className="mt-4 p-3 border border-yellow-500/50 bg-yellow-500/10 rounded-md">
                <h4 className="text-sm font-semibold flex items-center text-yellow-600 dark:text-yellow-500 mb-2">
                  <AlertCircle className="w-4 h-4 mr-1" />
                  Warnings
                </h4>
                <ul className="text-xs space-y-1 text-yellow-600 dark:text-yellow-500">
                  {result.validation.warnings.map((warn, idx) => (
                    <li key={idx}>• {warn}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ValidationRule({ name, isValid }: { name: string; isValid: boolean }) {
  return (
    <div className="flex items-center justify-between p-2 rounded-md border bg-card">
      <span className="text-sm font-medium text-card-foreground">{name}</span>
      {isValid ? (
        <CheckCircle2 className="w-5 h-5 text-green-500" />
      ) : (
        <XCircle className="w-5 h-5 text-destructive" />
      )}
    </div>
  );
}
