import { Link } from "react-router-dom";
import { AlertOctagon } from "lucide-react";
import { Button } from "../components/ui/Button";

export function ErrorPage() {
  return (
    <div className="flex h-[80vh] flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-500">
      <AlertOctagon className="h-20 w-20 text-destructive mb-4" />
      <h1 className="text-4xl font-bold tracking-tight mb-2">Something went wrong</h1>
      <p className="text-muted-foreground mb-8 max-w-md">
        An unexpected error occurred in the application. Please try refreshing the page or navigating back to safety.
      </p>
      <Link to="/">
        <Button size="lg">Return to Dashboard</Button>
      </Link>
    </div>
  );
}
