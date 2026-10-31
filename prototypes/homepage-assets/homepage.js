const paths = {
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/>',
  github:
    '<path d="M9 19c-4.3 1.2-4.3-2.1-6-2.6M15 22v-3.3c0-1 .1-1.5-.5-2 3.3-.4 6.7-1.6 6.7-7.2A5.5 5.5 0 0 0 19.7 5c.2-1 .2-2.1-.2-3.1 0 0-1.2-.4-4.2 1.6a14.5 14.5 0 0 0-7.6 0C4.7 1.5 3.5 1.9 3.5 1.9 3.1 3 3.1 4 3.3 5a5.5 5.5 0 0 0-1.5 4.5c0 5.6 3.4 6.8 6.7 7.2-.6.5-.5 1.3-.5 2V22"/>',
  menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
  'arrow-up-right': '<path d="M6 18 18 6M6 6h12v12"/>',
  'arrow-right': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
  'arrow-down': '<path d="M12 4v16m-6-6 6 6 6-6"/>',
  sparkles:
    '<path d="m12 3 2.6 6.4L21 12l-6.4 2.6L12 21l-2.6-6.4L3 12l6.4-2.6L12 3ZM20 2v4m-2-2h4"/>',
  box: '<path d="m12 3 9 5v9l-9 5-9-5V8l9-5Zm0 9v10M3 8l9 4 9-4M7.5 5.5l9 5"/>',
  layers: '<path d="m12 3 10 5-10 5L2 8l10-5ZM2 12l10 5 10-5M2 16l10 5 10-5"/>',
  database:
    '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
  terminal: '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="m7 9 3 3-3 3m6 0h4"/>',
  network:
    '<rect x="9" y="2" width="6" height="6" rx="1.5"/><rect x="2" y="16" width="6" height="6" rx="1.5"/><rect x="16" y="16" width="6" height="6" rx="1.5"/><path d="M12 8v4m-7 4v-4h14v4"/>',
  pause: '<path d="M9 5v14M15 5v14"/>',
  play: '<path d="m8 4 12 8-12 8V4Z"/>',
  leaf: '<path d="M20 3c-1 5 2 9-3 14A7.1 7.1 0 0 1 7 7c4-4 8-2 13-4ZM4 21l12-12M8 17H4"/>',
  coffee:
    '<path d="M4 9h12v8a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V9Zm12 0h2a3 3 0 0 1 0 6h-2M7 2v3m4-3v3M2 22h18"/>',
  code: '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
};
function icon(name, className = '') {
  return `<svg class="icon ${className}" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths['arrow-right']}</svg>`;
}
document
  .querySelectorAll('[data-icon]')
  .forEach((el) => (el.outerHTML = icon(el.dataset.icon, el.className)));

