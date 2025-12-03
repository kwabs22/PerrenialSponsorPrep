/**
 * Clerk Protected Dashboard
 * Showcases: React Router SDK + Reverification
 */
import { ClerkProvider, SignedIn, SignedOut, SignInButton, UserButton, useAuth } from '@clerk/clerk-react';

function Dashboard() {
  const { userId } = useAuth();

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Protected Dashboard</h1>
        <UserButton afterSignOutUrl="/" />
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Welcome!</h2>
        <p>You are signed in as user: {userId}</p>

        <div className="mt-6 space-y-4">
          <div className="p-4 bg-gray-50 rounded">
            <h3 className="font-medium">📊 Analytics</h3>
            <p>View your dashboard analytics</p>
          </div>
          <div className="p-4 bg-gray-50 rounded">
            <h3 className="font-medium">⚙️ Settings</h3>
            <p>Manage your account settings</p>
          </div>
          <div className="p-4 bg-red-50 rounded border border-red-200">
            <h3 className="font-medium text-red-700">🔒 Sensitive Action</h3>
            <p className="text-sm text-red-600">
              This action requires reverification
            </p>
            <button className="mt-2 px-4 py-2 bg-red-500 text-white rounded text-sm">
              Delete Account (Requires Reverification)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
      <div className="min-h-screen bg-gray-100">
        <SignedOut>
          <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
              <h1 className="text-3xl font-bold mb-4">Protected Dashboard</h1>
              <p className="mb-4">Sign in to access the dashboard</p>
              <SignInButton mode="modal">
                <button className="px-6 py-2 bg-blue-500 text-white rounded-lg">
                  Sign In
                </button>
              </SignInButton>
            </div>
          </div>
        </SignedOut>
        <SignedIn>
          <Dashboard />
        </SignedIn>
      </div>
    </ClerkProvider>
  );
}
