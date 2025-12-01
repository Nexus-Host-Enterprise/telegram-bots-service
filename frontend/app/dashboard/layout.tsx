import { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="container mx-auto py-6">
      <div>{children}</div>
    </div>
  );
}
