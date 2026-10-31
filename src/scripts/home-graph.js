import { iconMarkup as icon } from '../components/home/icon-markup';
import * as THREE from 'three';

/** @param {HTMLElement} sceneElement @param {HTMLButtonElement} motionButton */
export function initKnowledgeGraph(sceneElement, motionButton) {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reducedMotion.matches;
  function updateMotionButton() {
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.setAttribute('aria-label', paused ? '播放知识网络动画' : '暂停知识网络动画');
    motionButton.innerHTML = icon(paused ? 'play' : 'pause');
  }
  motionButton.disabled = false;
  updateMotionButton();
  motionButton.addEventListener('click', () => {
    paused = !paused;
    updateMotionButton();
  });
  reducedMotion.addEventListener('change', (e) => {
    paused = e.matches;
    updateMotionButton();
  });

  function createKnowledgeGraph() {
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
      vectors = [],
      brightness = [];
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
      const intensity = 0.25 + random() * 0.7;
      brightness.push(intensity);
      const color = (i % 4 === 0 ? violet : i % 3 === 0 ? blue : mint)
        .clone()
        .multiplyScalar(intensity);
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
        'varying vec3 vColor; void main(){float d=length(gl_PointCoord-.5);float a=(1.-smoothstep(.08,.5,d));gl_FragColor=vec4(vColor,a*.95);}',
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
    const rings = [];
    rings.push(orbit(2.82, 1.2, [0.15, 0.25, 0.43], 0x91a6c9, 0.18));
    rings.push(orbit(2.65, 1.38, [0.1, -0.3, -0.83], 0x86f3d3, 0.14));
    rings.push(orbit(2.38, 2.38, [0, 0.3, 0], 0x7b909e, 0.08));
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
    const dust = new THREE.Points(
      dustGeo,
      new THREE.PointsMaterial({
        color: 0x6d9998,
        size: 0.012,
        transparent: true,
        opacity: 0.45,
      }),
    );
    scene.add(dust);
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
      camera.position.z = matchMedia('(max-width: 520px)').matches ? 8.9 : 8.5;
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
    let light = false;
    function updateTheme() {
      light = document.documentElement.dataset.theme === 'light';
      mint.set(light ? 0x087457 : 0x86f3d3);
      violet.set(light ? 0x7151af : 0x9586dc);
      blue.set(light ? 0x296eaa : 0x73a6d9);
      for (let i = 0; i < count; i++) {
        const color = (i % 4 === 0 ? violet : i % 3 === 0 ? blue : mint).clone();
        // Pale backgrounds need darker ink instead of dimmed luminous points.
        if (!light) color.multiplyScalar(brightness[i]);
        geo.attributes.color.setXYZ(i, color.r, color.g, color.b);
      }
      geo.attributes.color.needsUpdate = true;
      edgeMaterial.color.set(light ? 0x296e59 : 0x6aaca9);
      edgeMaterial.opacity = light ? 0.24 : 0.11;
      rings.forEach((ring, i) => {
        ring.material.color.set(
          light ? [0x506b91, 0x087457, 0x566f63][i] : [0x91a6c9, 0x86f3d3, 0x7b909e][i],
        );
        ring.material.opacity = light ? [0.25, 0.24, 0.13][i] : [0.18, 0.14, 0.08][i];
      });
      inner.material.color.set(light ? 0x087457 : 0x8beacc);
      inner.material.opacity = light ? 0.09 : 0.045;
      dust.material.color.set(light ? 0x52776a : 0x6d9998);
      packets.material.color.set(light ? 0x087457 : 0xb6ffe5);
      resume();
    }
    new MutationObserver(updateTheme).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });
    updateTheme();
    document.querySelectorAll('[data-node]').forEach((link) => {
      const highlight = () => {
        edgeMaterial.opacity = light ? 0.4 : 0.2;
        resume();
      };
      const unhighlight = () => {
        edgeMaterial.opacity = light ? 0.24 : 0.11;
        resume();
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
        v.toArray(packetPositions, i * 3);
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
    resume();
  }
  try {
    createKnowledgeGraph();
  } catch {
    sceneElement.dataset.fallback = 'true';
    motionButton.hidden = true;
  }
}
