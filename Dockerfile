FROM python:3.13-slim AS base

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS build

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

FROM base AS runtime

# Install runtime dependencies for Brave and Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Brave Browser in runtime
RUN wget -qO- https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/brave-browser-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | tee /etc/apt/sources.list.d/brave-browser-release.list && \
    apt-get update && \
    apt-get install -y brave-browser && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /app/.venv /app/.venv

# Install Playwright system dependencies
RUN /app/.venv/bin/playwright install-deps chromium

COPY . /app

ENV PATH="/app/.venv/bin:$PATH"
ENV BRAVE_EXECUTABLE_PATH="/usr/bin/brave-browser"

CMD ["uv", "run", "fastapi", "dev", "main.py", "--host", "0.0.0.0"]