const DOCS_BASE = 'https://notes.wwkq.top';
document.querySelectorAll('[data-doc]').forEach((el) => {
  el.href = DOCS_BASE + el.dataset.doc;
  el.target = '_blank';
  el.rel = 'noreferrer';
  el.setAttribute('aria-label', `${el.textContent.trim().replace(/\s+/g, ' ')}（新标签页阅读）`);
});
window.mockData = {
  prototype: 'Hi, Agent! / Homepage / V1',
  note: '原型精选内容与路线为人工编排示例，不代表实时更新或用户进度。',
  routes: {
    java: {
      badge: '从熟悉到可能',
      title: '把 Spring 经验，变成 AI 能力。',
      description: '从第一个模型调用开始，逐步加入记忆、检索与工具。',
      steps: [
        ['接入第一个模型', '配置与快速开始', '/frameworks/spring-ai/getting-started/quickstart/'],
        ['掌握 ChatClient', '提示词与流式响应', '/frameworks/spring-ai/core/chat-client/'],
        ['让对话有记忆', '上下文与会话管理', '/frameworks/spring-ai/core/chat-memory/'],
        ['赋予工具能力', '让模型执行行动', '/frameworks/spring-ai/tools/tool-calling/'],
      ],
    },
    python: {
      badge: '从脚本到应用',
      title: '从 Python 出发，构建你的 AI 应用。',
      description: '理解模型调用，学习框架编排，再把知识连接到应用中。',
      steps: [
        ['理解大模型', '能力与使用边界', '/basics/llm-theory/what-is-llm/'],
        ['入门 LangChain', '模型与应用编排', '/frameworks/langchain/langchain-basics/'],
        ['理解 RAG', '让回答有据可依', '/rag/fundamentals/what-is-rag/'],
        ['探索 LangGraph', '有状态的工作流', '/frameworks/langgraph/'],
      ],
    },
    agent: {
      badge: '从调用到构建',
      title: '不止会回答，更要能解决问题。',
      description: '从工程结构理解智能体，连接上下文、规划与外部工具。',
      steps: [
        ['理解 Harness', '模型之外的工程', '/agent/harness/'],
        ['组织上下文', '为决策准备信息', '/agent/context-engineering/'],
        ['构建 Deep Agent', '规划与协作执行', '/frameworks/deepagents/'],
        ['连接 MCP', '开放的工具生态', '/frameworks/spring-ai/mcp/overview/'],
      ],
    },
  },
  articles: [
    ['Spring AI', 'Java · 模型接入与应用开发', '/frameworks/spring-ai/', 'leaf'],
    [
      'ChatClient API',
      'Spring AI · 提示词、模型调用与流式响应',
      '/frameworks/spring-ai/core/chat-client/',
      'terminal',
    ],
    [
      'Chat Memory 对话记忆',
      'Spring AI · 历史消息与会话管理',
      '/frameworks/spring-ai/core/chat-memory/',
      'layers',
    ],
    ['Deep Agents', 'Agent · 规划、委派与工具执行', '/frameworks/deepagents/', 'network'],
    ['RAG 检索增强生成', '知识库 · 文档与向量检索', '/rag/fundamentals/what-is-rag/', 'database'],
    [
      '上下文工程',
      'Context Engineering · 管理模型所需的信息',
      '/agent/context-engineering/',
      'layers',
    ],
    ['Harness 工程', 'Agent · 工具、上下文与执行循环', '/agent/harness/', 'sparkles'],
    ['MCP 协议', 'Spring AI · 客户端与服务端', '/frameworks/spring-ai/mcp/overview/', 'network'],
    ['LangChain 入门', 'Python · 模型应用编排', '/frameworks/langchain/langchain-basics/', 'code'],
    ['LangGraph', '工作流 · 状态与执行图', '/frameworks/langgraph/', 'network'],
    [
      'Tool Calling 工具调用',
      'Spring AI · 让模型执行行动',
      '/frameworks/spring-ai/tools/tool-calling/',
      'terminal',
    ],
    ['AI 编程', '开发工具 · 方法与实践', '/ai-programming/', 'code'],
  ],
};

const tabs = [...document.querySelectorAll('[data-path]')];
function selectPath(key, focus = false) {
  const data = window.mockData.routes[key];
  tabs.forEach((tab) => {
    const active = tab.dataset.path === key;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    if (active && focus) tab.focus();
  });
  const content = document.querySelector('#path-content');
  content.setAttribute('aria-labelledby', `tab-${key}`);
  content.querySelector('.pill').textContent = data.badge;
  content.querySelector('h3').textContent = data.title;
  content.querySelector('.path-intro p').textContent = data.description;
  document.querySelector('#path-steps').innerHTML = data.steps
    .map(
      ([title, desc, url], i) =>
        `<li><a href="${DOCS_BASE + url}" target="_blank" rel="noreferrer" aria-label="${title}（新标签页阅读）"><div class="step-top"><span class="step-number">0${i + 1}</span><span class="step-line"></span></div><h4>${title}</h4><p>${desc}</p></a></li>`,
    )
    .join('');
}
tabs.forEach((tab, i) => {
  tab.addEventListener('click', () => selectPath(tab.dataset.path));
  tab.addEventListener('keydown', (e) => {
    const offset = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
    let next = offset
      ? (i + offset + tabs.length) % tabs.length
      : e.key === 'Home'
        ? 0
        : e.key === 'End'
          ? tabs.length - 1
          : null;
    if (next !== null) {
      e.preventDefault();
      selectPath(tabs[next].dataset.path, true);
    }
  });
});
selectPath('java');

