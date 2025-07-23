import { getAppConfig } from '@/lib/utils';
import { headers } from 'next/headers';
import logo from "../images/logo.jpeg";

interface AppLayoutProps {
  children: React.ReactNode;
}


export default async function AppLayout({ children }: AppLayoutProps) {
  const hdrs = await headers();
  const { companyName, logoDark } = await getAppConfig(hdrs);

  return (
    <>
      <header className="fixed top-0 left-0 z-50 hidden w-full flex-row justify-between p-6 md:flex">
        <a
          rel="noopener noreferrer"
          href=""
          className="scale-100 transition-transform duration-300 hover:scale-110"
        >
          <img src={logo.src} alt="Logo" className="h-10 w-auto" />
        </a>
        <span className="text-foreground font-mono text-xs font-bold tracking-wider uppercase">
          OpenCode Built
        </span>
      </header>
      {children}
    </>
  );
}
