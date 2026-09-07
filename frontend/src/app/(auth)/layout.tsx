export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-sidebar to-brand-700 p-6">
      {children}
    </div>
  );
}
