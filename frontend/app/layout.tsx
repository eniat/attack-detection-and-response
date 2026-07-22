import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Cloud Identity Detection and Response",
  description: "Identity attack detection and response dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-slate-950 text-slate-100">
          <nav className="border-b border-slate-800 bg-slate-900 px-6 py-4">
            <div className="flex gap-6">
              <Link href="/" className="font-bold">
                Identity Detection and Response
              </Link>
              <Link href="/events">Events</Link>
              <Link href="/alerts">Alerts</Link>
              <Link href="/cases">Cases</Link>
            </div>
          </nav>

          <main className="p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
