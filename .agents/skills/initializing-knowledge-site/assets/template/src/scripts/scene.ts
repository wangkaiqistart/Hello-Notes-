import type * as Three from 'three';

let release: (() => void) | undefined;
let generation = 0;
const reduced = matchMedia('(prefers-reduced-motion: reduce)');

async function mount() {
  release?.();
  release = undefined;
  const token = ++generation;
  const host = document.querySelector<HTMLElement>('.scene');
  const canvas = host?.querySelector('canvas');
  const control = document.querySelector<HTMLButtonElement>('#motion');
  if (!host || !canvas || !control) return;
  control.hidden = true;
  host.dataset.sceneState = 'fallback';
  if (reduced.matches) return;
  host.dataset.sceneState = 'loading';
  let THREE: typeof Three;
  try {
    THREE = await import('three');
  } catch {
    host.dataset.sceneState = 'fallback';
    return;
  }
  if (token !== generation || reduced.matches) return;
  let renderer: Three.WebGLRenderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
    });
  } catch {
    host.dataset.sceneState = 'fallback';
    return;
  }
  const compact = matchMedia('(max-width: 640px)').matches;
  renderer.setPixelRatio(Math.min(devicePixelRatio, compact ? 1 : 1.5));
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(5, 4.5, 7.5);
  camera.lookAt(0, 0, 0);
  const folio = new THREE.Group();
  folio.rotation.set(0.1, -0.3, 0);
  scene.add(folio);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x918575, 3));
  const light = new THREE.DirectionalLight(0xffffff, 4);
  light.position.set(-3, 8, 5);
  scene.add(light);
  const geometries: Three.BufferGeometry[] = [];
  const materials: Three.Material[] = [];
  function line(points: Three.Vector3[], color: number, opacity = 1) {
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    geometries.push(geometry);
    const material = new THREE.LineBasicMaterial({
      color,
      transparent: true,
      opacity,
    });
    materials.push(material);
    return new THREE.Line(geometry, material);
  }
  // A stack of technical index pages: each layer connects the same three concepts.
  for (let layer = 0; layer < 3; layer++) {
    const y = (layer - 1) * 0.78;
    const page = new THREE.Group();
    page.position.y = y;
    folio.add(page);
    const geometry = new THREE.BoxGeometry(3.2, 0.045, 2.2);
    geometries.push(geometry);
    const material = new THREE.MeshStandardMaterial({
      color: layer === 2 ? 0xfdfbf7 : 0xebe5da,
      roughness: 0.88,
    });
    materials.push(material);
    page.add(new THREE.Mesh(geometry, material));
    const edges = new THREE.EdgesGeometry(geometry);
    geometries.push(edges);
    const ink = new THREE.LineBasicMaterial({ color: 0x8b857b });
    materials.push(ink);
    page.add(new THREE.LineSegments(edges, ink));
    const nodes = [
      new THREE.Vector3(-0.95, 0.055, -0.48),
      new THREE.Vector3(0.85, 0.055, -0.28),
      new THREE.Vector3(0.2, 0.055, 0.65),
    ];
    page.add(line([...nodes, nodes[0]], 0x176b62, layer === 2 ? 1 : 0.5));
    for (const point of nodes) {
      const dot = new THREE.SphereGeometry(0.075, compact ? 8 : 16, 8);
      geometries.push(dot);
      const paint = new THREE.MeshStandardMaterial({
        color: 0x176b62,
        roughness: 0.8,
      });
      materials.push(paint);
      const mesh = new THREE.Mesh(dot, paint);
      mesh.position.copy(point);
      page.add(mesh);
    }
    // Notebook ruling: calm, meaningful linework rather than decorative particles.
    for (let row = 0; row < 3; row++)
      page.add(
        line(
          [
            new THREE.Vector3(-1.25, 0.03, 0.3 + row * 0.18),
            new THREE.Vector3(-0.5, 0.03, 0.3 + row * 0.18),
          ],
          0xb0a99d,
        ),
      );
  }
  for (const [x, z] of [
    [-0.95, -0.48],
    [0.85, -0.28],
    [0.2, 0.65],
  ]) {
    folio.add(
      line(
        [new THREE.Vector3(x, -0.78, z), new THREE.Vector3(x, 0.78, z)],
        0x176b62,
        0.7,
      ),
    );
  }
  let frame = 0,
    last = 0,
    visible = true,
    alive = true,
    lost = false,
    playing = false;
  let angle = 0,
    dragging = false,
    pointerX = 0;
  const start = performance.now();
  function render() {
    if (alive && !lost) renderer.render(scene, camera);
  }
  function loop(now: number) {
    frame = 0;
    if (!alive || !visible || document.hidden || lost) return;
    const entering = now - start < 700;
    const delta = Math.min((now - (last || now)) / 1000, 0.05);
    last = now;
    if (playing) angle += delta * 0.18;
    folio.rotation.y =
      angle - 0.3 + (entering ? (1 - (now - start) / 700) * 0.35 : 0);
    render();
    host!.dataset.sceneState = playing || entering ? 'running' : 'paused';
    if (playing || entering) frame = requestAnimationFrame(loop);
  }
  function reconcile() {
    cancelAnimationFrame(frame);
    frame = 0;
    last = 0;
    if (alive && !document.hidden && visible && !lost)
      frame = requestAnimationFrame(loop);
  }
  function resize() {
    const width = host!.clientWidth,
      height = host!.clientHeight;
    if (!width || !height) return;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
    render();
  }
  function toggle() {
    playing = !playing;
    control!.textContent = playing ? '暂停演示' : '播放演示';
    control!.setAttribute('aria-pressed', String(playing));
    reconcile();
  }
  function down(event: PointerEvent) {
    dragging = true;
    pointerX = event.clientX;
    canvas!.setPointerCapture(event.pointerId);
  }
  function move(event: PointerEvent) {
    if (dragging) {
      angle += (event.clientX - pointerX) * 0.008;
      pointerX = event.clientX;
      reconcile();
    }
  }
  function up() {
    dragging = false;
  }
  function contextLost(event: Event) {
    event.preventDefault();
    lost = true;
    cancelAnimationFrame(frame);
    host!.dataset.sceneState = 'fallback';
    control!.hidden = true;
  }
  function contextRestored() {
    lost = false;
    control!.hidden = false;
    resize();
    reconcile();
  }
  const sizeObserver = new ResizeObserver(resize);
  sizeObserver.observe(host);
  const visibility = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    reconcile();
  });
  visibility.observe(host);
  document.addEventListener('visibilitychange', reconcile);
  control.addEventListener('click', toggle);
  canvas.addEventListener('pointerdown', down);
  canvas.addEventListener('pointermove', move);
  canvas.addEventListener('pointerup', up);
  canvas.addEventListener('lostpointercapture', up);
  canvas.addEventListener('webglcontextlost', contextLost);
  canvas.addEventListener('webglcontextrestored', contextRestored);
  control.hidden = false;
  control.textContent = '播放演示';
  resize();
  reconcile();
  release = () => {
    alive = false;
    cancelAnimationFrame(frame);
    sizeObserver.disconnect();
    visibility.disconnect();
    document.removeEventListener('visibilitychange', reconcile);
    control.removeEventListener('click', toggle);
    canvas.removeEventListener('pointerdown', down);
    canvas.removeEventListener('pointermove', move);
    canvas.removeEventListener('pointerup', up);
    canvas.removeEventListener('lostpointercapture', up);
    canvas.removeEventListener('webglcontextlost', contextLost);
    canvas.removeEventListener('webglcontextrestored', contextRestored);
    for (const geometry of geometries) geometry.dispose();
    for (const material of materials) material.dispose();
    renderer.dispose();
    host.dataset.sceneState = 'fallback';
    control.hidden = true;
  };
}
let scheduled: ReturnType<typeof setTimeout>;
function schedule() {
  clearTimeout(scheduled);
  scheduled = setTimeout(() => void mount(), 80);
}
window.addEventListener('pagehide', () => {
  clearTimeout(scheduled);
  ++generation;
  release?.();
  release = undefined;
});
window.addEventListener('pageshow', (event) => {
  if (event.persisted) schedule();
});
reduced.addEventListener('change', () => void mount());
schedule();