const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  menuButton.setAttribute('aria-label', expanded ? '展开导航' : '收起导航');
  mobileNav.hidden = expanded;
});
mobileNav.querySelectorAll('a').forEach((a) =>
  a.addEventListener('click', () => {
    mobileNav.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '展开导航');
  }),
);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !mobileNav.hidden) {
    mobileNav.hidden = true;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', '展开导航');
    menuButton.focus();
  }
});

const dialog = document.querySelector('#search-dialog');
const input = document.querySelector('#search-input');
const results = document.querySelector('#search-results');
let resultIndex = 0;
function highlightResult(index) {
  const links = [...results.querySelectorAll('a')];
  resultIndex = links.length ? (index + links.length) % links.length : 0;
  links.forEach((a, i) => a.setAttribute('aria-current', String(i === resultIndex)));
  links[resultIndex]?.scrollIntoView({ block: 'nearest' });
}
function renderSearch() {
  const query = input.value.trim().toLocaleLowerCase();
  const found = window.mockData.articles.filter(([title, description]) =>
    `${title} ${description}`.toLocaleLowerCase().includes(query),
  );
  results.innerHTML = found.length
    ? found
        .map(
          ([title, description, url, glyph]) =>
            `<a class="search-result" href="${DOCS_BASE + url}" target="_blank" rel="noreferrer">${icon(glyph)}<span>${title}<small>${description}</small></span>${icon('arrow-up-right', 'result-arrow')}</a>`,
        )
        .join('')
    : '<div class="search-empty">暂未找到相关文章，试试 Spring AI、RAG 或记忆。</div>';
  document.querySelector('#search-count').textContent = query
    ? `${found.length} 条匹配结果`
    : '精选专题与文章';
  highlightResult(0);
}
function openSearch() {
  if (!dialog.open) {
    dialog.showModal();
    input.value = '';
    renderSearch();
    input.focus();
  }
}
document
  .querySelectorAll('.search-trigger')
  .forEach((b) => b.addEventListener('click', openSearch));
document.querySelector('#search-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    e.preventDefault();
    dialog.close();
  }
});
dialog.addEventListener('click', (e) => {
  const r = dialog.getBoundingClientRect();
  if (
    e.target === dialog &&
    (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)
  )
    dialog.close();
});
results.addEventListener('click', (e) => {
  if (e.target.closest('a')) dialog.close();
});
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    if (dialog.open) dialog.close();
    else openSearch();
  }
});
input.addEventListener('input', renderSearch);
input.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    highlightResult(resultIndex + (e.key === 'ArrowDown' ? 1 : -1));
  }
  if (e.key === 'Enter') {
    e.preventDefault();
    results.querySelectorAll('a')[resultIndex]?.click();
  }
});

const sceneElement = document.querySelector('#knowledge-scene');
const motionButton = document.querySelector('#motion-toggle');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let paused = reducedMotion.matches;
function updateMotionButton() {
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.setAttribute('aria-label', paused ? '播放知识网络动画' : '暂停知识网络动画');
  motionButton.innerHTML = icon(paused ? 'play' : 'pause');
}
updateMotionButton();
motionButton.addEventListener('click', () => {
  paused = !paused;
  updateMotionButton();
});
reducedMotion.addEventListener('change', (e) => {
  paused = e.matches;
  updateMotionButton();
});

