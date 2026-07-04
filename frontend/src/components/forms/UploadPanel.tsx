import { useState } from "react";
import { useForm as useRHForm } from "react-hook-form";
import { FileUp, File, X, AlertCircle, Loader2 } from "lucide-react";
import { Button } from "../ui/Button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/Card";
import { useProcessDocument } from "../../hooks/useApi";
import type { ProcessResponse } from "../../types";
import { ProcessResultView } from "../workflow/ProcessResultView";

interface UploadFormData {
  subject: string;
  body: string;
  attachments: FileList;
}

export function UploadPanel() {
  const { register, handleSubmit, reset } = useRHForm<UploadFormData>();
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const processMutation = useProcessDocument();
  const [result, setResult] = useState<ProcessResponse | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const onSubmit = async (data: UploadFormData) => {
    if (selectedFiles.length === 0) return;
    setResult(null);

    const formData = new FormData();
    formData.append("subject", data.subject);
    formData.append("body", data.body);
    selectedFiles.forEach((file) => {
      formData.append("attachments", file);
    });

    try {
      const res = await processMutation.mutateAsync(formData);
      setResult(res);
      reset();
      setSelectedFiles([]);
    } catch (error) {
      console.error("Processing failed", error);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Process New Documents</CardTitle>
          <CardDescription>Upload invoices or delivery notes for AI extraction and validation.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Email Subject</label>
                <input
                  {...register("subject", { required: true })}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                  placeholder="e.g. Invoice INV-2023 for October"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Email Body</label>
                <input
                  {...register("body")}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                  placeholder="Optional routing instructions"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Attachments</label>
              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-muted/50 border-muted-foreground/25">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <FileUp className="w-8 h-8 mb-3 text-muted-foreground" />
                    <p className="mb-2 text-sm text-muted-foreground"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                    <p className="text-xs text-muted-foreground">PDF, PNG, JPG, DOCX (MAX. 10MB)</p>
                  </div>
                  <input type="file" multiple className="hidden" onChange={handleFileChange} accept=".pdf,.png,.jpg,.jpeg,.docx" />
                </label>
              </div>
            </div>

            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm font-medium">Selected Files ({selectedFiles.length})</p>
                <div className="grid gap-2 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                  {selectedFiles.map((file, idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 text-sm border rounded-md">
                      <div className="flex items-center space-x-2 truncate">
                        <File className="h-4 w-4 shrink-0 text-primary" />
                        <span className="truncate">{file.name}</span>
                      </div>
                      <Button type="button" variant="ghost" size="icon" className="h-6 w-6 shrink-0" onClick={() => removeFile(idx)}>
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex justify-end pt-4">
              <Button type="button" variant="outline" className="mr-2" onClick={() => { reset(); setSelectedFiles([]); }}>
                Clear
              </Button>
              <Button type="submit" disabled={processMutation.isPending || selectedFiles.length === 0}>
                {processMutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {processMutation.isPending ? "Processing..." : "Process Documents"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Inline result below upload section */}
      {processMutation.isPending && (
        <Card className="animate-pulse">
           <CardContent className="flex flex-col items-center justify-center p-12 space-y-4">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <p className="text-lg font-medium">Pipeline is extracting and validating...</p>
           </CardContent>
        </Card>
      )}

      {processMutation.isError && (
        <Card className="border-destructive">
          <CardContent className="p-6 flex items-center space-x-4 text-destructive">
             <AlertCircle className="h-6 w-6" />
             <div>
               <p className="font-semibold">Processing Failed</p>
               <p className="text-sm">{processMutation.error?.message || "An unexpected error occurred"}</p>
             </div>
          </CardContent>
        </Card>
      )}

      {result && !processMutation.isPending && (
        <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
           <ProcessResultView result={result} />
        </div>
      )}
    </div>
  );
}
