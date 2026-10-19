import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function RequireRole({ roles }) {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return null; // or a spinner component
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (!user?.roles) {
    return <Navigate to="/unauthorized" replace />;
  }

  const hasRole = user.roles.some((userRole) =>
    roles.includes(userRole.role?.name)
  )

  if (!hasRole) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
}

export default RequireRole;