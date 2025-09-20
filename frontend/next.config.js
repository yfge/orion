/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Do not fail the build in CI/Docker if ESLint errors exist.
    // We still run `npm run lint` locally/CI separately.
    ignoreDuringBuilds: true,
  },
  output: 'standalone',
}

module.exports = nextConfig
