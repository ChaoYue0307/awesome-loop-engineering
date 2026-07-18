import * as THREE from './vendor/three/three.module.min.js';

const container = document.querySelector('[data-loop-scene]');
const hero = container?.closest('.hero');
const stageButtons = Array.from(document.querySelectorAll('[data-loop-stage]'));
const stageDetail = document.getElementById('loop-stage-detail');
const stages = [
  ['Intake:', 'turn a queue signal, event, schedule, or goal into one bounded work packet.'],
  ['Delegate:', 'let an orchestrator route that packet to a specialist agent with explicit scope.'],
  ['Act:', 'give the agent a controlled workspace, relevant context, and scoped tools.'],
  ['Verify:', 'require evidence from tests, evals, traces, or independent review before progress.'],
  ['Persist:', 'write receipts, memory, and progress to durable state outside the model.'],
  ['Decide:', 'route the evidence to one bounded next action: retry, human escalation, or exit.'],
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
  const colors = {
    work: 0x08a9c4,
    orchestrator: 0x155eef,
    agent: 0x2868df,
    evidence: 0x0c9b68,
    state: 0x7055d9,
    decision: 0x4f46b8,
    retry: 0x7055d9,
    human: 0xd97706,
    exit: 0x0c9b68,
    ink: 0x172033,
    line: 0x91a0b8,
  };
  const palette = [
    colors.work,
    colors.orchestrator,
    colors.agent,
    colors.evidence,
    colors.state,
    colors.decision,
  ];
  const paper = new THREE.Color(0xf4f7fc);
  const white = new THREE.Color(0xffffff);
  const yAxis = new THREE.Vector3(0, 1, 0);
  const lineOffset = new THREE.Vector3(0, -0.08, -0.16);
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
    renderer.toneMappingExposure = 1.04;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.dataset.loopSceneCanvas = 'true';
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-6, 6, 2, -2, 0.1, 50);
    camera.position.set(0, 2.6, 10);
    camera.lookAt(0, 0, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0xb5c4da, 1.55));
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.05);
    keyLight.position.set(-4, 6, 8);
    scene.add(keyLight);
    const cyanLight = new THREE.PointLight(colors.work, 5.2, 12, 2);
    cyanLight.position.set(-2.3, 1.5, 4.5);
    scene.add(cyanLight);
    const greenLight = new THREE.PointLight(colors.evidence, 4.2, 10, 2);
    greenLight.position.set(2.2, 1.1, 4.2);
    scene.add(greenLight);

    const root = new THREE.Group();
    scene.add(root);

    function standardMaterial(hex, lighten = 0.28, options = {}) {
      const color = new THREE.Color(hex);
      const material = new THREE.MeshStandardMaterial({
        color: color.clone().lerp(white, Math.min(lighten, 0.46)),
        emissive: color,
        emissiveIntensity: options.emissiveIntensity ?? 0.06,
        metalness: options.metalness ?? 0.08,
        roughness: options.roughness ?? 0.38,
        transparent: options.transparent ?? false,
        opacity: options.opacity ?? 1,
        depthWrite: options.depthWrite ?? true,
      });
      material.userData.baseEmissiveIntensity = material.emissiveIntensity;
      return material;
    }

    function basicMaterial(hex, opacity = 1) {
      return new THREE.MeshBasicMaterial({
        color: hex,
        transparent: opacity < 1,
        opacity,
        depthWrite: opacity >= 0.94,
      });
    }

    function cylinderBetween(start, end, radius, material, segments = 12) {
      const direction = end.clone().sub(start);
      const cylinder = new THREE.Mesh(
        new THREE.CylinderGeometry(radius, radius, direction.length(), segments),
        material,
      );
      cylinder.position.copy(start).add(end).multiplyScalar(0.5);
      cylinder.quaternion.setFromUnitVectors(yAxis, direction.clone().normalize());
      return cylinder;
    }

    function makeTextSprite(text, hex, options = {}) {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 96;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.fillStyle = `#${new THREE.Color(hex).getHexString()}`;
      context.fillRect(22, 70, options.underlineWidth ?? 58, 5);
      context.fillStyle = options.textColor || '#172033';
      context.font = `${options.weight || 700} ${options.fontSize || 31}px Inter, Arial, sans-serif`;
      context.textAlign = 'left';
      context.textBaseline = 'middle';
      context.fillText(text, 22, 43);
      const texture = new THREE.CanvasTexture(canvas);
      texture.colorSpace = THREE.SRGBColorSpace;
      texture.minFilter = THREE.LinearFilter;
      const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }));
      sprite.scale.set(options.width || 1.52, options.height || 0.285, 1);
      sprite.renderOrder = 30;
      return sprite;
    }

    function makeNumberSprite(number, hex) {
      const canvas = document.createElement('canvas');
      canvas.width = 128;
      canvas.height = 128;
      const context = canvas.getContext('2d');
      context.beginPath();
      context.arc(64, 64, 48, 0, Math.PI * 2);
      context.fillStyle = '#f7f9fc';
      context.fill();
      context.lineWidth = 8;
      context.strokeStyle = `#${new THREE.Color(hex).getHexString()}`;
      context.stroke();
      context.fillStyle = '#172033';
      context.font = '700 50px Inter, Arial, sans-serif';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.fillText(String(number).padStart(2, '0'), 64, 67);
      const texture = new THREE.CanvasTexture(canvas);
      texture.colorSpace = THREE.SRGBColorSpace;
      const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
        map: texture,
        transparent: true,
        depthTest: false,
        depthWrite: false,
      }));
      sprite.scale.set(0.39, 0.39, 1);
      sprite.renderOrder = 31;
      return sprite;
    }

    function addTube(curve, radius, hex, opacity, segments = 160) {
      const material = new THREE.MeshBasicMaterial({
        color: hex,
        transparent: opacity < 1,
        opacity,
        depthWrite: false,
      });
      const mesh = new THREE.Mesh(
        new THREE.TubeGeometry(curve, lowPower ? Math.round(segments * 0.65) : segments, radius, 6, false),
        material,
      );
      root.add(mesh);
      return mesh;
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

    function addArrow(curve, time, hex, scale = 1) {
      const arrow = new THREE.Mesh(
        new THREE.ConeGeometry(0.055 * scale, 0.18 * scale, lowPower ? 10 : 16),
        basicMaterial(hex, 0.86),
      );
      root.add(arrow);
      positionArrow(arrow, curve, time);
      return arrow;
    }

    function positionArrow(arrow, curve, time) {
      const tangent = curve.getTangentAt(Math.min(0.999, time)).normalize();
      arrow.position.copy(curve.getPointAt(time));
      arrow.quaternion.setFromUnitVectors(yAxis, tangent);
    }

    const desktopStagePositions = [
      new THREE.Vector3(-4.45, -0.34, 0.06),
      new THREE.Vector3(-2.55, 0.72, 0),
      new THREE.Vector3(0, 0.02, 0.1),
      new THREE.Vector3(2.55, 0.72, 0),
      new THREE.Vector3(4.42, -0.34, 0.06),
      new THREE.Vector3(2.12, -1.08, 0),
    ];
    const compactStagePositions = [
      new THREE.Vector3(-1.72, 0.46, 0.04),
      new THREE.Vector3(-0.88, 0.96, 0),
      new THREE.Vector3(0, -0.02, 0.08),
      new THREE.Vector3(0.9, 0.96, 0),
      new THREE.Vector3(1.72, 0.46, 0.04),
      new THREE.Vector3(1.08, -0.82, 0),
    ];
    const stagePositions = desktopStagePositions.map((position) => position.clone());

    function buildMainCurve() {
      return new THREE.CatmullRomCurve3(
        stagePositions.map((position) => position.clone().add(lineOffset)),
        false,
        'centripetal',
        0.34,
      );
    }

    function buildRetryCurve(compact) {
      const start = stagePositions[5].clone().add(lineOffset);
      const end = stagePositions[0].clone().add(lineOffset);
      const controls = compact
        ? [
          start,
          new THREE.Vector3(0.1, -1.18, -0.5),
          new THREE.Vector3(-1.82, -0.9, -0.5),
          end,
        ]
        : [
          start,
          new THREE.Vector3(0.4, -1.54, -0.62),
          new THREE.Vector3(-2.5, -1.4, -0.72),
          new THREE.Vector3(-4.1, -0.95, -0.62),
          end,
        ];
      return new THREE.CatmullRomCurve3(controls, false, 'centripetal', 0.42);
    }

    let compactLayout = false;
    let mainCurve = buildMainCurve();
    let retryCurve = buildRetryCurve(false);
    const mainTube = addTube(mainCurve, 0.034, colors.orchestrator, 0.9, 180);
    const mainGlow = addTube(mainCurve, 0.078, colors.work, 0.1, 160);
    const retryLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(retryCurve.getPoints(lowPower ? 90 : 160)),
      new THREE.LineDashedMaterial({
        color: colors.retry,
        transparent: true,
        opacity: 0.72,
        dashSize: 0.12,
        gapSize: 0.09,
        depthWrite: false,
      }),
    );
    retryLine.computeLineDistances();
    root.add(retryLine);

    function closestCurveTime(position) {
      const target = position.clone().add(lineOffset);
      let closestTime = 0;
      let closestDistance = Infinity;
      for (let sample = 0; sample <= 200; sample += 1) {
        const time = sample / 200;
        const distance = mainCurve.getPointAt(time).distanceToSquared(target);
        if (distance < closestDistance) {
          closestDistance = distance;
          closestTime = time;
        }
      }
      return closestTime;
    }

    let stageTimes = stagePositions.map(closestCurveTime);
    let arrowTimes = stageTimes.slice(0, -1).map((time, index) => (time + stageTimes[index + 1]) / 2);
    const mainArrows = arrowTimes.map((time, index) => addArrow(mainCurve, time, palette[index + 1], 0.92));
    const retryArrows = [0.28, 0.55, 0.8].map((time) => addArrow(retryCurve, time, colors.retry, 0.84));

    const stationStates = [];
    const stationLabels = [];
    const numberLabels = [];
    const microLabels = [];

    function createStation(index, label, hex) {
      const group = new THREE.Group();
      group.position.copy(stagePositions[index]);
      root.add(group);

      const haloMaterial = new THREE.MeshBasicMaterial({
        color: hex,
        transparent: true,
        opacity: 0.11,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
      const halo = new THREE.Mesh(
        new THREE.TorusGeometry(0.57, 0.023, 8, lowPower ? 28 : 48),
        haloMaterial,
      );
      halo.rotation.x = Math.PI / 2;
      halo.position.y = -0.43;
      group.add(halo);

      const baseMaterial = standardMaterial(hex, 0.42, { roughness: 0.58, emissiveIntensity: 0.04 });
      const base = new THREE.Mesh(
        new THREE.CylinderGeometry(0.48, 0.56, 0.07, lowPower ? 20 : 32),
        baseMaterial,
      );
      base.position.y = -0.42;
      group.add(base);

      const title = makeTextSprite(label, hex);
      title.position.set(-0.03, 0.98, 0.08);
      group.add(title);
      stationLabels.push(title);

      const number = makeNumberSprite(index + 1, hex);
      number.position.set(0.43, 0.67, 0.28);
      group.add(number);
      numberLabels.push(number);

      const state = {
        baseScale: index === 2 ? 1.3 : 0.91,
        baseMaterial,
        group,
        haloMaterial,
        materials: [],
        title,
      };
      stationStates.push(state);
      return state;
    }

    function track(state, material) {
      state.materials.push(material);
      return material;
    }

    function addMicroLabel(group, text, hex, position, width = 0.72) {
      const label = makeTextSprite(text, hex, {
        width,
        height: 0.18,
        fontSize: 38,
        weight: 700,
        underlineWidth: 28,
      });
      label.position.copy(position);
      group.add(label);
      microLabels.push(label);
      return label;
    }

    const intake = createStation(0, 'WORK IN', colors.work);
    const queueCards = [];
    for (let index = 0; index < 3; index += 1) {
      const card = new THREE.Group();
      const bodyMaterial = track(intake, standardMaterial(colors.work, 0.5 - index * 0.05, {
        emissiveIntensity: 0.04,
        roughness: 0.54,
      }));
      const body = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.34, 0.08), bodyMaterial);
      card.add(body);
      const header = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.055, 0.018), basicMaterial(colors.work, 0.8));
      header.position.set(0, 0.1, 0.05);
      card.add(header);
      [0.01, -0.065].forEach((y, lineIndex) => {
        const line = new THREE.Mesh(
          new THREE.BoxGeometry(lineIndex ? 0.28 : 0.4, 0.025, 0.016),
          basicMaterial(0x8da0ba, 0.72),
        );
        line.position.set(-0.05, y, 0.052);
        card.add(line);
      });
      card.position.set(-0.12 + index * 0.12, -0.16 + index * 0.16, -index * 0.08);
      card.rotation.z = -0.06 + index * 0.03;
      intake.group.add(card);
      queueCards.push(card);
    }
    addMicroLabel(intake.group, 'GOAL / EVENT / QUEUE', colors.work, new THREE.Vector3(-0.05, -0.68, 0.18), 1.02);

    const delegate = createStation(1, 'ORCHESTRATOR', colors.orchestrator);
    const orchestratorCoreMaterial = track(delegate, standardMaterial(colors.orchestrator, 0.34, {
      emissiveIntensity: 0.34,
      roughness: 0.26,
    }));
    const orchestratorCore = new THREE.Mesh(
      new THREE.DodecahedronGeometry(0.22, 1),
      orchestratorCoreMaterial,
    );
    orchestratorCore.position.y = 0.08;
    delegate.group.add(orchestratorCore);
    const orchestratorRingMaterial = new THREE.MeshBasicMaterial({
      color: colors.orchestrator,
      transparent: true,
      opacity: 0.48,
      depthWrite: false,
    });
    const orchestratorRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.42, 0.026, 10, lowPower ? 36 : 56),
      orchestratorRingMaterial,
    );
    orchestratorRing.position.copy(orchestratorCore.position);
    delegate.group.add(orchestratorRing);
    const routerNodePositions = [
      new THREE.Vector3(-0.4, 0.48, 0.02),
      new THREE.Vector3(0.4, 0.48, 0.02),
      new THREE.Vector3(0, -0.24, 0.06),
    ];
    const routerNodes = routerNodePositions.map((position, index) => {
      const material = track(delegate, standardMaterial([colors.work, colors.agent, colors.evidence][index], 0.42, {
        emissiveIntensity: 0.18,
      }));
      const node = new THREE.Mesh(new THREE.SphereGeometry(0.1, 18, 12), material);
      node.position.copy(position);
      delegate.group.add(node);
      delegate.group.add(cylinderBetween(
        orchestratorCore.position,
        position,
        0.012,
        basicMaterial([colors.work, colors.agent, colors.evidence][index], 0.62),
      ));
      return node;
    });
    addMicroLabel(delegate.group, 'SCOPE + ROUTE', colors.orchestrator, new THREE.Vector3(-0.03, -0.68, 0.18), 0.9);

    const act = createStation(2, 'AGENT + TOOLS', colors.agent);
    const workspaceGeometry = new THREE.BoxGeometry(1.16, 0.82, 0.62);
    const workspace = new THREE.LineSegments(
      new THREE.EdgesGeometry(workspaceGeometry),
      new THREE.LineBasicMaterial({ color: colors.agent, transparent: true, opacity: 0.56 }),
    );
    workspace.position.y = 0.03;
    act.group.add(workspace);
    const workspaceFloor = new THREE.Mesh(
      new THREE.BoxGeometry(1.1, 0.035, 0.56),
      track(act, standardMaterial(colors.agent, 0.48, { transparent: true, opacity: 0.78, depthWrite: false })),
    );
    workspaceFloor.position.y = -0.365;
    act.group.add(workspaceFloor);
    const agentCoreGroup = new THREE.Group();
    agentCoreGroup.position.set(0, -0.02, 0.08);
    const agentCoreMaterial = track(act, standardMaterial(colors.agent, 0.3, {
      emissiveIntensity: 0.34,
      roughness: 0.24,
    }));
    const agentBody = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.18, 0.29, 20), agentCoreMaterial);
    agentBody.position.y = 0.02;
    const agentHead = new THREE.Mesh(new THREE.SphereGeometry(0.165, 24, 16), agentCoreMaterial);
    agentHead.position.y = 0.28;
    const agentVisor = new THREE.Mesh(new THREE.BoxGeometry(0.205, 0.05, 0.045), basicMaterial(0x172033, 0.9));
    agentVisor.position.set(0, 0.29, 0.14);
    const agentCore = new THREE.Mesh(
      new THREE.SphereGeometry(0.055, 16, 10),
      track(act, standardMaterial(colors.work, 0.08, { emissiveIntensity: 0.78, roughness: 0.18 })),
    );
    agentCore.position.set(0, 0.03, 0.17);
    const agentRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.24, 0.018, 8, 42),
      new THREE.MeshBasicMaterial({ color: colors.work, transparent: true, opacity: 0.5, depthWrite: false }),
    );
    agentRing.position.set(0, 0.03, 0.02);
    agentCoreGroup.add(agentBody, agentHead, agentVisor, agentCore, agentRing);
    act.group.add(agentCoreGroup);

    const roleNames = ['CODE', 'BROWSE', 'SHELL'];
    const roleColors = [colors.work, colors.evidence, colors.state];
    const toolPositions = [
      new THREE.Vector3(-0.43, -0.04, 0.04),
      new THREE.Vector3(0.43, -0.04, 0.04),
      new THREE.Vector3(0, -0.3, 0.05),
    ];
    const toolPods = toolPositions.map((position, index) => {
      const material = track(act, standardMaterial(roleColors[index], 0.36, { emissiveIntensity: 0.22 }));
      const tool = index === 0
        ? new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.14), material)
        : index === 1
          ? new THREE.Mesh(new THREE.IcosahedronGeometry(0.095, 1), material)
          : new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.105, 0.13, 16), material);
      tool.position.copy(position);
      tool.userData.basePosition = position.clone();
      act.group.add(tool);
      act.group.add(cylinderBetween(
        new THREE.Vector3(0, 0.03, 0.06),
        position,
        0.009,
        basicMaterial(roleColors[index], 0.55),
      ));
      return tool;
    });
    addMicroLabel(act.group, 'CONTEXT + TOOLS', colors.agent, new THREE.Vector3(-0.05, -0.68, 0.2), 0.92);
    const contextChips = roleColors.map((hex, index) => {
      const chip = new THREE.Mesh(
        new THREE.BoxGeometry(0.19, 0.12, 0.035),
        track(act, standardMaterial(hex, 0.4, { emissiveIntensity: 0.12 })),
      );
      chip.position.set((index - 1) * 0.29, 0.52 + (index % 2) * 0.035, 0.02);
      chip.userData.baseY = chip.position.y;
      act.group.add(chip);
      return chip;
    });

    const verify = createStation(3, 'INDEPENDENT GATE', colors.evidence);
    const gateMaterial = track(verify, standardMaterial(colors.evidence, 0.45, { emissiveIntensity: 0.18 }));
    [-0.36, 0.36].forEach((x) => {
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.75, 0.16), gateMaterial);
      post.position.set(x, -0.02, 0);
      verify.group.add(post);
    });
    const gateTop = new THREE.Mesh(new THREE.BoxGeometry(0.83, 0.11, 0.16), gateMaterial);
    gateTop.position.set(0, 0.36, 0);
    verify.group.add(gateTop);
    const scannerMaterial = new THREE.MeshBasicMaterial({
      color: colors.evidence,
      transparent: true,
      opacity: 0.22,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const scanner = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.025, 0.34), scannerMaterial);
    scanner.position.set(0, -0.22, 0.02);
    verify.group.add(scanner);
    const checkMaterial = track(verify, standardMaterial(colors.evidence, 0.18, { emissiveIntensity: 0.62 }));
    verify.group.add(cylinderBetween(
      new THREE.Vector3(-0.19, -0.01, 0.12),
      new THREE.Vector3(-0.04, -0.16, 0.12),
      0.036,
      checkMaterial,
      14,
    ));
    verify.group.add(cylinderBetween(
      new THREE.Vector3(-0.04, -0.16, 0.12),
      new THREE.Vector3(0.24, 0.16, 0.12),
      0.036,
      checkMaterial,
      14,
    ));
    const evidenceTokens = [0, 1, 2].map((index) => {
      const token = new THREE.Mesh(
        new THREE.SphereGeometry(0.045, 12, 8),
        basicMaterial(index === 1 ? colors.evidence : colors.work, 0.88),
      );
      verify.group.add(token);
      return token;
    });
    addMicroLabel(verify.group, 'TESTS / EVALS / TRACES', colors.evidence, new THREE.Vector3(-0.05, -0.68, 0.18), 1.05);

    const persist = createStation(4, 'DURABLE MEMORY', colors.state);
    const stateLayers = [0, 1, 2].map((index) => {
      const material = track(persist, standardMaterial(index === 1 ? colors.orchestrator : colors.state, 0.34, {
        emissiveIntensity: 0.12,
        roughness: 0.42,
      }));
      const layer = new THREE.Mesh(
        new THREE.CylinderGeometry(0.4, 0.4, 0.115, lowPower ? 22 : 34),
        material,
      );
      layer.position.set(0, -0.2 + index * 0.18, 0);
      persist.group.add(layer);
      return layer;
    });
    const receiptCards = [-0.24, 0, 0.24].map((x, index) => {
      const receipt = new THREE.Group();
      const body = new THREE.Mesh(
        new THREE.BoxGeometry(0.15, 0.22, 0.05),
        track(persist, standardMaterial(colors.state, 0.46, { emissiveIntensity: 0.1 })),
      );
      const mark = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.03, 0.012), basicMaterial(colors.evidence, 0.82));
      mark.position.set(0, 0.06, 0.035);
      receipt.add(body, mark);
      receipt.position.set(x, 0.48 + index * 0.035, 0.02);
      receipt.userData.baseY = receipt.position.y;
      persist.group.add(receipt);
      return receipt;
    });
    addMicroLabel(persist.group, 'RECEIPTS + MEMORY', colors.state, new THREE.Vector3(-0.04, -0.68, 0.18), 0.92);

    const decide = createStation(5, 'DECISION', colors.decision);
    const decisionCoreMaterial = track(decide, standardMaterial(colors.decision, 0.35, {
      emissiveIntensity: 0.3,
      roughness: 0.28,
    }));
    const decisionCore = new THREE.Mesh(new THREE.OctahedronGeometry(0.22, 0), decisionCoreMaterial);
    decisionCore.position.y = 0.08;
    decide.group.add(decisionCore);
    const decisionRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.33, 0.022, 8, 44),
      new THREE.MeshBasicMaterial({ color: colors.decision, transparent: true, opacity: 0.42, depthWrite: false }),
    );
    decisionRing.position.copy(decisionCore.position);
    decide.group.add(decisionRing);
    const outcomeSpecs = [
      { label: 'RETRY', color: colors.retry, position: new THREE.Vector3(-0.43, 0.5, 0.02), shape: 'ring' },
      { label: 'EXIT', color: colors.exit, position: new THREE.Vector3(0.43, 0.5, 0.02), shape: 'ring' },
      { label: 'HUMAN', color: colors.human, position: new THREE.Vector3(0, -0.31, 0.04), shape: 'diamond' },
    ];
    const outcomeNodes = outcomeSpecs.map((spec) => {
      decide.group.add(cylinderBetween(
        decisionCore.position,
        spec.position,
        0.012,
        basicMaterial(spec.color, 0.72),
      ));
      const material = track(decide, standardMaterial(spec.color, 0.36, { emissiveIntensity: 0.3 }));
      const mesh = spec.shape === 'ring'
        ? new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.03, 8, 28), material)
        : new THREE.Mesh(new THREE.OctahedronGeometry(0.11, 0), material);
      mesh.userData.outcome = spec.label;
      mesh.position.copy(spec.position);
      decide.group.add(mesh);
      return mesh;
    });
    addMicroLabel(decide.group, 'RETRY / HUMAN / EXIT', colors.decision, new THREE.Vector3(-0.04, -0.68, 0.16), 0.98);

    const packetMaterial = standardMaterial(colors.work, 0.3, { emissiveIntensity: 0.46, roughness: 0.2 });
    const packetBody = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.25, 0.075), packetMaterial);
    const packetHeader = new THREE.Mesh(new THREE.BoxGeometry(0.33, 0.052, 0.018), basicMaterial(0xffffff, 0.96));
    packetHeader.position.set(0, 0.071, 0.047);
    const packetLine = new THREE.Mesh(new THREE.BoxGeometry(0.23, 0.027, 0.016), basicMaterial(0xd8e2f1, 0.92));
    packetLine.position.set(-0.03, -0.03, 0.048);
    const packetMarker = new THREE.Mesh(new THREE.BoxGeometry(0.052, 0.052, 0.02), basicMaterial(colors.evidence, 0.9));
    packetMarker.position.set(0.13, -0.035, 0.052);
    const taskArtifact = new THREE.Group();
    taskArtifact.add(packetBody, packetHeader, packetLine, packetMarker);

    const assignmentArtifact = new THREE.Group();
    const assignmentCore = new THREE.Mesh(
      new THREE.DodecahedronGeometry(0.13, 0),
      standardMaterial(colors.orchestrator, 0.28, { emissiveIntensity: 0.42, roughness: 0.24 }),
    );
    const assignmentRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.2, 0.025, 8, 36),
      basicMaterial(colors.orchestrator, 0.82),
    );
    assignmentArtifact.add(assignmentCore, assignmentRing);

    const actionArtifact = new THREE.Group();
    const actionCore = new THREE.Mesh(
      new THREE.SphereGeometry(0.12, 18, 12),
      standardMaterial(colors.agent, 0.24, { emissiveIntensity: 0.48, roughness: 0.22 }),
    );
    actionArtifact.add(actionCore);
    [-0.2, 0, 0.2].forEach((x, index) => {
      const toolSignal = new THREE.Mesh(
        new THREE.BoxGeometry(0.075, 0.075, 0.075),
        basicMaterial(roleColors[index], 0.94),
      );
      toolSignal.position.set(x, index === 1 ? 0.2 : -0.16, 0);
      actionArtifact.add(toolSignal);
    });

    const evidenceArtifact = new THREE.Group();
    const evidenceBadge = new THREE.Mesh(
      new THREE.CircleGeometry(0.2, 6),
      standardMaterial(colors.evidence, 0.28, { emissiveIntensity: 0.44, roughness: 0.24 }),
    );
    evidenceArtifact.add(evidenceBadge);
    evidenceArtifact.add(cylinderBetween(
      new THREE.Vector3(-0.095, -0.005, 0.04),
      new THREE.Vector3(-0.025, -0.08, 0.04),
      0.018,
      basicMaterial(0xffffff, 0.96),
      10,
    ));
    evidenceArtifact.add(cylinderBetween(
      new THREE.Vector3(-0.025, -0.08, 0.04),
      new THREE.Vector3(0.12, 0.1, 0.04),
      0.018,
      basicMaterial(0xffffff, 0.96),
      10,
    ));

    const stateArtifact = new THREE.Group();
    [-0.09, 0, 0.09].forEach((y, index) => {
      const layer = new THREE.Mesh(
        new THREE.CylinderGeometry(0.17, 0.17, 0.07, 22),
        standardMaterial(index === 1 ? colors.orchestrator : colors.state, 0.3, {
          emissiveIntensity: 0.34,
          roughness: 0.3,
        }),
      );
      layer.position.y = y;
      stateArtifact.add(layer);
    });

    const decisionArtifact = new THREE.Group();
    const decisionSignal = new THREE.Mesh(
      new THREE.OctahedronGeometry(0.16, 0),
      standardMaterial(colors.decision, 0.26, { emissiveIntensity: 0.5, roughness: 0.2 }),
    );
    const decisionSignalRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.22, 0.02, 8, 36),
      basicMaterial(colors.decision, 0.78),
    );
    decisionArtifact.add(decisionSignal, decisionSignalRing);

    const packetAuraMaterial = new THREE.MeshBasicMaterial({
      color: colors.work,
      transparent: true,
      opacity: 0.14,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const packetAura = new THREE.Mesh(new THREE.SphereGeometry(0.31, 16, 10), packetAuraMaterial);
    const packetGroup = new THREE.Group();
    const packetRepresentations = [
      taskArtifact,
      assignmentArtifact,
      actionArtifact,
      evidenceArtifact,
      stateArtifact,
      decisionArtifact,
    ];
    packetRepresentations.forEach((artifact, index) => {
      artifact.visible = index === 0;
      packetGroup.add(artifact);
    });
    packetGroup.add(packetAura);
    packetGroup.position.copy(mainCurve.getPointAt(0));
    packetGroup.position.z = 0.24;
    root.add(packetGroup);

    const trail = [];
    if (!lowPower) {
      for (let index = 0; index < 6; index += 1) {
        const point = new THREE.Mesh(
          new THREE.SphereGeometry(0.042 - index * 0.003, 9, 6),
          new THREE.MeshBasicMaterial({
            color: colors.work,
            transparent: true,
            opacity: 0.18 * (1 - index / 7),
            depthWrite: false,
          }),
        );
        point.position.copy(packetGroup.position);
        trail.push(point);
        root.add(point);
      }
    }

    const retryPulse = new THREE.Mesh(
      new THREE.SphereGeometry(0.06, 12, 8),
      basicMaterial(colors.retry, 0.9),
    );
    root.add(retryPulse);

    let frameCount = 0;
    let animationFrame = 0;
    let visible = true;
    let flowStage = 0;
    let targetRotationX = 0;
    let targetRotationY = 0;
    let stationScale = 1;
    let currentPacketColor = -1;
    const startedAt = performance.now();
    const targetPacketPosition = new THREE.Vector3();
    const targetPacketTangent = new THREE.Vector3(1, 0, 0);

    function setPacketColor(hex) {
      if (currentPacketColor === hex) return;
      currentPacketColor = hex;
      const color = new THREE.Color(hex);
      packetMaterial.color.copy(color).lerp(white, 0.3);
      packetMaterial.emissive.copy(color);
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
      let visualStage = activeStage;

      if (manual) {
        targetPacketPosition.copy(stagePositions[activeStage]).add(lineOffset);
        targetPacketTangent.set(1, 0, 0);
        setPacketColor(palette[activeStage]);
        visualStage = activeStage;
      } else {
        const phase = (seconds * 0.055) % 1;
        if (phase < 0.8) {
          const progress = phase / 0.8;
          targetPacketPosition.copy(mainCurve.getPointAt(progress));
          targetPacketTangent.copy(mainCurve.getTangentAt(Math.min(progress, 0.999)));
          flowStage = nearestStage(progress);
          visualStage = flowStage;
          setPacketColor(palette[flowStage]);
        } else {
          const progress = (phase - 0.8) / 0.2;
          targetPacketPosition.copy(retryCurve.getPointAt(progress));
          targetPacketTangent.copy(retryCurve.getTangentAt(Math.min(progress, 0.999)));
          flowStage = progress > 0.86 ? 0 : 5;
          visualStage = flowStage;
          setPacketColor(progress > 0.86 ? colors.work : colors.retry);
        }
      }

      packetRepresentations.forEach((artifact, index) => {
        artifact.visible = index === visualStage;
      });
      targetPacketPosition.z = 0.24;
      packetGroup.position.lerp(targetPacketPosition, reducedMotion.matches ? 1 : 0.18);
      const targetAngle = Math.atan2(targetPacketTangent.y, targetPacketTangent.x);
      packetGroup.rotation.z += (targetAngle - packetGroup.rotation.z) * 0.12;
      const packetPulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 3.1) * 0.055;
      packetAura.scale.setScalar(packetPulse);

      let previous = packetGroup.position;
      trail.forEach((point, index) => {
        point.position.lerp(previous, 0.18 - index * 0.012);
        previous = point.position;
      });

      stationStates.forEach((state, index) => {
        const selected = index === visualStage;
        const packetDistance = state.group.position.distanceTo(packetGroup.position);
        const nearby = Math.max(0, 1 - packetDistance / 1.2);
        const scale = stationScale * state.baseScale * (1 + (selected ? 0.075 : 0) + nearby * 0.025);
        state.group.scale.setScalar(scale);
        state.haloMaterial.opacity = selected ? 0.32 : 0.07 + nearby * 0.12;
        state.baseMaterial.emissiveIntensity = selected ? 0.14 : 0.025 + nearby * 0.05;
        state.materials.forEach((material) => {
          const base = material.userData.baseEmissiveIntensity || 0;
          material.emissiveIntensity = base + (selected ? 0.18 : nearby * 0.08);
        });
        state.title.material.opacity = selected ? 1 : 0.9;
      });

      queueCards.forEach((card, index) => {
        card.position.y = -0.16 + index * 0.16 + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.25 + index) * 0.012);
      });
      orchestratorCore.rotation.x = seconds * 0.38;
      orchestratorCore.rotation.y = seconds * 0.58;
      orchestratorRing.rotation.z = -seconds * 0.22;
      routerNodes.forEach((node, index) => {
        const pulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2 + index * 1.8) * 0.08;
        node.scale.setScalar(pulse);
      });
      const agentWorking = reducedMotion.matches ? 0 : Math.sin(seconds * 1.8) * 0.018;
      agentCoreGroup.position.y = -0.02 + agentWorking;
      agentRing.rotation.z = -seconds * 0.3;
      agentCore.scale.setScalar(reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2.4) * 0.1);
      toolPods.forEach((tool, index) => {
        tool.position.copy(tool.userData.basePosition);
        tool.position.y += reducedMotion.matches ? 0 : Math.sin(seconds * 1.7 + index * 1.7) * 0.018;
        tool.rotation.y = seconds * (index % 2 ? -0.34 : 0.34);
      });
      contextChips.forEach((chip, index) => {
        chip.position.y = chip.userData.baseY + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.4 + index) * 0.025);
        chip.rotation.y = seconds * 0.25 + index * 0.5;
      });
      scanner.position.y = reducedMotion.matches ? 0.02 : -0.22 + ((Math.sin(seconds * 1.65) + 1) * 0.22);
      scannerMaterial.opacity = visualStage === 3 ? 0.4 : 0.2;
      evidenceTokens.forEach((token, index) => {
        const angle = seconds * 1.1 + index * (Math.PI * 2 / evidenceTokens.length);
        token.position.set(Math.cos(angle) * 0.5, 0.02 + Math.sin(angle) * 0.35, 0.08);
      });
      stateLayers.forEach((layer, index) => {
        layer.rotation.y = seconds * (index % 2 ? -0.08 : 0.08);
      });
      receiptCards.forEach((receipt, index) => {
        receipt.position.y = receipt.userData.baseY + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.35 + index * 0.7) * 0.018);
      });
      decisionCore.rotation.y = seconds * 0.52;
      decisionCore.rotation.z = Math.PI / 4 + seconds * 0.12;
      decisionRing.rotation.z = -seconds * 0.2;
      outcomeNodes.forEach((node, index) => {
        const pulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 1.8 + index * 1.9) * 0.07;
        node.scale.setScalar(pulse);
      });
      assignmentCore.rotation.x = seconds * 0.5;
      assignmentCore.rotation.y = seconds * 0.7;
      assignmentRing.rotation.z = -seconds * 0.32;
      actionArtifact.rotation.z = seconds * 0.2;
      evidenceArtifact.rotation.z = reducedMotion.matches ? 0 : Math.sin(seconds * 1.2) * 0.08;
      stateArtifact.rotation.y = seconds * 0.28;
      decisionSignal.rotation.y = seconds * 0.6;
      decisionSignalRing.rotation.z = -seconds * 0.28;
      retryPulse.position.copy(retryCurve.getPointAt((seconds * 0.12 + 0.2) % 1));

      root.rotation.x += (targetRotationX - root.rotation.x) * 0.04;
      root.rotation.y += (targetRotationY - root.rotation.y) * 0.04;
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

    function applyLayout(compact) {
      compactLayout = compact;
      const positions = compact ? compactStagePositions : desktopStagePositions;
      positions.forEach((position, index) => {
        stagePositions[index].copy(position);
        stationStates[index].group.position.copy(position);
      });

      mainCurve = buildMainCurve();
      replaceTubeGeometry(mainTube, mainCurve, 0.034, 180);
      replaceTubeGeometry(mainGlow, mainCurve, 0.078, 160);
      stageTimes = stagePositions.map(closestCurveTime);
      arrowTimes = stageTimes.slice(0, -1).map((time, index) => (time + stageTimes[index + 1]) / 2);
      mainArrows.forEach((arrow, index) => positionArrow(arrow, mainCurve, arrowTimes[index]));

      retryCurve = buildRetryCurve(compact);
      retryLine.geometry.dispose();
      retryLine.geometry = new THREE.BufferGeometry().setFromPoints(
        retryCurve.getPoints(lowPower ? 90 : 160),
      );
      retryLine.computeLineDistances();
      retryArrows.forEach((arrow, index) => {
        positionArrow(arrow, retryCurve, [0.28, 0.55, 0.8][index]);
        arrow.visible = !compact || index === 1;
      });
    }

    function resize() {
      const width = Math.max(container.clientWidth, 1);
      const height = Math.max(container.clientHeight, 1);
      const compact = width < 720;
      const narrow = width < 350;
      const tablet = !compact && width < 900;
      applyLayout(compact);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, compact || lowPower ? 1.3 : 1.65));
      renderer.setSize(width, height, false);

      const aspect = width / height;
      const viewHeight = compact
        ? Math.max(3.42, (narrow ? 5.42 : 5.2) / aspect)
        : tablet
          ? 11.6 / aspect
          : 3.48;
      const viewWidth = viewHeight * aspect;
      camera.left = -viewWidth / 2;
      camera.right = viewWidth / 2;
      camera.top = viewHeight / 2;
      camera.bottom = -viewHeight / 2;
      camera.position.set(0, compact ? 2.0 : 2.6, 10);
      camera.lookAt(0, compact ? -0.05 : 0, 0);
      camera.updateProjectionMatrix();

      stationScale = narrow ? 0.78 : compact ? 0.82 : tablet ? 0.88 : 0.96;
      packetGroup.scale.setScalar(narrow ? 1.02 : compact ? 1.08 : 1);
      stationLabels.forEach((label) => {
        label.visible = !compact;
        label.position.y = 0.98;
        label.scale.set(tablet ? 1.34 : 1.52, 0.285, 1);
      });
      numberLabels.forEach((label) => {
        label.visible = compact;
        label.scale.setScalar(narrow ? 0.4 : compact ? 0.43 : 0.39);
      });
      microLabels.forEach((label) => { label.visible = width >= 980; });
      render(performance.now());
    }

    function updatePointer(event) {
      if (compactLayout) return;
      const bounds = hero.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width * 2 - 1;
      const y = (event.clientY - bounds.top) / bounds.height * 2 - 1;
      targetRotationY = x * 0.028;
      targetRotationX = -y * 0.014;
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
        const distanceFromPaper = Math.abs(red - 244) + Math.abs(green - 247) + Math.abs(blue - 252);
        const luminance = red * 0.2126 + green * 0.7152 + blue * 0.0722;
        sampled += 1;
        if (distanceFromPaper > 24) painted += 1;
        minimumLuminance = Math.min(minimumLuminance, luminance);
        maximumLuminance = Math.max(maximumLuminance, luminance);
      }
      return {
        activeStage,
        boundedAgent: true,
        compactLayout,
        contextInputs: contextChips.length,
        drawCalls: renderer.info.render.calls,
        durableMemory: true,
        externalVerifier: true,
        flowStage,
        frameCount,
        height,
        labelsVisible: stationLabels.some((label) => label.visible),
        luminanceRange: maximumLuminance - minimumLuminance,
        lowPower,
        outcomes: outcomeNodes.length,
        painted,
        paintedRatio: sampled ? painted / sampled : 0,
        reducedMotion: reducedMotion.matches,
        sampled,
        semanticStages: stationStates.length,
        scopedTools: roleNames.length,
        triangles: renderer.info.render.triangles,
        width,
      };
    };

    window.__loopScenePause = () => {
      stopAnimation();
      manualSelectionUntil = performance.now() + 60000;
      packetGroup.position.copy(stagePositions[activeStage]).add(lineOffset);
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

const stackContainer = document.querySelector('[data-stack-scene]');
const desktopStackMedia = window.matchMedia('(min-width: 561px)');
let stackSceneInitialized = false;

function initStackScene() {
  if (!stackContainer || stackSceneInitialized || !desktopStackMedia.matches) return;
  stackSceneInitialized = true;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const lowPower = Number(navigator.hardwareConcurrency || 8) <= 4;
  const colors = {
    prompt: 0x172033,
    context: 0x0c8b66,
    harness: 0x098fb8,
    loop: 0x155eef,
    violet: 0x7055d9,
    evidence: 0x0c9b68,
    human: 0xd97706,
    line: 0x91a0b8,
  };
  const paper = new THREE.Color(0xf4f7fc);
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
    stackContainer.dataset.sceneState = 'fallback';
    return;
  }

  renderer.setClearColor(paper, 1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.02;
  renderer.domElement.setAttribute('aria-hidden', 'true');
  renderer.domElement.dataset.stackSceneCanvas = 'true';
  stackContainer.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-4, 4, 2.5, -2.5, 0.1, 40);
  camera.position.set(0, 3.5, 10);
  camera.lookAt(0, 0, 0);

  scene.add(new THREE.HemisphereLight(0xffffff, 0xb9c8dc, 1.7));
  const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
  keyLight.position.set(-4, 6, 8);
  scene.add(keyLight);
  const blueLight = new THREE.PointLight(colors.loop, 4.6, 12, 2);
  blueLight.position.set(-1.4, 2.2, 4.4);
  scene.add(blueLight);
  const greenLight = new THREE.PointLight(colors.evidence, 3.8, 10, 2);
  greenLight.position.set(1.2, -0.2, 4.2);
  scene.add(greenLight);

  const root = new THREE.Group();
  scene.add(root);
  const stack = new THREE.Group();
  stack.position.x = -1.25;
  root.add(stack);

  function material(hex, lighten = 0.36, options = {}) {
    const color = new THREE.Color(hex);
    const result = new THREE.MeshStandardMaterial({
      color: color.clone().lerp(white, Math.min(lighten, 0.58)),
      emissive: color,
      emissiveIntensity: options.emissiveIntensity ?? 0.08,
      metalness: options.metalness ?? 0.08,
      roughness: options.roughness ?? 0.4,
      transparent: options.transparent ?? false,
      opacity: options.opacity ?? 1,
      depthWrite: options.depthWrite ?? true,
    });
    result.userData.baseEmissiveIntensity = result.emissiveIntensity;
    return result;
  }

  function basic(hex, opacity = 1) {
    return new THREE.MeshBasicMaterial({
      color: hex,
      transparent: opacity < 1,
      opacity,
      depthWrite: opacity >= 0.94,
    });
  }

  function cylinderBetween(start, end, radius, meshMaterial) {
    const direction = end.clone().sub(start);
    const cylinder = new THREE.Mesh(
      new THREE.CylinderGeometry(radius, radius, direction.length(), 12),
      meshMaterial,
    );
    cylinder.position.copy(start).add(end).multiplyScalar(0.5);
    cylinder.quaternion.setFromUnitVectors(yAxis, direction.clone().normalize());
    return cylinder;
  }

  function makeLayerLabel(title, description, hex) {
    const canvas = document.createElement('canvas');
    canvas.width = 768;
    canvas.height = 160;
    const context = canvas.getContext('2d');
    const accent = `#${new THREE.Color(hex).getHexString()}`;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = accent;
    context.fillRect(20, 29, 42, 5);
    context.fillStyle = accent;
    context.font = '700 38px Inter, Arial, sans-serif';
    context.textAlign = 'left';
    context.textBaseline = 'middle';
    context.fillText(title, 20, 67);
    context.fillStyle = '#4d5b70';
    context.font = '500 23px Inter, Arial, sans-serif';
    context.fillText(description, 20, 111);
    const texture = new THREE.CanvasTexture(canvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.minFilter = THREE.LinearFilter;
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      depthTest: false,
      depthWrite: false,
    }));
    sprite.scale.set(3.5, 0.73, 1);
    sprite.renderOrder = 40;
    return sprite;
  }

  function makeMicroLabel(text, hex, width = 1.15) {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 96;
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = `#${new THREE.Color(hex).getHexString()}`;
    context.font = '700 29px IBM Plex Mono, monospace';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(text, 256, 48);
    const texture = new THREE.CanvasTexture(canvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      depthTest: false,
      depthWrite: false,
    }));
    sprite.scale.set(width, 0.22, 1);
    sprite.renderOrder = 42;
    return sprite;
  }

  const layerSpecs = [
    { title: 'Prompt Engineering', description: 'Instruction for one model call', color: colors.prompt, y: -1.32 },
    { title: 'Context Engineering', description: 'Memory, state, documents, examples', color: colors.context, y: -0.62 },
    { title: 'Harness Engineering', description: 'Tools, permissions, sandbox, traces', color: colors.harness, y: 0.08 },
    { title: 'Loop Engineering', description: 'Trigger, verify, persist, decide, repeat', color: colors.loop, y: 0.9 },
  ];
  const layerMeshes = [];
  const layerLabels = [];

  layerSpecs.forEach((spec, index) => {
    const layerMaterial = material(spec.color, index === 0 ? 0.5 : 0.44, {
      emissiveIntensity: index === 3 ? 0.16 : 0.06,
      roughness: 0.48,
      transparent: index === 3,
      opacity: index === 3 ? 0.82 : 1,
    });
    const slab = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.14, 1.48), layerMaterial);
    slab.position.y = spec.y;
    stack.add(slab);
    layerMeshes.push(slab);

    const connectorStart = new THREE.Vector3(0.2, spec.y, 0.04);
    const connectorEnd = new THREE.Vector3(0.58, spec.y, 0.04);
    root.add(cylinderBetween(connectorStart, connectorEnd, 0.009, basic(spec.color, 0.64)));
    const connectorDot = new THREE.Mesh(new THREE.SphereGeometry(0.045, 12, 8), basic(spec.color, 0.9));
    connectorDot.position.copy(connectorEnd);
    root.add(connectorDot);

    const label = makeLayerLabel(spec.title, spec.description, spec.color);
    label.position.set(2.35, spec.y + 0.04, 0.12);
    root.add(label);
    layerLabels.push(label);
  });

  const promptCard = new THREE.Group();
  const promptBody = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.06, 0.62), material(colors.prompt, 0.64, { roughness: 0.58 }));
  const promptHeader = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.012, 0.07), basic(colors.loop, 0.88));
  promptHeader.position.set(0, 0.042, 0.16);
  const promptLine = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.012, 0.055), basic(0x8fa0b7, 0.72));
  promptLine.position.set(-0.08, 0.043, -0.04);
  promptCard.add(promptBody, promptHeader, promptLine);
  promptCard.position.set(0, -1.18, 0.02);
  stack.add(promptCard);

  const contextCards = [-0.65, 0, 0.65].map((x, index) => {
    const card = new THREE.Mesh(
      new THREE.BoxGeometry(0.43, 0.08, 0.36),
      material([colors.context, colors.loop, colors.violet][index], 0.48, { emissiveIntensity: 0.12 }),
    );
    card.position.set(x, -0.48 + (index === 1 ? 0.05 : 0), 0.02);
    card.userData.baseY = card.position.y;
    stack.add(card);
    return card;
  });

  const harnessFrame = new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.BoxGeometry(1.52, 0.66, 0.92)),
    new THREE.LineBasicMaterial({ color: colors.harness, transparent: true, opacity: 0.62 }),
  );
  harnessFrame.position.y = 0.32;
  stack.add(harnessFrame);

  const agent = new THREE.Group();
  const agentMaterial = material(colors.loop, 0.28, { emissiveIntensity: 0.3, roughness: 0.24 });
  const agentBody = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.2, 0.34, 20), agentMaterial);
  const agentHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 24, 16), agentMaterial);
  agentHead.position.y = 0.31;
  const agentVisor = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.05, 0.05), basic(colors.prompt, 0.9));
  agentVisor.position.set(0, 0.32, 0.16);
  const agentCore = new THREE.Mesh(
    new THREE.SphereGeometry(0.06, 16, 10),
    material(colors.context, 0.08, { emissiveIntensity: 0.78, roughness: 0.18 }),
  );
  agentCore.position.set(0, 0, 0.2);
  agent.add(agentBody, agentHead, agentVisor, agentCore);
  agent.position.set(0, 0.18, 0.08);
  stack.add(agent);

  const toolNodes = [-0.58, 0.58].map((x, index) => {
    const node = new THREE.Mesh(
      index === 0 ? new THREE.BoxGeometry(0.16, 0.16, 0.16) : new THREE.IcosahedronGeometry(0.11, 1),
      material(index === 0 ? colors.harness : colors.evidence, 0.32, { emissiveIntensity: 0.28 }),
    );
    node.position.set(x, 0.25, 0.08);
    node.userData.baseY = node.position.y;
    stack.add(node);
    stack.add(cylinderBetween(
      new THREE.Vector3(0, 0.18, 0.08),
      node.position,
      0.01,
      basic(index === 0 ? colors.harness : colors.evidence, 0.62),
    ));
    return node;
  });

  const loopRing = new THREE.Mesh(
    new THREE.TorusGeometry(1.05, 0.035, 10, lowPower ? 54 : 88),
    new THREE.MeshBasicMaterial({ color: colors.loop, transparent: true, opacity: 0.82, depthWrite: false }),
  );
  loopRing.rotation.x = Math.PI / 2;
  loopRing.position.y = 1.07;
  stack.add(loopRing);

  const checkpointColors = [colors.loop, colors.evidence, colors.violet, colors.human];
  const checkpoints = checkpointColors.map((hex, index) => {
    const angle = index * Math.PI / 2;
    const checkpoint = new THREE.Mesh(
      new THREE.SphereGeometry(0.095, 16, 10),
      material(hex, 0.24, { emissiveIntensity: 0.46, roughness: 0.22 }),
    );
    checkpoint.position.set(Math.cos(angle) * 1.05, 1.07, Math.sin(angle) * 1.05);
    stack.add(checkpoint);
    return checkpoint;
  });

  const loopToken = new THREE.Mesh(
    new THREE.OctahedronGeometry(0.105, 0),
    material(colors.loop, 0.16, { emissiveIntensity: 0.72, roughness: 0.16 }),
  );
  stack.add(loopToken);

  const runPulse = new THREE.Mesh(
    new THREE.SphereGeometry(0.055, 14, 10),
    basic(colors.context, 0.92),
  );
  stack.add(runPulse);

  const runLabel = makeMicroLabel('ONE AGENT RUN', colors.context, 1.35);
  runLabel.position.set(0, -1.67, 0.18);
  stack.add(runLabel);
  const loopLabel = makeMicroLabel('WORK OVER TIME', colors.loop, 1.35);
  loopLabel.position.set(0, 1.63, 0.18);
  stack.add(loopLabel);

  let frameCount = 0;
  let animationFrame = 0;
  let visible = true;
  let targetRotationX = 0;
  let targetRotationY = 0;
  const startedAt = performance.now();

  function render(time = 0) {
    const seconds = Math.max(0, time - startedAt) * 0.001;
    const loopAngle = reducedMotion.matches ? Math.PI * 0.2 : seconds * 0.5;
    loopToken.position.set(Math.cos(loopAngle) * 1.05, 1.07, Math.sin(loopAngle) * 1.05);
    loopToken.rotation.x = seconds * 0.6;
    loopToken.rotation.y = seconds * 0.8;

    const runPhase = reducedMotion.matches ? 0.55 : (seconds * 0.22) % 1;
    const runY = runPhase < 0.5
      ? -1.05 + runPhase * 2.5
      : 0.2 - (runPhase - 0.5) * 1.3;
    runPulse.position.set(
      reducedMotion.matches ? 0.28 : Math.sin(runPhase * Math.PI * 2) * 0.2,
      runY,
      0.3,
    );

    contextCards.forEach((card, index) => {
      card.position.y = card.userData.baseY + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.25 + index) * 0.025);
      card.rotation.y = reducedMotion.matches ? 0 : Math.sin(seconds * 0.7 + index) * 0.08;
    });
    toolNodes.forEach((node, index) => {
      node.position.y = node.userData.baseY + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.6 + index * 1.8) * 0.025);
      node.rotation.y = seconds * (index ? -0.34 : 0.34);
    });
    checkpoints.forEach((checkpoint, index) => {
      const pulse = reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 1.7 + index * 1.4) * 0.08;
      checkpoint.scale.setScalar(pulse);
    });
    agent.position.y = 0.18 + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.5) * 0.018);
    agentCore.scale.setScalar(reducedMotion.matches ? 1 : 1 + Math.sin(seconds * 2.3) * 0.1);
    promptCard.rotation.y = reducedMotion.matches ? 0 : Math.sin(seconds * 0.6) * 0.035;

    root.rotation.x += (targetRotationX - root.rotation.x) * 0.045;
    root.rotation.y += (targetRotationY - root.rotation.y) * 0.045;
    renderer.render(scene, camera);
    frameCount += 1;
    stackContainer.dataset.sceneFrames = String(frameCount);
    stackContainer.dataset.sceneReady = 'true';
  }

  function animate(time) {
    animationFrame = 0;
    if (!visible || document.hidden || reducedMotion.matches || !desktopStackMedia.matches) return;
    render(time);
    animationFrame = window.requestAnimationFrame(animate);
  }

  function startAnimation() {
    if (!animationFrame && visible && !document.hidden && !reducedMotion.matches && desktopStackMedia.matches) {
      animationFrame = window.requestAnimationFrame(animate);
    }
  }

  function stopAnimation() {
    if (!animationFrame) return;
    window.cancelAnimationFrame(animationFrame);
    animationFrame = 0;
  }

  function resize() {
    const width = Math.max(stackContainer.clientWidth, 1);
    const height = Math.max(stackContainer.clientHeight, 1);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, lowPower ? 1.25 : 1.55));
    renderer.setSize(width, height, false);
    const aspect = width / height;
    const viewHeight = 4.25;
    const viewWidth = viewHeight * aspect;
    camera.left = -viewWidth / 2;
    camera.right = viewWidth / 2;
    camera.top = viewHeight / 2;
    camera.bottom = -viewHeight / 2;
    camera.updateProjectionMatrix();
    render(performance.now());
  }

  function updatePointer(event) {
    const bounds = stackContainer.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width * 2 - 1;
    const y = (event.clientY - bounds.top) / bounds.height * 2 - 1;
    targetRotationY = x * 0.035;
    targetRotationX = -y * 0.018;
  }

  function resetPointer() {
    targetRotationX = 0;
    targetRotationY = 0;
  }

  if ('ResizeObserver' in window) {
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(stackContainer);
  } else {
    window.addEventListener('resize', resize, { passive: true });
  }

  if ('IntersectionObserver' in window) {
    const visibilityObserver = new IntersectionObserver((entries) => {
      visible = entries[0]?.isIntersecting ?? true;
      if (visible) startAnimation();
      else stopAnimation();
    }, { threshold: 0.02 });
    visibilityObserver.observe(stackContainer);
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

  stackContainer.addEventListener('pointermove', updatePointer, { passive: true });
  stackContainer.addEventListener('pointerleave', resetPointer, { passive: true });
  renderer.domElement.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    stopAnimation();
    stackContainer.dataset.sceneState = 'fallback';
  });

  window.__loopStackDiagnostics = () => {
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
      const distanceFromPaper = Math.abs(red - 244) + Math.abs(green - 247) + Math.abs(blue - 252);
      const luminance = red * 0.2126 + green * 0.7152 + blue * 0.0722;
      sampled += 1;
      if (distanceFromPaper > 24) painted += 1;
      minimumLuminance = Math.min(minimumLuminance, luminance);
      maximumLuminance = Math.max(maximumLuminance, luminance);
    }
    return {
      agentCore: true,
      contextSources: contextCards.length,
      drawCalls: renderer.info.render.calls,
      frameCount,
      harnessTools: toolNodes.length,
      height,
      layers: layerMeshes.length,
      loopCheckpoints: checkpoints.length,
      luminanceRange: maximumLuminance - minimumLuminance,
      painted,
      paintedRatio: sampled ? painted / sampled : 0,
      reducedMotion: reducedMotion.matches,
      sampled,
      triangles: renderer.info.render.triangles,
      width,
    };
  };

  window.__loopStackPause = () => {
    stopAnimation();
    render(performance.now());
    return window.__loopStackDiagnostics();
  };
  window.__loopStackResume = () => {
    startAnimation();
    return true;
  };

  resize();
  startAnimation();
}

initStackScene();
function handleDesktopStackChange(event) {
  if (!stackSceneInitialized) {
    initStackScene();
    return;
  }
  if (event.matches) window.__loopStackResume?.();
  else window.__loopStackPause?.();
}
if (desktopStackMedia.addEventListener) desktopStackMedia.addEventListener('change', handleDesktopStackChange);
else desktopStackMedia.addListener(handleDesktopStackChange);
