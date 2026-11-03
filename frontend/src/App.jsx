import React, { useState, useEffect } from 'react';
import api from './api/axios';
import {
  Sprout,
  Database,
  Server,
  Layers,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  KeyRound,
  LogOut,
  User,
  Activity,
  Warehouse,
  ShoppingBag,
  Users
} from 'lucide-react';

function App() {
  const [apiStatus, setApiStatus] = useState(null);
  const [loadingStatus, setLoadingStatus] = useState(true);
  const [credentials, setCredentials] = useState({ username: 'admin', password: '' });
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [loginError, setLoginError] = useState('');
  const [loginLoading, setLoginLoading] = useState(false);

  // Probar conexión con la API de Django
  const checkHealth = async () => {
    setLoadingStatus(true);
    try {
      const response = await api.get('');
      setApiStatus(response.data);
    } catch (err) {
      setApiStatus({ error: 'No se pudo conectar al servidor Django en http://localhost:8000/api/' });
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  // Manejo de inicio de sesión JWT
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginLoading(true);
    setLoginError('');
    try {
      const res = await api.post('token/', credentials);
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      setToken(res.data.access);
    } catch (err) {
      setLoginError(err.response?.data?.detail || 'Credenciales inválidas o error de conexión');
    } finally {
      setLoginLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Header */}
      <header className="border-b border-emerald-900/40 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-green-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Sprout className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 via-green-300 to-emerald-200 bg-clip-text text-transparent">
                Agro_Valle
              </span>
              <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0.0
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={checkHealth}
              className="flex items-center space-x-2 text-xs px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 transition"
              title="Revisar conexión con Django"
            >
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              <span>Verificar API</span>
            </button>
            {token ? (
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-xs px-3 py-1.5 rounded-lg bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Cerrar Sesión</span>
              </button>
            ) : null}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full space-y-10">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-700/50 text-emerald-300 text-sm">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Arquitectura desacoplada: Django REST + React + PostgreSQL
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white">
            Plataforma Agrícola <span className="text-emerald-400">Agro_Valle</span>
          </h1>
          <p className="max-w-2xl mx-auto text-slate-400 text-base sm:text-lg">
            Sistema integral para la gestión agrícola, control de producción, inventarios, compras y ventas.
          </p>
        </div>

        {/* Stack Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Base de Datos */}
          <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400">
                <Database className="w-5 h-5" />
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                Conectado
              </span>
            </div>
            <div>
              <h3 className="font-semibold text-white">Base de Datos</h3>
              <p className="text-xs text-slate-400">PostgreSQL 16 / 17</p>
            </div>
            <div className="text-xs text-slate-300 bg-slate-800/60 p-2 rounded-lg font-mono">
              DB: agrovalle (5432)
            </div>
          </div>

          {/* Backend */}
          <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                <Server className="w-5 h-5" />
              </div>
              {loadingStatus ? (
                <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                  Comprobando...
                </span>
              ) : apiStatus?.status === 'online' ? (
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Online
                </span>
              ) : (
                <span className="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium flex items-center gap-1">
                  En espera
                </span>
              )}
            </div>
            <div>
              <h3 className="font-semibold text-white">Backend</h3>
              <p className="text-xs text-slate-400">Django 6.1 + REST Framework</p>
            </div>
            <div className="text-xs text-slate-300 bg-slate-800/60 p-2 rounded-lg font-mono truncate">
              http://localhost:8000/api/
            </div>
          </div>

          {/* Frontend */}
          <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="w-10 h-10 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400">
                <Layers className="w-5 h-5" />
              </div>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                Activo
              </span>
            </div>
            <div>
              <h3 className="font-semibold text-white">Frontend</h3>
              <p className="text-xs text-slate-400">React + Vite + Tailwind CSS</p>
            </div>
            <div className="text-xs text-slate-300 bg-slate-800/60 p-2 rounded-lg font-mono">
              Puerto: 5173
            </div>
          </div>

          {/* Autenticación */}
          <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <span className={`text-xs px-2 py-0.5 rounded font-medium ${token ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-400'}`}>
                {token ? 'Sesión Activa' : 'SimpleJWT'}
              </span>
            </div>
            <div>
              <h3 className="font-semibold text-white">Seguridad</h3>
              <p className="text-xs text-slate-400">Tokens Bearer / JWT</p>
            </div>
            <div className="text-xs text-slate-300 bg-slate-800/60 p-2 rounded-lg font-mono">
              /api/token/
            </div>
          </div>
        </div>

        {/* Sección interactiva: Test de Autenticación o Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Card de Inicio de Sesión / JWT */}
          <div className="lg:col-span-1 p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl">
            <div className="flex items-center space-x-3 mb-5">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                <KeyRound className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-semibold text-white">Prueba de Autenticación</h3>
                <p className="text-xs text-slate-400">Solicitud de Token JWT a Django</p>
              </div>
            </div>

            {token ? (
              <div className="space-y-4">
                <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-sm space-y-2">
                  <div className="flex items-center gap-2 font-medium">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ¡Autenticado con éxito!
                  </div>
                  <p className="text-xs text-slate-400 break-all font-mono bg-slate-900/80 p-2 rounded">
                    Token: {token.slice(0, 35)}...
                  </p>
                </div>
                <button
                  onClick={handleLogout}
                  className="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium text-sm transition"
                >
                  Cerrar Sesión
                </button>
              </div>
            ) : (
              <form onSubmit={handleLogin} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Usuario</label>
                  <input
                    type="text"
                    value={credentials.username}
                    onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-sm text-white focus:outline-none focus:border-emerald-500"
                    placeholder="admin"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Contraseña</label>
                  <input
                    type="password"
                    value={credentials.password}
                    onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-sm text-white focus:outline-none focus:border-emerald-500"
                    placeholder="admin123"
                    required
                  />
                  <span className="text-[11px] text-slate-500">Superusuario creado por defecto: admin / admin123</span>
                </div>

                {loginError && (
                  <div className="p-3 rounded-lg bg-red-950/50 border border-red-800 text-red-300 text-xs flex items-center gap-2">
                    <XCircle className="w-4 h-4 shrink-0" />
                    <span>{loginError}</span>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={loginLoading}
                  className="w-full py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-medium text-sm transition shadow-lg shadow-emerald-600/20"
                >
                  {loginLoading ? 'Conectando...' : 'Obtener Token JWT'}
                </button>
              </form>
            )}
          </div>

          {/* Próximos Módulos del Proyecto */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl flex flex-col justify-between">
            <div>
              <h3 className="font-semibold text-white mb-1">Módulos del Sistema Agro_Valle</h3>
              <p className="text-xs text-slate-400 mb-5">Estructura preparada para implementar las entidades de negocio:</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                    <Sprout className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-slate-200">Cultivos & Parcelas</h4>
                    <p className="text-xs text-slate-400">Gestión de lotes, siembras, cosechas y riegos.</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                    <Warehouse className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-slate-200">Inventario & Insumos</h4>
                    <p className="text-xs text-slate-400">Semillas, fertilizantes, pesticidas y maquinaria.</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
                    <ShoppingBag className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-slate-200">Ventas & Clientes</h4>
                    <p className="text-xs text-slate-400">Órdenes de compra, pedidos, precios y despachos.</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-start space-x-3">
                  <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
                    <Users className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-slate-200">Usuarios & Roles</h4>
                    <p className="text-xs text-slate-400">Administradores, agrónomos, operadores y supervisores.</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Carpetas organizadas: <code>/backend</code> y <code>/frontend</code></span>
              <span className="text-emerald-400 font-medium">Listo para desarrollo</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