async function createKnowledgeGraph() {
  const THREE = await import('./vendor/three.module.min.js');
  const canvas = document.querySelector('#knowledge-canvas');
  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    powerPreference: 'low-power',
  });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
  renderer.setClearColor(0x080c0f, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 0.2, 8.5);
  const globe = new THREE.Group();
  globe.rotation.set(0.18, 0.4, -0.16);
  scene.add(globe);
  let seed = 27;
  function random() {
    seed = (seed * 16807) % 2147483647;
    return (seed - 1) / 2147483646;
  }
  const coordinates = [],
    pointColors = [],
    vectors = [];
  const mint = new THREE.Color(0x86f3d3),
    violet = new THREE.Color(0x9586dc),
    blue = new THREE.Color(0x73a6d9);
  const mobile = matchMedia('(max-width: 520px)').matches;
  const count = mobile ? 120 : 200;
  for (let i = 0; i < count; i++) {
    const y = 1 - (i / (count - 1)) * 2;
    const radius = Math.sqrt(1 - y * y);
    const theta = Math.PI * (3 - Math.sqrt(5)) * i;
    const v = new THREE.Vector3(
      Math.cos(theta) * radius,
      y,
      Math.sin(theta) * radius,
    ).multiplyScalar(2.12 + random() * 0.06);
    vectors.push(v);
    coordinates.push(...v.toArray());
    const color = (i % 4 === 0 ? violet : i % 3 === 0 ? blue : mint)
      .clone()
      .multiplyScalar(0.25 + random() * 0.7);
    pointColors.push(color.r, color.g, color.b);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(coordinates, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(pointColors, 3));
  const pointMat = new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    uniforms: { pixelRatio: { value: renderer.getPixelRatio() } },
    vertexShader:
      'attribute vec3 color; varying vec3 vColor; uniform float pixelRatio; void main(){vColor=color;vec4 mv=modelViewMatrix*vec4(position,1.);gl_PointSize=19.*pixelRatio/-mv.z;gl_Position=projectionMatrix*mv;}',
    fragmentShader:
      'varying vec3 vColor; void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,.08,d);gl_FragColor=vec4(vColor,a*.95);}',
  });
  globe.add(new THREE.Points(geo, pointMat));
  const edges = [];
  for (let i = 0; i < vectors.length; i++) {
    for (let j = i + 1; j < vectors.length; j++) {
      if (vectors[i].distanceTo(vectors[j]) < (mobile ? 0.85 : 0.69))
        edges.push(...vectors[i].toArray(), ...vectors[j].toArray());
    }
  }
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(edges, 3));
  const edgeMaterial = new THREE.LineBasicMaterial({
    color: 0x6aaca9,
    transparent: true,
    opacity: 0.11,
    depthWrite: false,
  });
  globe.add(new THREE.LineSegments(edgeGeo, edgeMaterial));
  function orbit(rx, ry, rotation, color, opacity) {
    const points = [];
    for (let i = 0; i <= 180; i++) {
      const a = (i / 180) * Math.PI * 2;
      points.push(new THREE.Vector3(Math.cos(a) * rx, Math.sin(a) * ry, 0));
    }
    const ring = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(points),
      new THREE.LineBasicMaterial({ color, transparent: true, opacity }),
    );
    ring.rotation.set(...rotation);
    scene.add(ring);
    return ring;
  }
  orbit(2.82, 1.2, [0.15, 0.25, 0.43], 0x91a6c9, 0.18);
  orbit(2.65, 1.38, [0.1, -0.3, -0.83], 0x86f3d3, 0.14);
  orbit(2.38, 2.38, [0, 0.3, 0], 0x7b909e, 0.08);
  const inner = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.66, 1),
    new THREE.MeshBasicMaterial({
      color: 0x8beacc,
      wireframe: true,
      transparent: true,
      opacity: 0.045,
    }),
  );
  inner.rotation.z = 0.2;
  scene.add(inner);
  const dustPositions = [];
  for (let i = 0; i < 90; i++)
    dustPositions.push((random() - 0.5) * 10, (random() - 0.5) * 7.5, -1 - random() * 3);
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute('position', new THREE.Float32BufferAttribute(dustPositions, 3));
  scene.add(
    new THREE.Points(
      dustGeo,
      new THREE.PointsMaterial({ color: 0x6d9998, size: 0.012, transparent: true, opacity: 0.45 }),
    ),
  );
  const packetCount = mobile ? 10 : 18;
  const packetPositions = new Float32Array(packetCount * 3);
  const packetGeo = new THREE.BufferGeometry();
  packetGeo.setAttribute('position', new THREE.BufferAttribute(packetPositions, 3));
  const packets = new THREE.Points(
    packetGeo,
    new THREE.PointsMaterial({
      color: 0xb6ffe5,
      size: 0.045,
      transparent: true,
      opacity: 0.8,
      depthWrite: false,
    }),
  );
  globe.add(packets);
  const packetPaths = Array.from({ length: packetCount }, (_, i) => ({
    a: vectors[(i * 11) % count],
    b: vectors[(i * 11 + 8) % count],
    speed: 0.06 + random() * 0.05,
    offset: random(),
  }));
  const v = new THREE.Vector3();
  let pointerX = 0,
    pointerY = 0,
    frame = 0,
    inView = true,
    contextLost = false;
  let activeTime = 0,
    lastTime = performance.now();
  function resize() {
    const { width, height } = sceneElement.getBoundingClientRect();
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.position.z = mobile ? 8.9 : 8.5;
    camera.updateProjectionMatrix();
    if (paused) renderer.render(scene, camera);
  }
  new ResizeObserver(resize).observe(sceneElement);
  resize();
  sceneElement.addEventListener('pointermove', (e) => {
    if (e.pointerType === 'touch') return;
    const r = sceneElement.getBoundingClientRect();
    pointerX = ((e.clientX - r.left) / r.width - 0.5) * 0.22;
    pointerY = ((e.clientY - r.top) / r.height - 0.5) * 0.12;
  });
  sceneElement.addEventListener('pointerleave', () => {
    pointerX = 0;
    pointerY = 0;
  });
  document.querySelectorAll('[data-node]').forEach((link) => {
    const highlight = () => {
      edgeMaterial.opacity = 0.2;
    };
    const unhighlight = () => {
      edgeMaterial.opacity = 0.11;
    };
    link.addEventListener('pointerenter', highlight);
    link.addEventListener('focus', highlight);
    link.addEventListener('pointerleave', unhighlight);
    link.addEventListener('blur', unhighlight);
  });
  function draw(now) {
    frame = 0;
    if (!inView || document.hidden || contextLost) return;
    const delta = Math.min((now - lastTime) / 1000, 0.05);
    lastTime = now;
    if (!paused) {
      activeTime += delta;
      globe.rotation.y += delta * 0.035;
      globe.rotation.x += (0.18 + pointerY - globe.rotation.x) * 0.025;
      globe.rotation.z += (-0.16 + pointerX - globe.rotation.z) * 0.025;
      inner.rotation.y += delta * 0.14;
    }
    packetPaths.forEach((p, i) => {
      v.lerpVectors(p.a, p.b, (activeTime * p.speed + p.offset) % 1)
        .normalize()
        .multiplyScalar(2.16);
      packetPositions.set(v.toArray(), i * 3);
    });
    packetGeo.attributes.position.needsUpdate = true;
    renderer.render(scene, camera);
    if (!paused) frame = requestAnimationFrame(draw);
  }
  function resume() {
    if (!frame && inView && !document.hidden && !contextLost) {
      lastTime = performance.now();
      frame = requestAnimationFrame(draw);
    }
  }
  new IntersectionObserver(
    (entries) => {
      inView = entries[0].isIntersecting;
      if (inView) resume();
      else if (frame) {
        cancelAnimationFrame(frame);
        frame = 0;
      }
    },
    { threshold: 0 },
  ).observe(sceneElement);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    } else resume();
  });
  motionButton.addEventListener('click', resume);
  reducedMotion.addEventListener('change', resume);
  canvas.addEventListener('webglcontextlost', (e) => {
    e.preventDefault();
    contextLost = true;
    sceneElement.classList.remove('webgl-ready');
    if (frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  });
  canvas.addEventListener('webglcontextrestored', () => {
    contextLost = false;
    sceneElement.classList.add('webgl-ready');
    resume();
  });
  sceneElement.classList.add('webgl-ready');
  window.prototypeGraph = {
    renderer,
    scene,
    pause: () => {
      paused = true;
      updateMotionButton();
    },
    get running() {
      return !!frame;
    },
  };
  resume();
}
createKnowledgeGraph().catch((error) => {
  sceneElement.dataset.fallback = 'true';
  motionButton.hidden = true;
  console.info('知识网络使用静态展示：', error.message);
});
