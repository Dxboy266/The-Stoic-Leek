# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app

# 复制依赖文件
COPY package.json package-lock.json ./
RUN npm ci

# 复制源代码
COPY . .

# 接收构建参数
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# 构建
RUN npm run build

# 运行阶段 - 使用 standalone 输出
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# 复制 standalone 构建产物
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
