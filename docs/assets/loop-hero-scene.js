import * as THREE from './vendor/three/three.module.min.js';

const container = document.querySelector('[data-loop-scene]');
const hero = container?.closest('.hero');
const stageButtons = Array.from(document.querySelectorAll('[data-loop-stage]'));
const stageDetail = document.getElementById('loop-stage-detail');
const stages = [
  ['Intake:', 'capture a bounded work packet from a queue, schedule, event, or goal.'],
  ['Delegate:', 'route that packet to the right agent role while keeping scope explicit.'],
  ['Act:', 'execute inside an isolated workspace with scoped tools and permissions.'],
  ['Verify:', 'turn output into evidence through tests, evals, traces, or review.'],
  ['Persist:', 'write progress, receipts, and durable state outside the model.'],
  ['Decide:', 'choose one bounded outcome: retry with evidence, escalate, or exit.'],
];
let activeStage = 0;
let manualSelectionUntil = 0;
const stageSubscribers = [];

function renderStageCopy(index) {
  if (!stageDetail) return;
  const strong = document.createElement('strong');
  strong.textContent = stages[index][0];
  stageDetail.replaceChildren(strong, document.createTextNode(` ${stages[index][1]}`));
}

function selectStage(index, moveFocus = false, userInitiated = false) {
  activeStage = Math.max(0, Math.min(stages.length - 1, index));
  if (userInitiated) manualSelectionUntil = performance.now() + 8000;
  stageButtons.forEach((button, buttonIndex) => {
    button.setAttribute('aria-pressed', buttonIndex === activeStage ? 'true' : 'false');
  });
  renderStageCopy(activeStage);
  stageSubscribers.forEach((subscriber) => subscriber(activeStage));
  if (moveFocus) stageButtons[activeStage]?.focus();
}

stageButtons.forEach((button, index) => {
  button.addEventListener('click', () => selectStage(index, false, true));
  button.addEventListener('focus', () => selectStage(index, false, true));
  button.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    if (event.key === 'Home') selectStage(0, true, true);
    else if (event.key === 'End') selectStage(stageButtons.length - 1, true, true);
    else {
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      selectStage((index + direction + stageButtons.length) % stageButtons.length, true, true);
    }
  });
});

selectStage(activeStage);

