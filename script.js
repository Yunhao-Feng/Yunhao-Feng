const i18n = {
  en: {
    name: 'Yunhao Feng',
    title: 'Ph.D. Student · Agent Safety / Computer-Use Agents',
    summary: 'Focused on safety, evaluation, and training of Computer-Use/Coding Agents, with hands-on experience in benchmark construction, runtime monitoring, tool-use risk modeling, process-level verifier design, and agentic RL from real interaction trajectories.',
    education: 'Education', experience: 'Experience', publications: 'Selected Publications & Works', skills: 'Research Interests', awards: 'Awards', repos: 'Top GitHub Repositories', reposHint: 'Auto-loaded from GitHub API by stars.',
    edu1: 'National University of Defense Technology, Ph.D. in Management Science and Engineering (Engineering)',
    edu2: 'Fudan University, Visiting Student',
    edu3: 'National University of Defense Technology, M.Eng. in Electronic Information',
    edu4: 'Southwestern University of Finance and Economics, B.Sc. in Information Management and Information System',
    exp1: 'Alibaba Future Living Lab · Algorithm Engineer Intern (Coding Agent Safety)',
    exp2: 'JD Explore Academy · Algorithm Engineer Intern',
    expDesc: 'Studied safety attack surfaces across planning, tool-use, and code execution; designed runtime guardrails and trajectory-driven safety learning pipelines.',
    award1: 'Champion, Huawei Cup China Graduate AI Innovation Competition (LLM Security Track)',
    award2: 'Third Prize, China Graduate Electronic Design Contest',
    award3: 'Second Prize, National College Mathematical Modeling Contest'
  },
  zh: {
    name: '冯云浩',
    title: '博士生 · Agent 安全 / Computer-Use Agent',
    summary: '聚焦 Computer-Use / Coding Agent 的安全、评测与训练，具备 benchmark 构建、运行时监控、tool-use 风险建模、过程级 verifier 设计及基于实机轨迹的 Agentic RL 研究经验。',
    education: '教育经历', experience: '实习经历', publications: '代表性成果', skills: '研究方向', awards: '获奖情况', repos: 'GitHub 高星仓库', reposHint: '通过 GitHub API 按 Star 自动加载。',
    edu1: '国防科技大学，管理科学与工程（工学）博士',
    edu2: '复旦大学，访问学生',
    edu3: '国防科技大学，电子信息硕士',
    edu4: '西南财经大学，信息管理与信息系统本科',
    exp1: '阿里巴巴未来生活实验室 · 实习算法工程师（Coding Agent 安全）',
    exp2: '京东探索研究院 · 算法工程师实习生',
    expDesc: '围绕 planning、tool-use、代码执行等链路研究安全攻击面，并设计运行时风控与轨迹驱动的安全学习机制。',
    award1: '华为杯·中国研究生人工智能创新大赛（大模型安全赛道）全国冠军',
    award2: '中国研究生电子设计竞赛技术赛三等奖',
    award3: '全国大学生数学建模竞赛二等奖'
  }
};
let current = 'en';
const applyLang = () => {
  document.documentElement.lang = current;
  document.querySelectorAll('[data-i18n]').forEach(el => el.textContent = i18n[current][el.dataset.i18n] || el.textContent);
  document.getElementById('langToggle').textContent = current === 'en' ? '中文' : 'EN';
};
document.getElementById('langToggle').addEventListener('click', () => { current = current === 'en' ? 'zh' : 'en'; applyLang(); });

async function loadRepos() {
  try {
    const resp = await fetch('https://api.github.com/users/Yunhao-Feng/repos?per_page=100');
    const repos = await resp.json();
    const top = repos.filter(r => !r.fork).sort((a,b) => b.stargazers_count - a.stargazers_count).slice(0, 6);
    const container = document.getElementById('repoList');
    container.innerHTML = top.map(r => `<a class="repo" href="${r.html_url}" target="_blank" rel="noreferrer"><strong>${r.name}</strong><div>${r.description || ''}</div><small>⭐ ${r.stargazers_count}</small></a>`).join('');
  } catch {
    document.getElementById('repoList').textContent = 'Failed to load repositories.';
  }
}

document.getElementById('year').textContent = new Date().getFullYear();
applyLang();
loadRepos();
