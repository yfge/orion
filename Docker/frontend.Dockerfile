FROM node:20-alpine AS deps
WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
# Use pnpm if lockfile exists; fallback to npm
RUN if [ -f pnpm-lock.yaml ]; then \
      corepack enable && corepack prepare pnpm@9.12.1 --activate && pnpm install --frozen-lockfile; \
    else \
      npm ci; \
    fi

FROM node:20-alpine AS build
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=deps /app/node_modules ./node_modules
COPY frontend ./
# Build in standalone output for smaller runtime image
RUN npm run build || (corepack enable && corepack prepare pnpm@9.12.1 --activate && pnpm build)

FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

# Only copy standalone output if available, fallback to full .next
COPY --from=build /app/.next/standalone ./
COPY --from=build /app/.next/static ./.next/static
COPY --from=build /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]