if (container && hero) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const lowPower = Number(navigator.hardwareConcurrency || 8) <= 4;
  const palette = [0x1457ff, 0x009ac2, 0x07866f, 0x12a66a, 0x2868df, 0x7657e8];
  const paper = new THREE.Color(0xf7f9fc);
  const white = new THREE.Color(0xffffff);
  const yAxis = new THREE.Vector3(0, 1, 0);
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
    renderer.setClearColor(paper, 1);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.dataset.loopSceneCanvas = 'true';
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(29, 1, 0.1, 60);
    scene.add(new THREE.HemisphereLight(0xffffff, 0xb9cbe4, 2.15));

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.8);
    keyLight.position.set(-4, 6, 8);
    scene.add(keyLight);

    const cyanLight = new THREE.PointLight(0x08a9c4, 13, 14, 2);
    cyanLight.position.set(-1.5, 1.2, 4.5);
    scene.add(cyanLight);

    const greenLight = new THREE.PointLight(0x16a36a, 8, 10, 2);
    greenLight.position.set(2.3, 0.8, 3.6);
    scene.add(greenLight);

    const root = new THREE.Group();
    scene.add(root);

    function standardMaterial(hex, lighten = 0.5, options = {}) {
      const color = new THREE.Color(hex);
      const blend = Math.min(lighten, 0.58);
      return new THREE.MeshStandardMaterial({
        color: color.clone().lerp(white, blend),
        emissive: color,
        emissiveIntensity: options.emissiveIntensity ?? 0.08,
        metalness: options.metalness ?? 0.12,
        roughness: options.roughness ?? 0.34,
        transparent: options.transparent ?? false,
        opacity: options.opacity ?? 1,
        depthWrite: options.depthWrite ?? true,
      });
    }

    function basicMaterial(hex, opacity = 1) {
      return new THREE.MeshBasicMaterial({
        color: hex,
        transparent: opacity < 1,
        opacity,
        depthWrite: opacity >= 1,
      });
    }

    function cylinderBetween(start, end, radius, material, segments = 12) {
      const direction = end.clone().sub(start);
      const cylinder = new THREE.Mesh(
        new THREE.CylinderGeometry(radius, radius, direction.length(), segments),
        material,
      );
      cylinder.position.copy(start).add(end).multiplyScalar(0.5);
      cylinder.quaternion.setFromUnitVectors(yAxis, direction.normalize());
      return cylinder;
    }

    function addTube(curve, radius, hex, opacity, segments = 120) {
      const tube = new THREE.Mesh(
        new THREE.TubeGeometry(curve, lowPower ? Math.round(segments * 0.65) : segments, radius, 6, false),
        new THREE.MeshBasicMaterial({
          color: hex,
          transparent: true,
          opacity,
          blending: opacity < 0.16 ? THREE.AdditiveBlending : THREE.NormalBlending,
          depthWrite: false,
        }),
      );
      root.add(tube);
      return tube;
    }

    function addArrow(curve, time, hex, scale = 1) {
      const tangent = curve.getTangentAt(time).normalize();
      const arrow = new THREE.Mesh(
        new THREE.ConeGeometry(0.06 * scale, 0.2 * scale, lowPower ? 10 : 16),
        basicMaterial(hex, 0.78),
      );
      arrow.position.copy(curve.getPointAt(time));
      arrow.quaternion.setFromUnitVectors(yAxis, tangent);
      root.add(arrow);
      return arrow;
    }

    function positionArrow(arrow, curve, time) {
      const tangent = curve.getTangentAt(time).normalize();
      arrow.position.copy(curve.getPointAt(time));
      arrow.quaternion.setFromUnitVectors(yAxis, tangent);
    }

    function replaceTubeGeometry(mesh, curve, radius, segments) {
      mesh.geometry.dispose();
      mesh.geometry = new THREE.TubeGeometry(
        curve,
        lowPower ? Math.round(segments * 0.65) : segments,
        radius,
        6,
        false,
      );
    }

    function roundedRect(context, x, y, width, height, radius) {
      context.beginPath();
      context.moveTo(x + radius, y);
      context.lineTo(x + width - radius, y);
      context.quadraticCurveTo(x + width, y, x + width, y + radius);
      context.lineTo(x + width, y + height - radius);
      context.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
      context.lineTo(x + radius, y + height);
      context.quadraticCurveTo(x, y + height, x, y + height - radius);
      context.lineTo(x, y + radius);
      context.quadraticCurveTo(x, y, x + radius, y);
      context.closePath();
    }

    function labelSprite(text, hex) {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 104;
      const context = canvas.getContext('2d');
      const cssColor = `#${hex.toString(16).padStart(6, '0')}`;
      context.clearRect(0, 0, canvas.width, canvas.height);
      roundedRect(context, 4, 4, 504, 96, 18);
      context.fillStyle = 'rgba(247, 249, 252, 0.95)';
      context.fill();
      context.lineWidth = 4;
      context.strokeStyle = cssColor;
      context.stroke();
      context.fillStyle = '#111827';
      context.font = '700 32px IBM Plex Mono, ui-monospace, monospace';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.fillText(text, 256, 53);

      const texture = new THREE.CanvasTexture(canvas);
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.minFilter = THREE.LinearFilter;
      const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }));
      sprite.scale.set(1.48, 0.32, 1);
      sprite.renderOrder = 20;
      return sprite;
    }

    function numberSprite(number, hex) {
      const canvas = document.createElement('canvas');
      canvas.width = 128;
      canvas.height = 128;
      const context = canvas.getContext('2d');
      const cssColor = `#${hex.toString(16).padStart(6, '0')}`;
      context.beginPath();
      context.arc(64, 64, 54, 0, Math.PI * 2);
      context.fillStyle = 'rgba(255, 255, 255, 0.98)';
      context.fill();
      context.lineWidth = 7;
      context.strokeStyle = cssColor;
      context.stroke();
      context.fillStyle = '#111827';
      context.font = '700 46px IBM Plex Mono, ui-monospace, monospace';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.fillText(String(number).padStart(2, '0'), 64, 67);

      const texture = new THREE.CanvasTexture(canvas);
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.minFilter = THREE.LinearFilter;
      const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }));
      sprite.scale.set(0.42, 0.42, 1);
      sprite.renderOrder = 21;
      return sprite;
    }

    const desktopStagePositions = [
      new THREE.Vector3(-4.35, -0.06, 0.22),
      new THREE.Vector3(-2.62, 0.08, 0.04),
      new THREE.Vector3(-0.86, -0.03, 0.18),
      new THREE.Vector3(0.94, 0.08, 0.02),
      new THREE.Vector3(2.62, -0.02, 0.16),
      new THREE.Vector3(4.12, 0.07, 0.02),
    ];
    const compactStagePositions = [
      new THREE.Vector3(-2.7, 0.78, 0.2),
      new THREE.Vector3(-0.92, 0.78, 0.04),
      new THREE.Vector3(0.88, 0.78, 0.18),
      new THREE.Vector3(2.65, 0.78, 0.02),
      new THREE.Vector3(1.52, -0.74, 0.16),
      new THREE.Vector3(-0.18, -0.74, 0.02),
    ];
    const stagePositions = desktopStagePositions.map((position) => position.clone());
    let mainCurve = new THREE.CatmullRomCurve3(stagePositions, false, 'centripetal', 0.35);
    const mainTube = addTube(mainCurve, 0.032, 0x1457ff, 0.82, 180);
    const mainGlow = addTube(mainCurve, 0.095, 0x009ac2, 0.1, 150);
    const mainArrowTimes = [0.11, 0.29, 0.47, 0.65, 0.84];
    const mainArrows = mainArrowTimes.map((time, index) => (
      addArrow(mainCurve, time, palette[Math.min(index + 1, palette.length - 1)], 1.02)
    ));

    function closestCurveTime(position) {
      let closestTime = 0;
      let closestDistance = Infinity;
      for (let sample = 0; sample <= 240; sample += 1) {
        const time = sample / 240;
        const distance = mainCurve.getPointAt(time).distanceToSquared(position);
        if (distance < closestDistance) {
          closestDistance = distance;
          closestTime = time;
        }
      }
      return closestTime;
    }

    let stageTimes = stagePositions.map(closestCurveTime);
    let retryCurve = new THREE.CatmullRomCurve3([
      stagePositions[5],
      new THREE.Vector3(3.7, 1.48, -0.55),
      new THREE.Vector3(0.1, 1.88, -0.82),
      new THREE.Vector3(-3.85, 1.4, -0.52),
      stagePositions[0],
    ], false, 'centripetal', 0.45);
    const retryLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(retryCurve.getPoints(lowPower ? 90 : 160)),
      new THREE.LineDashedMaterial({
        color: 0x7c5ce0,
        transparent: true,
        opacity: 0.6,
        dashSize: 0.14,
        gapSize: 0.1,
        depthWrite: false,
      }),
    );
    retryLine.computeLineDistances();
    root.add(retryLine);
    const retryArrowTimes = [0.24, 0.5, 0.76];
    const retryArrows = retryArrowTimes.map((time) => addArrow(retryCurve, time, 0x7657e8, 0.94));

    const exitTarget = new THREE.Vector3(5.35, 0.75, 0.08);
    const escalateTarget = new THREE.Vector3(5.35, -0.72, 0.12);
    let exitCurve = new THREE.CatmullRomCurve3([
      stagePositions[5],
      new THREE.Vector3(4.72, 0.3, 0.04),
      exitTarget,
    ], false, 'centripetal', 0.35);
    let escalateCurve = new THREE.CatmullRomCurve3([
      stagePositions[5],
      new THREE.Vector3(4.7, -0.28, 0.06),
      escalateTarget,
    ], false, 'centripetal', 0.35);
    const exitTube = addTube(exitCurve, 0.022, 0x16a36a, 0.82, 60);
    const escalateTube = addTube(escalateCurve, 0.022, 0xd97706, 0.76, 60);
    const exitArrow = addArrow(exitCurve, 0.68, 0x16a36a, 0.9);
    const escalateArrow = addArrow(escalateCurve, 0.68, 0xd97706, 0.9);

    const stationStates = [];
    const labels = [];
    const numberLabels = [];

    function createStation(index, name) {
      const color = palette[index];
      const group = new THREE.Group();
      group.position.copy(stagePositions[index]);
      root.add(group);

      const haloMaterial = new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.12,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
      const halo = new THREE.Mesh(
        new THREE.TorusGeometry(0.67, 0.025, 8, lowPower ? 32 : 56),
        haloMaterial,
      );
      halo.rotation.x = Math.PI / 2;
      halo.position.y = -0.42;
      group.add(halo);

      const baseMaterial = standardMaterial(color, 0.56, { emissiveIntensity: 0.05, roughness: 0.46 });
      const base = new THREE.Mesh(
        new THREE.CylinderGeometry(0.55, 0.61, 0.09, lowPower ? 20 : 36),
        baseMaterial,
      );
      base.position.y = -0.39;
      group.add(base);

      const label = labelSprite(`${String(index + 1).padStart(2, '0')}  ${name.toUpperCase()}`, color);
      label.position.set(0, 1.22, 0.12);
      group.add(label);
      labels.push(label);

      const numberLabel = numberSprite(index + 1, color);
      numberLabel.position.set(0.4, 0.84, 0.38);
      group.add(numberLabel);
      numberLabels.push(numberLabel);

      const state = { group, haloMaterial, baseMaterial, materials: [], label, numberLabel };
      stationStates.push(state);
      return state;
    }

    function track(state, material) {
      state.materials.push(material);
      return material;
    }

    const intake = createStation(0, 'Intake');
    const intakeMaterial = track(intake, standardMaterial(palette[0], 0.58));
    const intakeTray = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.1, 0.62), intakeMaterial);
    intakeTray.position.y = -0.08;
    intake.group.add(intakeTray);
    [-0.38, 0.38].forEach((x) => {
      const wall = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.38, 0.62), intakeMaterial);
      wall.position.set(x, 0.08, 0);
      intake.group.add(wall);
    });
    const funnelMaterial = track(intake, standardMaterial(0x08a9c4, 0.62, { transparent: true, opacity: 0.9 }));
    const intakeFunnel = new THREE.Mesh(
      new THREE.CylinderGeometry(0.34, 0.14, 0.48, lowPower ? 20 : 32, 1, true),
      funnelMaterial,
    );
    intakeFunnel.position.y = 0.52;
    intake.group.add(intakeFunnel);
    const incomingPacketMaterial = track(intake, standardMaterial(0x155eef, 0.35, { emissiveIntensity: 0.35 }));
    const incomingPacket = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.18), incomingPacketMaterial);
    incomingPacket.position.y = 0.95;
    intake.group.add(incomingPacket);

    const delegate = createStation(1, 'Delegate');
    const delegateHubMaterial = track(delegate, standardMaterial(palette[1], 0.45, { emissiveIntensity: 0.24 }));
    const delegateHub = new THREE.Mesh(new THREE.SphereGeometry(0.2, 24, 16), delegateHubMaterial);
    delegateHub.position.y = 0.12;
    delegate.group.add(delegateHub);
    const delegateNodes = [
      new THREE.Vector3(-0.42, 0.58, 0.02),
      new THREE.Vector3(0.46, 0.5, -0.02),
      new THREE.Vector3(0.32, -0.16, 0.08),
    ].map((position, index) => {
      const material = track(delegate, standardMaterial([0x155eef, 0x16a36a, 0x7c5ce0][index], 0.45));
      const node = new THREE.Mesh(new THREE.SphereGeometry(0.13, 20, 12), material);
      node.position.copy(position);
      node.userData.basePosition = position.clone();
      delegate.group.add(node);
      delegate.group.add(cylinderBetween(
        new THREE.Vector3(0, 0.12, 0),
        position,
        0.014,
        basicMaterial([0x155eef, 0x16a36a, 0x7c5ce0][index], 0.48),
      ));
      return node;
    });

    const act = createStation(2, 'Act');
    const sandbox = new THREE.Mesh(
      new THREE.BoxGeometry(0.92, 0.86, 0.78),
      new THREE.MeshBasicMaterial({ color: palette[2], wireframe: true, transparent: true, opacity: 0.46 }),
    );
    sandbox.position.y = 0.16;
    act.group.add(sandbox);
    const actCoreMaterial = track(act, standardMaterial(palette[2], 0.36, { emissiveIntensity: 0.3 }));
    const actCore = new THREE.Mesh(new THREE.IcosahedronGeometry(0.25, 1), actCoreMaterial);
    actCore.position.y = 0.16;
    act.group.add(actCore);
    const scannerMaterial = new THREE.MeshBasicMaterial({
      color: 0x08a9c4,
      transparent: true,
      opacity: 0.22,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const scanner = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.022, 0.66), scannerMaterial);
    scanner.position.y = -0.2;
    act.group.add(scanner);

    const verify = createStation(3, 'Verify');
    const verifyRingMaterial = track(verify, standardMaterial(palette[3], 0.44, { emissiveIntensity: 0.22 }));
    const verifyRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.48, 0.065, 12, lowPower ? 36 : 64),
      verifyRingMaterial,
    );
    verifyRing.position.y = 0.14;
    verify.group.add(verifyRing);
    const verifyAuraMaterial = new THREE.MeshBasicMaterial({
      color: palette[3],
      transparent: true,
      opacity: 0.12,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const verifyAura = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.018, 8, 64), verifyAuraMaterial);
    verifyAura.position.copy(verifyRing.position);
    verify.group.add(verifyAura);
    const checkMaterial = track(verify, standardMaterial(0x16a36a, 0.18, { emissiveIntensity: 0.62 }));
    verify.group.add(cylinderBetween(
      new THREE.Vector3(-0.23, 0.13, 0.12),
      new THREE.Vector3(-0.06, -0.04, 0.12),
      0.045,
      checkMaterial,
      16,
    ));
    verify.group.add(cylinderBetween(
      new THREE.Vector3(-0.06, -0.04, 0.12),
      new THREE.Vector3(0.28, 0.34, 0.12),
      0.045,
      checkMaterial,
      16,
    ));
    const evidenceDots = [0, 1, 2].map((index) => {
      const dot = new THREE.Mesh(
        new THREE.SphereGeometry(0.055, 12, 8),
        basicMaterial(index === 1 ? 0x16a36a : 0x08a9c4, 0.84),
      );
      verify.group.add(dot);
      return dot;
    });

    const persist = createStation(4, 'Persist');
    const persistPlates = [0, 1, 2, 3].map((index) => {
      const material = track(persist, standardMaterial(index % 2 ? 0x155eef : 0x08a9c4, 0.58, { emissiveIntensity: 0.1 }));
      const plate = new THREE.Mesh(new THREE.BoxGeometry(0.88, 0.11, 0.62), material);
      plate.position.set(index * 0.035 - 0.05, -0.12 + index * 0.18, -index * 0.035);
      plate.userData.baseY = plate.position.y;
      persist.group.add(plate);
      return plate;
    });
    const receiptMaterial = track(persist, standardMaterial(0x16a36a, 0.34, { emissiveIntensity: 0.34 }));
    [-0.26, 0, 0.26].forEach((x, index) => {
      const receipt = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.18, 0.13), receiptMaterial);
      receipt.position.set(x, 0.66 + index * 0.04, 0.02);
      persist.group.add(receipt);
    });

    const decide = createStation(5, 'Decide');
    const decisionMaterial = track(decide, standardMaterial(palette[5], 0.38, { emissiveIntensity: 0.3 }));
    const decisionCore = new THREE.Mesh(new THREE.OctahedronGeometry(0.48, 0), decisionMaterial);
    decisionCore.position.y = 0.13;
    decide.group.add(decisionCore);
    const decisionRingMaterial = new THREE.MeshBasicMaterial({
      color: palette[5],
      transparent: true,
      opacity: 0.42,
      depthWrite: false,
    });
    const decisionRing = new THREE.Mesh(new THREE.TorusGeometry(0.61, 0.02, 8, 56), decisionRingMaterial);
    decisionRing.position.copy(decisionCore.position);
    decide.group.add(decisionRing);

    function endpoint(position, hex, shape = 'ring') {
      const group = new THREE.Group();
      group.position.copy(position);
      const material = standardMaterial(hex, 0.38, { emissiveIntensity: 0.42 });
      const mesh = shape === 'ring'
        ? new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.048, 10, 32), material)
        : new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 0), material);
      group.add(mesh);
      const halo = new THREE.Mesh(
        new THREE.TorusGeometry(0.3, 0.012, 8, 36),
        new THREE.MeshBasicMaterial({ color: hex, transparent: true, opacity: 0.24, depthWrite: false }),
      );
      group.add(halo);
      root.add(group);
      return { group, mesh, halo };
    }

    const exitEndpoint = endpoint(exitTarget, 0x16a36a, 'ring');
    const escalateEndpoint = endpoint(escalateTarget, 0xd97706, 'diamond');

    const packetMaterial = standardMaterial(palette[0], 0.28, { emissiveIntensity: 0.48, roughness: 0.22 });
    const packet = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.27, 0.28), packetMaterial);
    const packetEdgesMaterial = new THREE.LineBasicMaterial({ color: palette[0], transparent: true, opacity: 0.92 });
    const packetEdges = new THREE.LineSegments(new THREE.EdgesGeometry(packet.geometry), packetEdgesMaterial);
    const packetAuraMaterial = new THREE.MeshBasicMaterial({
      color: palette[0],
      transparent: true,
      opacity: 0.16,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const packetAura = new THREE.Mesh(new THREE.SphereGeometry(0.38, 18, 12), packetAuraMaterial);
    const packetBand = new THREE.Mesh(
      new THREE.BoxGeometry(0.372, 0.055, 0.292),
      basicMaterial(0xffffff, 0.94),
    );
    packetBand.position.y = 0.055;
    const packetGroup = new THREE.Group();
    packetGroup.add(packetAura, packet, packetEdges, packetBand);
    packetGroup.position.copy(stagePositions[0]);
    root.add(packetGroup);

    const trail = [];
    if (!lowPower) {
      for (let index = 0; index < 7; index += 1) {
        const material = new THREE.MeshBasicMaterial({
          color: palette[0],
          transparent: true,
          opacity: 0.22 * (1 - index / 8),
          depthWrite: false,
        });
        const point = new THREE.Mesh(new THREE.SphereGeometry(0.052 - index * 0.003, 10, 7), material);
        point.position.copy(packetGroup.position);
        trail.push(point);
        root.add(point);
      }
    }

    const retryPulse = new THREE.Mesh(
      new THREE.SphereGeometry(0.07, 14, 9),
      new THREE.MeshBasicMaterial({ color: 0x7c5ce0, transparent: true, opacity: 0.9, depthWrite: false }),
    );
    root.add(retryPulse);
    const exitPulse = new THREE.Mesh(new THREE.SphereGeometry(0.065, 14, 9), basicMaterial(0x16a36a, 0.9));
    const escalatePulse = new THREE.Mesh(new THREE.SphereGeometry(0.065, 14, 9), basicMaterial(0xd97706, 0.85));
    root.add(exitPulse, escalatePulse);

    let frameCount = 0;
    let animationFrame = 0;
    let visible = true;
    let targetRotationX = 0;
    let targetRotationY = 0;
    let layoutScaleX = 1;
    let layoutScaleY = 1;
    let stationLayoutScale = 1.12;
    let endpointLayoutScale = 1.08;
    let currentPacketColor = -1;
    let currentFlowStage = activeStage;
    const startedAt = performance.now();
    const targetPacketPosition = new THREE.Vector3();

    function setPacketColor(hex) {
      if (currentPacketColor === hex) return;
      currentPacketColor = hex;
      const color = new THREE.Color(hex);
      packetMaterial.color.copy(color).lerp(white, 0.28);
      packetMaterial.emissive.copy(color);
      packetEdgesMaterial.color.copy(color);
      packetAuraMaterial.color.copy(color);
      trail.forEach((point) => point.material.color.copy(color));
    }

    function nearestStage(time) {
      let nearest = 0;
      let distance = Infinity;
      stageTimes.forEach((stageTime, index) => {
        const candidate = Math.abs(stageTime - time);
        if (candidate < distance) {
          distance = candidate;
          nearest = index;
        }
      });
      return nearest;
    }

    function render(time = 0) {
      const seconds = Math.max(0, time - startedAt) * 0.001;
      const manual = reducedMotion.matches || performance.now() < manualSelectionUntil;
      let flowStage = activeStage;

      if (manual) {
        targetPacketPosition.copy(stagePositions[activeStage]);
        setPacketColor(palette[activeStage]);
      } else {
        const phase = (seconds * 0.062) % 1;
        if (phase < 0.76) {
          const progress = phase / 0.76;
          targetPacketPosition.copy(mainCurve.getPointAt(progress));
          flowStage = nearestStage(progress);
          setPacketColor(palette[flowStage]);
        } else {
          const progress = (phase - 0.76) / 0.24;
          targetPacketPosition.copy(retryCurve.getPointAt(progress));
          flowStage = progress > 0.84 ? 0 : 5;
          setPacketColor(progress > 0.84 ? palette[0] : 0x7c5ce0);
        }

        if (flowStage !== currentFlowStage) {
          currentFlowStage = flowStage;
          selectStage(flowStage);
        }
      }

      packetGroup.position.lerp(targetPacketPosition, reducedMotion.matches ? 1 : 0.16);
      packetGroup.rotation.x = seconds * 0.72;
      packetGroup.rotation.y = seconds * 0.94;
      const packetPulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 3.2) * 0.06;
      packetAura.scale.setScalar(packetPulse);

      let previous = packetGroup.position;
      trail.forEach((point, index) => {
        point.position.lerp(previous, 0.17 - index * 0.01);
        previous = point.position;
      });

      stationStates.forEach((state, index) => {
        const selected = index === activeStage;
        const packetDistance = state.group.position.distanceTo(packetGroup.position);
        const nearby = Math.max(0, 1 - packetDistance / 1.15);
        const scale = 1 + (selected ? 0.09 : 0) + nearby * 0.05;
        state.group.scale.setScalar(scale * stationLayoutScale);
        state.haloMaterial.opacity = selected ? 0.38 : 0.07 + nearby * 0.18;
        state.baseMaterial.emissiveIntensity = selected ? 0.17 : 0.035 + nearby * 0.08;
        state.materials.forEach((material) => {
          material.emissiveIntensity = selected ? Math.max(material.emissiveIntensity, 0.28) : 0.08 + nearby * 0.14;
        });
        state.label.material.opacity = selected ? 1 : 0.72;
      });

      incomingPacket.position.y = 0.88 - ((seconds * 0.42) % 1) * 0.34;
      incomingPacket.rotation.y = seconds * 0.8;
      delegateNodes.forEach((node, index) => {
        const pulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2.1 + index * 1.7) * 0.1;
        node.scale.setScalar(pulse);
      });
      delegateHub.rotation.y = seconds * 0.6;
      actCore.rotation.x = seconds * 0.54;
      actCore.rotation.y = seconds * 0.76;
      scanner.position.y = reducedMotion.matches ? 0.08 : -0.2 + ((Math.sin(seconds * 1.7) + 1) * 0.27);
      const gatePulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2.4) * 0.035;
      verifyRing.scale.setScalar(gatePulse);
      verifyAura.rotation.z = seconds * 0.16;
      verifyAuraMaterial.opacity = activeStage === 3 ? 0.34 : 0.12;
      evidenceDots.forEach((dot, index) => {
        const angle = seconds * 1.05 + index * (Math.PI * 2 / evidenceDots.length);
        dot.position.set(Math.cos(angle) * 0.68, 0.14 + Math.sin(angle) * 0.42, 0.02);
      });
      persistPlates.forEach((plate, index) => {
        plate.position.y = plate.userData.baseY + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.4 + index * 0.65) * 0.012);
      });
      decisionCore.rotation.y = seconds * 0.5;
      decisionCore.rotation.z = Math.PI / 4 + seconds * 0.12;
      decisionRing.rotation.z = -seconds * 0.18;

      retryPulse.position.copy(retryCurve.getPointAt((seconds * 0.13 + 0.17) % 1));
      exitPulse.position.copy(exitCurve.getPointAt((seconds * 0.24) % 1));
      escalatePulse.position.copy(escalateCurve.getPointAt((seconds * 0.19 + 0.45) % 1));
      const outcomePulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2) * 0.08;
      exitEndpoint.group.scale.setScalar(outcomePulse * endpointLayoutScale);
      escalateEndpoint.group.scale.setScalar((2 - outcomePulse) * endpointLayoutScale);

      root.rotation.x += (targetRotationX - root.rotation.x) * 0.045;
      root.rotation.y += (targetRotationY - root.rotation.y) * 0.045;
      root.scale.set(layoutScaleX, layoutScaleY, layoutScaleY);
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

    function buildRetryCurve(compact) {
      if (compact) {
        return new THREE.CatmullRomCurve3([
          stagePositions[5],
          new THREE.Vector3(-0.82, 0.02, -0.58),
          new THREE.Vector3(-2.5, 0.32, -0.76),
          stagePositions[0],
        ], false, 'centripetal', 0.42);
      }
      return new THREE.CatmullRomCurve3([
        stagePositions[5],
        new THREE.Vector3(3.7, 1.48, -0.55),
        new THREE.Vector3(0.1, 1.88, -0.82),
        new THREE.Vector3(-3.85, 1.4, -0.52),
        stagePositions[0],
      ], false, 'centripetal', 0.45);
    }

    function applySemanticLayout(compact) {
      const positions = compact ? compactStagePositions : desktopStagePositions;
      positions.forEach((position, index) => {
        stagePositions[index].copy(position);
        stationStates[index].group.position.copy(position);
      });

      mainCurve = new THREE.CatmullRomCurve3(stagePositions, false, 'centripetal', 0.35);
      replaceTubeGeometry(mainTube, mainCurve, 0.032, 180);
      replaceTubeGeometry(mainGlow, mainCurve, 0.095, 150);
      mainArrows.forEach((arrow, index) => positionArrow(arrow, mainCurve, mainArrowTimes[index]));
      stageTimes = stagePositions.map(closestCurveTime);

      retryCurve = buildRetryCurve(compact);
      retryLine.geometry.dispose();
      retryLine.geometry = new THREE.BufferGeometry().setFromPoints(
        retryCurve.getPoints(lowPower ? 90 : 160),
      );
      retryLine.computeLineDistances();
      retryArrows.forEach((arrow, index) => {
        positionArrow(arrow, retryCurve, retryArrowTimes[index]);
        arrow.visible = !compact || index !== 1;
      });

      if (compact) {
        exitTarget.set(-1.32, -1.5, 0.08);
        escalateTarget.set(-2.35, -1.48, 0.12);
        exitCurve = new THREE.CatmullRomCurve3([
          stagePositions[5],
          new THREE.Vector3(-0.62, -1.08, 0.04),
          exitTarget,
        ], false, 'centripetal', 0.35);
        escalateCurve = new THREE.CatmullRomCurve3([
          stagePositions[5],
          new THREE.Vector3(-1.18, -1.16, 0.06),
          escalateTarget,
        ], false, 'centripetal', 0.35);
      } else {
        exitTarget.set(5.35, 0.75, 0.08);
        escalateTarget.set(5.35, -0.72, 0.12);
        exitCurve = new THREE.CatmullRomCurve3([
          stagePositions[5],
          new THREE.Vector3(4.72, 0.3, 0.04),
          exitTarget,
        ], false, 'centripetal', 0.35);
        escalateCurve = new THREE.CatmullRomCurve3([
          stagePositions[5],
          new THREE.Vector3(4.7, -0.28, 0.06),
          escalateTarget,
        ], false, 'centripetal', 0.35);
      }
      replaceTubeGeometry(exitTube, exitCurve, 0.022, 60);
      replaceTubeGeometry(escalateTube, escalateCurve, 0.022, 60);
      positionArrow(exitArrow, exitCurve, 0.68);
      positionArrow(escalateArrow, escalateCurve, 0.68);
      exitEndpoint.group.position.copy(exitTarget);
      escalateEndpoint.group.position.copy(escalateTarget);
    }

    function resize() {
      const width = Math.max(container.clientWidth, 1);
      const height = Math.max(container.clientHeight, 1);
      const mobile = window.innerWidth < 640;
      const narrow = window.innerWidth < 360;
      const tablet = !mobile && window.innerWidth < 920;
      applySemanticLayout(mobile);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile || lowPower ? 1.25 : 1.6));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.fov = mobile ? 31 : 28;
      camera.position.set(0, narrow ? 1.55 : mobile ? 1.5 : 3.25, narrow ? 7.35 : mobile ? 6.9 : 9.15);
      camera.lookAt(0, mobile ? 0.05 : 0.12, 0);
      camera.updateProjectionMatrix();
      layoutScaleX = mobile ? 1 : tablet ? 1.08 : 1.3;
      layoutScaleY = mobile ? 1 : tablet ? 1 : 1.06;
      stationLayoutScale = narrow ? 0.84 : mobile ? 0.86 : tablet ? 1.04 : 1.12;
      endpointLayoutScale = mobile ? 0.9 : 1.08;
      root.position.y = mobile ? 0.02 : -0.06;
      labels.forEach((label) => { label.visible = width >= 760; });
      numberLabels.forEach((label) => { label.visible = width < 760; });
      render(performance.now());
    }

    function updatePointer(event) {
      const bounds = hero.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width * 2 - 1;
      const y = (event.clientY - bounds.top) / bounds.height * 2 - 1;
      targetRotationY = x * 0.035;
      targetRotationX = -y * 0.018;
    }

    function resetPointer() {
      targetRotationX = 0;
      targetRotationY = 0;
    }

    stageSubscribers.push(() => render(performance.now()));

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
        labelsVisible: labels.some((label) => label.visible),
        luminanceRange: maximumLuminance - minimumLuminance,
        lowPower,
        outcomes: 3,
        painted,
        paintedRatio: sampled ? painted / sampled : 0,
        reducedMotion: reducedMotion.matches,
        sampled,
        semanticStages: stationStates.length,
        triangles: renderer.info.render.triangles,
        width,
      };
    };

    window.__loopScenePause = () => {
      stopAnimation();
      manualSelectionUntil = performance.now() + 60000;
      packetGroup.position.copy(stagePositions[activeStage]);
      render(performance.now());
      return window.__loopSceneDiagnostics();
    };
    window.__loopSceneResume = () => {
      manualSelectionUntil = 0;
      startAnimation();
      return true;
    };

    resize();
    startAnimation();
  }
}
