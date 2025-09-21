/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Do not fail the build in CI/Docker if ESLint errors exist.
    // We still run `npm run lint` locally/CI separately.
    ignoreDuringBuilds: true,
  },
  output: 'standalone',
  async rewrites() {
    const devTarget = process.env.DEV_API_PROXY || process.env.INTERNAL_API_BASE_URL
    // Dev convenience: proxy same-origin /api to backend if DEV_API_PROXY is provided
    // Example: DEV_API_PROXY=http://127.0.0.1:8000
    if (devTarget) {
      return [{ source: '/api/:path*', destination: `${devTarget.replace(/\/$/, '')}/api/:path*` }]
    }
    return []
  },
}

module.exports = nextConfig
