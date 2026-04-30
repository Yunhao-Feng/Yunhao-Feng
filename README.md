# Yunhao Feng · Personal Homepage

一个淡雅、简洁、支持中英文切换（默认英文）的个人学术主页模板，适合作为求职/学术展示主页。

## 本地预览

你可以直接双击 `index.html` 打开，也可以用本地服务器：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 内容来源

- 头像：`resume/avatar.jpg`
- 教育/实习/研究方向/成果：根据 `resume/body.tex` 整理
- Google Scholar：
  `https://scholar.google.com/citations?user=7xD7XIUAAAAJ&hl=zh-CN`
- GitHub 高星仓库：前端运行时通过 GitHub API 自动按 star 加载

## 如何发布为 GitHub Pages（详细教程）

> 适用于仓库：`Yunhao-Feng/Yunhao-Feng`（用户主页仓库）

### 方式 A（推荐，最简单）

1. 确保仓库根目录有 `index.html`（本仓库已完成）。
2. 进入 GitHub 仓库页面 → `Settings` → `Pages`。
3. 在 **Build and deployment** 下：
   - **Source** 选择 `Deploy from a branch`
   - **Branch** 选择 `main`（或你的默认分支）
   - 文件夹选择 `/ (root)`
4. 点击 `Save`。
5. 等待 1~3 分钟，GitHub 会生成访问地址。
   - 对用户主页仓库（`<username>/<username>`）通常是：
     `https://<username>.github.io/`

### 方式 B（如果你后续想加构建工具）

使用 GitHub Actions 自动部署（适合未来接入 React/Vite 等）。当前纯静态页面不必用此方式。

## 你可以继续自定义的点

- 修改 `index.html` 中的 sections 结构
- 修改 `styles.css` 中颜色、留白、字体
- 修改 `script.js` 中中英文文案（`i18n`）
- 若想固定展示论文列表，可把 publication 列表迁移到单独的 JSON 文件

## 文件结构

- `index.html`：主页主体
- `styles.css`：样式（淡雅玻璃感）
- `script.js`：中英文切换 + GitHub 仓库自动加载

---

如果你愿意，我下一步可以继续帮你做两件事：

1. 增加「论文详情页 + 可筛选标签（Agent Safety / RL / Benchmark）」
2. 增加「简历下载按钮 + 一键复制邮箱 + 深色模式」
