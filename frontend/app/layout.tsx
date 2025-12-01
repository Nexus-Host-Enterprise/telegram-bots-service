import "./globals.css";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import Navbar from "@/components/Navbar";

export const metadata = { title: "Nexus Bot Platform" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <QueryClientProvider client={queryClient}>
          <Navbar />
          <main>{children}</main>
        </QueryClientProvider>
      </body>
    </html>
  );
}
