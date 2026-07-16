import * as THREE from './vendor/three/three.module.min.js';

const container = document.querySelector('[data-loop-scene]');
const hero = container?.closest('.hero');

if (container && hero) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const palette = [0x155eef, 0x08a9c4, 0x0c9b68, 0x7055d9];
  let renderer;

  try {
    renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
    });
  } catch (error) {
    container.dataset.sceneState = 'fallback';
  }

  if (renderer) {
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.dataset.loopSceneCanvas = 'true';
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
    camera.position.set(0, 0, 10);

    const root = new THREE.Group();
    scene.add(root);

    const orbitMaterial = new THREE.MeshBasicMaterial({
      color: palette[0],
      transparent: true,
      opacity: 0.2,
      depthWrite: false,
    });
    const orbit = new THREE.Mesh(
      new THREE.TorusGeometry(4.2, 0.014, 8, 180),
      orbitMaterial,
    );
    orbit.scale.y = 0.54;
    orbit.rotation.set(0.08, 0.12, -0.04);
    root.add(orbit);

    const evidenceOrbit = new THREE.Mesh(
      new THREE.TorusGeometry(3.55, 0.009, 6, 160),
      new THREE.MeshBasicMaterial({
        color: palette[1],
        transparent: true,
        opacity: 0.14,
        depthWrite: false,
      }),
    );
    evidenceOrbit.scale.y = 0.48;
    evidenceOrbit.rotation.set(-0.06, -0.08, 0.2);
    root.add(evidenceOrbit);

    const plateGroup = new THREE.Group();
    plateGroup.position.set(-4.35, -0.12, 0.08);
    root.add(plateGroup);

    function makePlate(index) {
      const shape = new THREE.Shape();
      const points = [];
      for (let pointIndex = 0; pointIndex < 6; pointIndex += 1) {
        const angle = Math.PI / 6 + pointIndex * Math.PI / 3;
        points.push(new THREE.Vector2(Math.cos(angle) * 0.9, Math.sin(angle) * 0.54));
      }
      shape.moveTo(points[0].x, points[0].y);
      points.slice(1).forEach((point) => shape.lineTo(point.x, point.y));
      shape.closePath();

      const group = new THREE.Group();
      const fill = new THREE.Mesh(
        new THREE.ShapeGeometry(shape),
        new THREE.MeshBasicMaterial({
          color: palette[index],
          transparent: true,
          opacity: 0.055,
          side: THREE.DoubleSide,
          depthWrite: false,
        }),
      );
      group.add(fill);

      const outlinePoints = points.map((point) => new THREE.Vector3(point.x, point.y, 0.01));
      outlinePoints.push(outlinePoints[0].clone());
      const outline = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(outlinePoints),
        new THREE.LineBasicMaterial({
          color: palette[index],
          transparent: true,
          opacity: 0.34,
        }),
      );
      group.add(outline);

      const status = new THREE.Mesh(
        new THREE.RingGeometry(0.07, 0.105, 24),
        new THREE.MeshBasicMaterial({
          color: palette[index],
          transparent: true,
          opacity: 0.42,
          side: THREE.DoubleSide,
          depthWrite: false,
        }),
      );
      status.position.z = 0.02;
      group.add(status);

      group.position.set(index * 0.09, (index - 1.5) * 0.27, index * 0.055);
      return group;
    }

    for (let index = 0; index < 4; index += 1) {
      plateGroup.add(makePlate(index));
    }

    const gateGroup = new THREE.Group();
    gateGroup.position.set(4.35, -0.08, 0.1);
    root.add(gateGroup);

    const gatePlate = makePlate(2);
    gatePlate.scale.setScalar(0.9);
    gateGroup.add(gatePlate);

    [0.58, 0.42].forEach((radius, index) => {
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(radius, 0.012, 8, 96),
        new THREE.MeshBasicMaterial({
          color: index === 0 ? palette[2] : palette[1],
          transparent: true,
          opacity: index === 0 ? 0.28 : 0.2,
          depthWrite: false,
        }),
      );
      ring.scale.y = 0.72;
      ring.position.z = 0.08 + index * 0.02;
      gateGroup.add(ring);
    });

    const check = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(-0.22, 0.01, 0.13),
        new THREE.Vector3(-0.05, -0.16, 0.13),
        new THREE.Vector3(0.28, 0.2, 0.13),
      ]),
      new THREE.LineBasicMaterial({
        color: palette[2],
        transparent: true,
        opacity: 0.56,
      }),
    );
    gateGroup.add(check);

    const nodeGeometry = new THREE.SphereGeometry(0.075, 20, 14);
    const lifecycleNodes = palette.concat([palette[1], palette[0]]).map((color, index) => {
      const node = new THREE.Mesh(
        nodeGeometry,
        new THREE.MeshBasicMaterial({
          color,
          transparent: true,
          opacity: index === 5 ? 0.78 : 0.56,
          depthWrite: false,
        }),
      );
      root.add(node);
      return node;
    });

    function positionNodes(time) {
      lifecycleNodes.forEach((node, index) => {
        const angle = index / lifecycleNodes.length * Math.PI * 2 + time * 0.16;
        node.position.set(
          Math.cos(angle) * 4.15,
          Math.sin(angle) * 2.2,
          0.26 + Math.sin(angle * 2) * 0.12,
        );
        const pulse = index === 5 ? 1 + Math.sin(time * 1.4) * 0.16 : 1;
        node.scale.setScalar(pulse);
      });
    }

    let frameCount = 0;
    let animationFrame = 0;
    let visible = true;
    let targetRotationX = 0;
    let targetRotationY = 0;

    function render(time = 0) {
      const seconds = time * 0.001;
      positionNodes(seconds);
      root.rotation.x += (targetRotationX - root.rotation.x) * 0.045;
      root.rotation.y += (targetRotationY - root.rotation.y) * 0.045;
      root.rotation.z = Math.sin(seconds * 0.18) * 0.012;
      plateGroup.position.y = -0.12 + Math.sin(seconds * 0.42) * 0.045;
      gateGroup.rotation.z = Math.sin(seconds * 0.34) * 0.025;
      renderer.render(scene, camera);
      frameCount += 1;
      container.dataset.sceneFrames = String(frameCount);
      if (!container.dataset.sceneReady) {
        container.dataset.sceneReady = 'true';
      }
    }

    function animate(time) {
      animationFrame = 0;
      if (!visible || document.hidden || reducedMotion.matches) return;
      render(time);
      animationFrame = window.requestAnimationFrame(animate);
    }

    function startAnimation() {
      if (!animationFrame && visible && !document.hidden && !reducedMotion.matches) {
        animationFrame = window.requestAnimationFrame(animate);
      }
    }

    function stopAnimation() {
      if (animationFrame) {
        window.cancelAnimationFrame(animationFrame);
        animationFrame = 0;
      }
    }

    function resize() {
      const width = Math.max(container.clientWidth, 1);
      const height = Math.max(container.clientHeight, 1);
      const mobile = width < 640;
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.position.z = mobile ? 11.6 : 10;
      camera.updateProjectionMatrix();
      root.scale.setScalar(mobile ? 0.78 : 1);
      render(performance.now());
    }

    function updatePointer(event) {
      const bounds = hero.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width * 2 - 1;
      const y = (event.clientY - bounds.top) / bounds.height * 2 - 1;
      targetRotationY = x * 0.075;
      targetRotationX = -y * 0.04;
    }

    function resetPointer() {
      targetRotationX = 0;
      targetRotationY = 0;
    }

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(container);

    const visibilityObserver = new IntersectionObserver((entries) => {
      visible = entries[0]?.isIntersecting ?? true;
      if (visible) startAnimation();
      else stopAnimation();
    }, { threshold: 0.02 });
    visibilityObserver.observe(hero);

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stopAnimation();
      else startAnimation();
    });

    reducedMotion.addEventListener('change', () => {
      if (reducedMotion.matches) {
        stopAnimation();
        resetPointer();
        render(performance.now());
      } else {
        startAnimation();
      }
    });

    if (!reducedMotion.matches) {
      hero.addEventListener('pointermove', updatePointer, { passive: true });
      hero.addEventListener('pointerleave', resetPointer, { passive: true });
    }

    window.__loopSceneDiagnostics = () => {
      const gl = renderer.getContext();
      const width = renderer.domElement.width;
      const height = renderer.domElement.height;
      const pixels = new Uint8Array(width * height * 4);
      gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
      let sampled = 0;
      let painted = 0;
      for (let index = 3; index < pixels.length; index += 64) {
        sampled += 1;
        if (pixels[index] > 0) painted += 1;
      }
      return {
        frameCount,
        height,
        painted,
        paintedRatio: sampled ? painted / sampled : 0,
        reducedMotion: reducedMotion.matches,
        sampled,
        width,
      };
    };

    resize();
    startAnimation();
  }
}
