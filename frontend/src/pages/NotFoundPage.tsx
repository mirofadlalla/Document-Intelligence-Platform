import { Link } from "react-router-dom";
import { AlertCircle } from "lucide-react";
import { Button } from "../components/ui/Button";

export function NotFoundPage() {
  return (
    <div className="flex h-[80vh] flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-500">
      <AlertCircle className="h-20 w-20 text-muted-foreground mb-4" />
      <h1 className="text-4xl font-bold tracking-tight mb-2">404</h1>
      <h2 className="text-2xl font-semibold mb-4">Page Not Found</h2>
      <p className="text-muted-foreground mb-8 max-w-md">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link to="/">
        <Button size="lg">Return to Dashboard</Button>
      </Link>
    </div>
  );
}
