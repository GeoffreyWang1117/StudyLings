# 文档部署指南

本指南介绍如何部署 JAXlings 文档网站。

## 📦 本地预览

### 安装依赖

```bash
# 安装文档构建依赖
pip install -r docs-requirements.txt
```

### 启动开发服务器

```bash
# 在项目根目录运行
mkdocs serve
```

访问 http://127.0.0.1:8000 查看文档。

开发服务器支持热重载，修改文档后自动刷新。

## 🚀 部署选项

### 选项 1: GitHub Pages

最简单的免费部署方式。

#### 自动部署

创建 `.github/workflows/docs.yml`：

```yaml
name: Deploy Docs
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - run: pip install -r docs-requirements.txt
      - run: mkdocs gh-deploy --force
```

#### 手动部署

```bash
mkdocs gh-deploy
```

访问: `https://<username>.github.io/<repo>/`

### 选项 2: Read the Docs

专业的文档托管平台。

#### 配置文件

创建 `.readthedocs.yaml`：

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

mkdocs:
  configuration: mkdocs.yml

python:
  install:
    - requirements: docs-requirements.txt
```

#### 部署步骤

1. 访问 [Read the Docs](https://readthedocs.org/)
2. 连接 GitHub 仓库
3. 导入项目
4. 配置自动构建

访问: `https://<project-name>.readthedocs.io/`

### 选项 3: Netlify

快速且功能强大。

#### 配置文件

创建 `netlify.toml`：

```toml
[build]
  command = "mkdocs build"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.11"

[[plugins]]
  package = "@netlify/plugin-python"
```

#### 部署步骤

1. 访问 [Netlify](https://netlify.com)
2. 连接 GitHub 仓库
3. 构建命令：`mkdocs build`
4. 发布目录：`site`

### 选项 4: Vercel

现代化的部署平台。

#### 配置文件

创建 `vercel.json`：

```json
{
  "buildCommand": "pip install -r docs-requirements.txt && mkdocs build",
  "outputDirectory": "site",
  "framework": null
}
```

## 🔧 构建静态站点

如果需要手动部署到自己的服务器：

```bash
# 构建静态文件
mkdocs build

# 生成的文件在 site/ 目录
ls site/
```

将 `site/` 目录内容复制到 web 服务器即可。

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name docs.jaxlings.com;
    root /var/www/jaxlings-docs;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # 启用 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

## 📝 自定义配置

### 修改主题颜色

编辑 `mkdocs.yml`：

```yaml
theme:
  palette:
    primary: indigo  # 修改主色调
    accent: indigo   # 修改强调色
```

### 添加 Google Analytics

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

### 添加自定义 CSS

1. 创建 `docs/assets/custom.css`
2. 在 `mkdocs.yml` 中引用：

```yaml
extra_css:
  - assets/custom.css
```

## 🔍 SEO 优化

### 添加元数据

在 `mkdocs.yml` 中：

```yaml
site_description: JAX 从入门到精通的完整学习指南
site_author: JAXlings Contributors
```

### 生成 sitemap

MkDocs 自动生成 `sitemap.xml`。

### robots.txt

创建 `docs/robots.txt`：

```
User-agent: *
Allow: /

Sitemap: https://your-domain.com/sitemap.xml
```

## 🌐 多语言支持

如果需要支持多语言：

```yaml
plugins:
  - i18n:
      default_language: zh
      languages:
        zh:
          name: 简体中文
        en:
          name: English
```

## 📊 监控和分析

### 添加 Plausible Analytics

```yaml
extra:
  analytics:
    provider: plausible
    domain: docs.jaxlings.com
```

### 添加 Umami

```html
<!-- 在 theme 的 extra 中 -->
<script async defer data-website-id="xxx" src="https://umami.example.com/umami.js"></script>
```

## 🐛 故障排查

### 构建失败

```bash
# 检查依赖
pip list | grep mkdocs

# 重新安装
pip install --upgrade -r docs-requirements.txt

# 清除缓存
rm -rf site/
```

### 样式问题

清除浏览器缓存或使用无痕模式测试。

### 数学公式不显示

确保 `mkdocs.yml` 包含：

```yaml
markdown_extensions:
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
```

## 📦 持续集成/部署

### GitHub Actions 完整示例

```yaml
name: Build and Deploy Docs

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('docs-requirements.txt') }}

      - name: Install dependencies
        run: pip install -r docs-requirements.txt

      - name: Build docs
        run: mkdocs build --strict

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        run: mkdocs gh-deploy --force
```

## ✅ 部署检查清单

部署前确认：

- [ ] 所有文档链接正常
- [ ] 数学公式渲染正确
- [ ] 代码高亮显示正常
- [ ] 移动端显示良好
- [ ] 搜索功能正常
- [ ] 导航结构清晰
- [ ] SEO 元数据完整

## 📚 相关资源

- [MkDocs 官方文档](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [Read the Docs 文档](https://docs.readthedocs.io/)

---

如有问题，请在 GitHub Issues 中反馈。
