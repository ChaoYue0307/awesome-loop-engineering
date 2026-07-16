import * as THREE from './vendor/three/three.module.min.js';

const container = document.querySelector('[data-loop-scene]');
const hero = container?.closest('.hero');
const stageButtons = Array.from(document.querySelectorAll('[data-loop-stage]'));
const stageDetail = document.getElementById('loop-stage-detail');
const stageCopy = [
  ['Intake:', 'capture work from queues, schedules, events, or goals.'],
  ['Delegate:', 'route bounded work to the right agent role.'],
  ['Act:', 'work inside an isolated environment with scoped tools.'],
  ['Verify:', 'gate completion with tests, evals, traces, or review.'],
  ['Persist:', 'record state, evidence, and receipts outside the model.'],
  ['Decide:', 'retry with evidence, escalate, or exit when the goal is met.'],
];
let activeStage = 3;
const stageSubscribers = [];

function renderStageCopy(index) {
  if (!stageDetail) return;
  const strong = document.createElement('strong');
  strong.textContent = stageCopy[index][0];
  stageDetail.replaceChildren(strong, document.createTextNode(` ${stageCopy[index][1]}`));
}

function selectStage(index, moveFocus = false) {
  activeStage = Math.max(0, Math.min(stageCopy.length - 1, index));
  stageButtons.forEach((button, buttonIndex) => {
    button.setAttribute('aria-pressed', buttonIndex === activeStage ? 'true' : 'false');
  });
  renderStageCopy(activeStage);
  stageSubscribers.forEach((subscriber) => subscriber(activeStage));
  if (moveFocus) stageButtons[activeStage]?.focus();
}

stageButtons.forEach((button, index) => {
  button.addEventListener('click', () => selectStage(index));
  button.addEventListener('focus', () => selectStage(index));
  button.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'Home') selectStage(0, true);
    else if (event.key === 'End') selectStage(stageButtons.length - 1, true);
    else {
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      selectStage((index + direction + stageButtons.length) % stageButtons.length, true);
    }
  });
});

renderStageCopy(activeStage);

