FROM oven/bun:alpine as base

FROM base AS deps
WORKDIR /deps
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

FROM base as run
WORKDIR /run
RUN apk --no-cache add curl
COPY --from=deps /deps/node_modules node_modules
COPY . .

HEALTHCHECK CMD curl -f http://localhost:4000 || exit 1
ENV NODE_ENV production
CMD [ "bun", "./src/index.ts" ]
