FROM oven/bun:1.1.20-slim

WORKDIR /app
COPY app.js ./

ENV FLAG="ictf{just_a_funny_bug_in_bun_http_handling}"

CMD ["bun", "run", "app.js"]