if (container && hero) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const lowPower = Number(navigator.hardwareConcurrency || 8) <= 4;
  const palette = [0x155eef, 0x08a9c4, 0x0c9b68, 0x7055d9, 0x08a9c4, 0x155eef];
  const white = new THREE.Color(0xffffff);
  let renderer;

  try {
    renderer = new THREE.WebGLRenderer({
      alpha: false,
      antialias: !lowPower,
      preserveDrawingBuffer: true,
      powerPreference: 'high-performance',
    });
  } catch (error) {
    container.dataset.sceneState = 'fallback';
  }

  if (renderer) {
    renderer.setClearColor(0xf7f9fc, 1);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.dataset.loopSceneCanvas = 'true';
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(31, 1, 0.1, 60);
    camera.position.set(0, 0.25, 12.2);

    scene.add(new THREE.HemisphereLight(0xffffff, 0xdbe8ff, 2.4));
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.8);
    keyLight.position.set(-3.5, 5, 8);
    scene.add(keyLight);
    const accentLight = new THREE.PointLight(0x08a9c4, 11, 12, 2);
    accentLight.position.set(2.4, -0.8, 3.8);
    scene.add(accentLight);

    const root = new THREE.Group();
    root.position.set(0, -0.28, 0);
    scene.add(root);

    const stagePositions = [
      new THREE.Vector3(-4.15, -0.08, 0.08),
      new THREE.Vector3(-2.45, 1.2, -0.22),
      new THREE.Vector3(0, 1.56, 0.12),
      new THREE.Vector3(2.45, 1.2, -0.16),
      new THREE.Vector3(4.15, -0.08, 0.1),
      new THREE.Vector3(0, -1.48, 0.32),
    ];
    const flowCurve = new THREE.CatmullRomCurve3(stagePositions, true, 'centripetal', 0.42);
    const flowMaterial = new THREE.MeshBasicMaterial({
      color: 0x155eef,
      transparent: true,
      opacity: 0.28,
      depthWrite: false,
    });
    const flow = new THREE.Mesh(
      new THREE.TubeGeometry(flowCurve, lowPower ? 120 : 200, 0.018, 6, true),
      flowMaterial,
    );
    root.add(flow);

    const flowAura = new THREE.Mesh(
      new THREE.TubeGeometry(flowCurve, lowPower ? 96 : 160, 0.058, 6, true),
      new THREE.MeshBasicMaterial({
        color: 0x08a9c4,
        transparent: true,
        opacity: 0.05,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      }),
    );
    root.add(flowAura);

    function closestCurveTime(position) {
      let closestTime = 0;
      let closestDistance = Infinity;
      for (let sample = 0; sample <= 240; sample += 1) {
        const time = sample / 240;
        const distance = flowCurve.getPointAt(time).distanceToSquared(position);
        if (distance < closestDistance) {
          closestDistance = distance;
          closestTime = time;
        }
      }
      return closestTime;
    }

    const stageTimes = stagePositions.map(closestCurveTime);
    const diskGeometry = new THREE.CylinderGeometry(0.46, 0.46, 0.13, lowPower ? 24 : 48);
    const rimGeometry = new THREE.TorusGeometry(0.49, 0.026, 8, lowPower ? 36 : 64);
    const haloGeometry = new THREE.TorusGeometry(0.61, 0.012, 8, lowPower ? 40 : 72);
    const markerGeometry = new THREE.SphereGeometry(0.085, lowPower ? 16 : 24, lowPower ? 10 : 16);

    const lifecycleNodes = stagePositions.map((position, index) => {
      const color = new THREE.Color(palette[index]);
      const group = new THREE.Group();
      const diskMaterial = new THREE.MeshStandardMaterial({
        color: color.clone().lerp(white, 0.7),
        emissive: color,
        emissiveIntensity: 0.05,
        metalness: 0.08,
        roughness: 0.4,
        transparent: true,
        opacity: 0.96,
      });
      const disk = new THREE.Mesh(diskGeometry, diskMaterial);
      disk.rotation.x = Math.PI / 2;
      group.add(disk);

      const rimMaterial = new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.82,
        depthWrite: false,
      });
      const rim = new THREE.Mesh(rimGeometry, rimMaterial);
      rim.position.z = 0.08;
      group.add(rim);

      const haloMaterial = new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.08,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
      const halo = new THREE.Mesh(haloGeometry, haloMaterial);
      halo.position.z = 0.1;
      group.add(halo);

      const marker = new THREE.Mesh(
        markerGeometry,
        new THREE.MeshStandardMaterial({
          color,
          emissive: color,
          emissiveIntensity: 0.5,
          metalness: 0.12,
          roughness: 0.28,
        }),
      );
      marker.position.z = 0.16;
      group.add(marker);

      group.position.copy(position);
      group.userData = { diskMaterial, haloMaterial, rimMaterial };
      root.add(group);
      return group;
    });

    const directionAxis = new THREE.Vector3(0, 1, 0);
    stageTimes.forEach((stageTime, index) => {
      const time = (stageTime - 0.045 + 1) % 1;
      const tangent = flowCurve.getTangentAt(time).normalize();
      const arrow = new THREE.Mesh(
        new THREE.ConeGeometry(0.075, 0.24, lowPower ? 12 : 18),
        new THREE.MeshBasicMaterial({
          color: palette[index],
          transparent: true,
          opacity: 0.58,
          depthWrite: false,
        }),
      );
      arrow.position.copy(flowCurve.getPointAt(time));
      arrow.quaternion.setFromUnitVectors(directionAxis, tangent);
      root.add(arrow);
    });

    const stackGroup = new THREE.Group();
    stackGroup.position.set(0, -0.06, -0.32);
    root.add(stackGroup);
    palette.slice(0, 4).forEach((hex, index) => {
      const color = new THREE.Color(hex);
      const plate = new THREE.Mesh(
        new THREE.CylinderGeometry(0.92, 0.92, 0.075, 6),
        new THREE.MeshStandardMaterial({
          color: color.clone().lerp(white, 0.68),
          emissive: color,
          emissiveIntensity: 0.04,
          metalness: 0.08,
          roughness: 0.44,
          transparent: true,
          opacity: 0.9,
        }),
      );
      plate.rotation.x = Math.PI / 2;
      plate.scale.z = 0.68;
      plate.position.set(index * 0.035 - 0.052, index * 0.055 - 0.08, index * 0.105);
      stackGroup.add(plate);
    });

    const coreMaterial = new THREE.MeshStandardMaterial({
      color: 0xf2fbff,
      emissive: 0x08a9c4,
      emissiveIntensity: 0.22,
      metalness: 0.18,
      roughness: 0.24,
    });
    const core = new THREE.Mesh(new THREE.IcosahedronGeometry(0.45, 1), coreMaterial);
    core.position.set(0, 0.03, 0.62);
    stackGroup.add(core);

    const coreShell = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.62, 1),
      new THREE.MeshBasicMaterial({
        color: 0x155eef,
        wireframe: true,
        transparent: true,
        opacity: 0.23,
        depthWrite: false,
      }),
    );
    coreShell.position.copy(core.position);
    stackGroup.add(coreShell);

    const coreRings = [0.72, 0.86].map((radius, index) => {
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(radius, 0.012, 8, lowPower ? 48 : 80),
        new THREE.MeshBasicMaterial({
          color: index === 0 ? 0x08a9c4 : 0x7055d9,
          transparent: true,
          opacity: index === 0 ? 0.27 : 0.18,
          depthWrite: false,
        }),
      );
      ring.position.copy(core.position);
      ring.rotation.set(index ? 0.76 : -0.62, index ? 0.28 : -0.2, index ? 0.18 : -0.12);
      stackGroup.add(ring);
      return ring;
    });

    const beamGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, 0.52),
      stagePositions[activeStage],
    ]);
    const focusBeam = new THREE.Line(
      beamGeometry,
      new THREE.LineDashedMaterial({
        color: palette[activeStage],
        transparent: true,
        opacity: 0.28,
        dashSize: 0.12,
        gapSize: 0.09,
        depthWrite: false,
      }),
    );
    focusBeam.computeLineDistances();
    root.add(focusBeam);

    function updateFocusBeam(index) {
      const positions = focusBeam.geometry.attributes.position;
      positions.setXYZ(0, 0, 0, 0.52);
      positions.setXYZ(1, stagePositions[index].x, stagePositions[index].y, stagePositions[index].z);
      positions.needsUpdate = true;
      focusBeam.material.color.setHex(palette[index]);
      focusBeam.computeLineDistances();
    }

    stageSubscribers.push((index) => {
      updateFocusBeam(index);
      render(performance.now());
    });

    const pulseMaterial = new THREE.MeshBasicMaterial({
      color: 0x155eef,
      transparent: true,
      opacity: 0.94,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const evidencePulse = new THREE.Mesh(
      new THREE.SphereGeometry(0.105, lowPower ? 16 : 24, lowPower ? 10 : 16),
      pulseMaterial,
    );
    root.add(evidencePulse);

    const trail = [];
    if (!lowPower) {
      for (let index = 0; index < 6; index += 1) {
        const material = pulseMaterial.clone();
        material.opacity = 0.28 * (1 - index / 7);
        const point = new THREE.Mesh(new THREE.SphereGeometry(0.05 - index * 0.004, 12, 8), material);
        trail.push(point);
        root.add(point);
      }
    }

    let frameCount = 0;
    let animationFrame = 0;
    let visible = true;
    let targetRotationX = 0;
    let targetRotationY = 0;
    let layoutScaleX = 1;
    let layoutScaleY = 1;

    function circularDistance(left, right) {
      const distance = Math.abs(left - right);
      return Math.min(distance, 1 - distance);
    }

    function render(time = 0) {
      const seconds = time * 0.001;
      const progress = reducedMotion.matches ? stageTimes[activeStage] : (seconds * 0.058) % 1;
      evidencePulse.position.copy(flowCurve.getPointAt(progress));
      trail.forEach((point, index) => {
        const trailTime = (progress - (index + 1) * 0.012 + 1) % 1;
        point.position.copy(flowCurve.getPointAt(trailTime));
      });

      lifecycleNodes.forEach((node, index) => {
        const selected = index === activeStage;
        const flowPulse = Math.max(0, 1 - circularDistance(progress, stageTimes[index]) / 0.055);
        const scale = 1 + (selected ? 0.12 : 0) + flowPulse * 0.1;
        node.scale.setScalar(scale);
        node.userData.diskMaterial.emissiveIntensity = selected ? 0.21 : 0.05 + flowPulse * 0.12;
        node.userData.rimMaterial.opacity = selected ? 0.96 : 0.58 + flowPulse * 0.22;
        node.userData.haloMaterial.opacity = selected ? 0.34 : 0.06 + flowPulse * 0.18;
      });

      const corePulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 1.2) * 0.035;
      core.scale.setScalar(corePulse);
      core.rotation.y = seconds * 0.22;
      core.rotation.x = seconds * 0.13;
      coreShell.rotation.y = -seconds * 0.12;
      coreShell.rotation.x = seconds * 0.09;
      coreRings[0].rotation.z = -0.12 + seconds * 0.08;
      coreRings[1].rotation.z = 0.18 - seconds * 0.065;

      root.rotation.x += (targetRotationX - root.rotation.x) * 0.045;
      root.rotation.y += (targetRotationY - root.rotation.y) * 0.045;
      root.rotation.z = reducedMotion.matches ? 0 : Math.sin(seconds * 0.16) * 0.008;
      root.scale.x = layoutScaleX;
      root.scale.y = layoutScaleY;
      renderer.render(scene, camera);
      frameCount += 1;
      container.dataset.sceneFrames = String(frameCount);
      container.dataset.sceneReady = 'true';
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
      if (!animationFrame) return;
      window.cancelAnimationFrame(animationFrame);
      animationFrame = 0;
    }

    function resize() {
      const width = Math.max(container.clientWidth, 1);
      const height = Math.max(container.clientHeight, 1);
      const mobile = window.innerWidth < 640;
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile || lowPower ? 1.25 : 1.6));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.fov = mobile ? 35 : 31;
      camera.position.z = mobile ? 12.9 : 12.2;
      camera.updateProjectionMatrix();
      layoutScaleX = mobile ? 1.04 : 1.58;
      layoutScaleY = mobile ? 0.96 : 1.04;
      root.position.y = mobile ? -0.14 : -0.28;
      render(performance.now());
    }

    function updatePointer(event) {
      const bounds = hero.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width * 2 - 1;
      const y = (event.clientY - bounds.top) / bounds.height * 2 - 1;
      targetRotationY = x * 0.055;
      targetRotationX = -y * 0.025;
    }

    function resetPointer() {
      targetRotationX = 0;
      targetRotationY = 0;
    }

    if ('ResizeObserver' in window) {
      const resizeObserver = new ResizeObserver(resize);
      resizeObserver.observe(container);
    } else {
      window.addEventListener('resize', resize, { passive: true });
    }

    if ('IntersectionObserver' in window) {
      const visibilityObserver = new IntersectionObserver((entries) => {
        visible = entries[0]?.isIntersecting ?? true;
        if (visible) startAnimation();
        else stopAnimation();
      }, { threshold: 0.02 });
      visibilityObserver.observe(hero);
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stopAnimation();
      else startAnimation();
    });

    const handleMotionChange = () => {
      if (reducedMotion.matches) {
        stopAnimation();
        resetPointer();
        render(performance.now());
      } else {
        startAnimation();
      }
    };
    if (reducedMotion.addEventListener) reducedMotion.addEventListener('change', handleMotionChange);
    else reducedMotion.addListener(handleMotionChange);

    if (!reducedMotion.matches) {
      hero.addEventListener('pointermove', updatePointer, { passive: true });
      hero.addEventListener('pointerleave', resetPointer, { passive: true });
    }

    renderer.domElement.addEventListener('webglcontextlost', (event) => {
      event.preventDefault();
      stopAnimation();
      container.dataset.sceneState = 'fallback';
    });

    window.__loopSceneDiagnostics = () => {
      const gl = renderer.getContext();
      const width = renderer.domElement.width;
      const height = renderer.domElement.height;
      const pixels = new Uint8Array(width * height * 4);
      gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
      let sampled = 0;
      let painted = 0;
      let minimumLuminance = 255;
      let maximumLuminance = 0;
      for (let index = 0; index < pixels.length; index += 64) {
        const red = pixels[index];
        const green = pixels[index + 1];
        const blue = pixels[index + 2];
        const distanceFromPaper = Math.abs(red - 247) + Math.abs(green - 249) + Math.abs(blue - 252);
        const luminance = red * 0.2126 + green * 0.7152 + blue * 0.0722;
        sampled += 1;
        if (distanceFromPaper > 24) painted += 1;
        minimumLuminance = Math.min(minimumLuminance, luminance);
        maximumLuminance = Math.max(maximumLuminance, luminance);
      }
      return {
        activeStage,
        drawCalls: renderer.info.render.calls,
        frameCount,
        height,
        luminanceRange: maximumLuminance - minimumLuminance,
        lowPower,
        painted,
        paintedRatio: sampled ? painted / sampled : 0,
        reducedMotion: reducedMotion.matches,
        sampled,
        triangles: renderer.info.render.triangles,
        width,
      };
    };

    window.__loopScenePause = () => {
      stopAnimation();
      render(performance.now());
      return window.__loopSceneDiagnostics();
    };
    window.__loopSceneResume = () => {
      startAnimation();
      return true;
    };

    resize();
    updateFocusBeam(activeStage);
    startAnimation();
  }
}
