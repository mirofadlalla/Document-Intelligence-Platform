import { Link, useLocation } from "react-router-dom";
import { BrainCircuit, Moon, Sun, Activity } from "lucide-react";
import { useEffect, useState } from "react";
import { Button } from "../ui/Button";
import { apiClient } from "../../api/client";

export function Navbar() {
  const [isDark, setIsDark] = useState(true);
  const [isHealthy, setIsHealthy] = useState(true);
  const location = useLocation();

  useEffect(() => {
    // Add dark mode by default
    document.documentElement.classList.add("dark");
    
    // Check API health
    apiClient.get("/health")
      .then(() => setIsHealthy(true))
      .catch(() => setIsHealthy(false));
  }, []);

  const toggleDark = () => {
    document.documentElement.classList.toggle("dark");
    setIsDark(!isDark);
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center px-4 md:px-8 mx-auto">
        <Link to="/" className="mr-6 flex items-center space-x-2">
          <BrainCircuit className="h-6 w-6 text-primary" />
          <span className="hidden font-bold sm:inline-block">
            Document Intelligence
          </span>
        </Link>
        <div className="flex flex-1 items-center space-x-4 text-sm font-medium">
          <Link
            to="/"
            className={`transition-colors hover:text-foreground/80 ${
              location.pathname === "/" ? "text-foreground" : "text-foreground/60"
            }`}
          >
            Dashboard
          </Link>
          <Link
            to="/history"
            className={`transition-colors hover:text-foreground/80 ${
              location.pathname.startsWith("/history") || location.pathname.startsWith("/jobs")
                ? "text-foreground"
                : "text-foreground/60"
            }`}
          >
            History
          </Link>
        </div>
        <div className="flex items-center justify-end space-x-4">
          <div className="flex items-center space-x-1.5 text-sm font-medium text-muted-foreground">
            <Activity className={`h-4 w-4 ${isHealthy ? "text-green-500" : "text-red-500"}`} />
            <span className="hidden sm:inline-block">{isHealthy ? "API Healthy" : "API Offline"}</span>
          </div>
          <Button variant="ghost" size="icon" onClick={toggleDark}>
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </nav>
  );
}
