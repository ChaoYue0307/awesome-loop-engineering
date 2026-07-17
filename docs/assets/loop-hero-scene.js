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
    line: 0xb8c4d6,
  };
  const palette = [
    colors.work,
    colors.orchestrator,
    colors.agent,
    colors.evidence,
    colors.state,
    colors.decision,
  ];
  const paper = new THREE.Color(0xf7f9fc);
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
    renderer.toneMappingExposure = 1;
    renderer.domElement.setAttribute('aria-hidden', 'true');
    renderer.domElement.dataset.loopSceneCanvas = 'true';
    container.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-6, 6, 2, -2, 0.1, 50);
    camera.position.set(0, 2.6, 10);
    camera.lookAt(0, 0, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0xc5d2e5, 2.4));
    const keyLight = new THREE.DirectionalLight(0xffffff, 3.1);
    keyLight.position.set(-4, 6, 8);
    scene.add(keyLight);
    const cyanLight = new THREE.PointLight(colors.work, 9, 12, 2);
    cyanLight.position.set(-2.3, 1.5, 4.5);
    scene.add(cyanLight);
    const greenLight = new THREE.PointLight(colors.evidence, 7, 10, 2);
    greenLight.position.set(2.2, 1.1, 4.2);
    scene.add(greenLight);

    const root = new THREE.Group();
    scene.add(root);

    function standardMaterial(hex, lighten = 0.48, options = {}) {
      const color = new THREE.Color(hex);
      const material = new THREE.MeshStandardMaterial({
        color: color.clone().lerp(white, Math.min(lighten, 0.64)),
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
      new THREE.Vector3(-4.55, 0, 0.06),
      new THREE.Vector3(-2.72, 0, 0),
      new THREE.Vector3(-0.7, 0, 0.06),
      new THREE.Vector3(1.42, 0, 0),
      new THREE.Vector3(3.2, 0, 0.06),
      new THREE.Vector3(4.72, 0, 0),
    ];
    const compactStagePositions = [
      new THREE.Vector3(-1.86, 0.94, 0.04),
      new THREE.Vector3(0, 0.94, 0),
      new THREE.Vector3(1.86, 0.94, 0.04),
      new THREE.Vector3(1.86, -1.02, 0),
      new THREE.Vector3(0, -1.02, 0.04),
      new THREE.Vector3(-1.86, -1.02, 0),
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
          new THREE.Vector3(-2.36, -1.04, -0.5),
          new THREE.Vector3(-2.36, 0.94, -0.5),
          end,
        ]
        : [
          start,
          new THREE.Vector3(3.55, 1.12, -0.62),
          new THREE.Vector3(0, 1.3, -0.72),
          new THREE.Vector3(-3.5, 1.12, -0.62),
          end,
        ];
      return new THREE.CatmullRomCurve3(controls, false, 'centripetal', 0.42);
    }

    let compactLayout = false;
    let mainCurve = buildMainCurve();
    let retryCurve = buildRetryCurve(false);
    const mainTube = addTube(mainCurve, 0.026, colors.orchestrator, 0.78, 180);
    const mainGlow = addTube(mainCurve, 0.072, colors.work, 0.08, 160);
    const retryLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(retryCurve.getPoints(lowPower ? 90 : 160)),
      new THREE.LineDashedMaterial({
        color: colors.retry,
        transparent: true,
        opacity: 0.58,
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

      const baseMaterial = standardMaterial(hex, 0.62, { roughness: 0.58, emissiveIntensity: 0.025 });
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

    const intake = createStation(0, 'WORK QUEUE', colors.work);
    const queueCards = [];
    for (let index = 0; index < 3; index += 1) {
      const card = new THREE.Group();
      const bodyMaterial = track(intake, standardMaterial(colors.work, 0.8 - index * 0.08, {
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
    addMicroLabel(delegate.group, 'ROUTES SCOPE + ROLE', colors.orchestrator, new THREE.Vector3(-0.03, -0.68, 0.18), 0.98);

    const act = createStation(2, 'AGENT TEAM', colors.agent);
    const workspaceGeometry = new THREE.BoxGeometry(1.08, 0.72, 0.54);
    const workspace = new THREE.LineSegments(
      new THREE.EdgesGeometry(workspaceGeometry),
      new THREE.LineBasicMaterial({ color: colors.agent, transparent: true, opacity: 0.42 }),
    );
    workspace.position.y = 0.06;
    act.group.add(workspace);
    const workspaceFloor = new THREE.Mesh(
      new THREE.BoxGeometry(1.02, 0.035, 0.5),
      track(act, standardMaterial(colors.agent, 0.78, { transparent: true, opacity: 0.72, depthWrite: false })),
    );
    workspaceFloor.position.y = -0.29;
    act.group.add(workspaceFloor);
    const roleNames = ['PLAN', 'BUILD', 'REVIEW'];
    const roleColors = [colors.work, colors.agent, colors.evidence];
    const agentPods = roleNames.map((role, index) => {
      const pod = new THREE.Group();
      pod.userData.role = role;
      pod.position.set((index - 1) * 0.34, -0.04 + (index === 1 ? 0.04 : 0), 0.05);
      const material = track(act, standardMaterial(roleColors[index], 0.4, { emissiveIntensity: 0.18 }));
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.105, 0.13, 0.22, 16), material);
      body.position.y = 0.05;
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.11, 18, 12), material);
      head.position.y = 0.25;
      const visor = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.035, 0.035), basicMaterial(0x172033, 0.86));
      visor.position.set(0, 0.26, 0.1);
      const base = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.19, 0.035, 18), basicMaterial(roleColors[index], 0.42));
      base.position.y = -0.09;
      pod.add(body, head, visor, base);
      act.group.add(pod);
      return pod;
    });
    addMicroLabel(act.group, 'PLAN / BUILD / REVIEW', colors.agent, new THREE.Vector3(-0.04, -0.68, 0.2), 1.02);
    const contextChips = roleColors.map((hex, index) => {
      const chip = new THREE.Mesh(
        new THREE.BoxGeometry(0.17, 0.11, 0.035),
        track(act, standardMaterial(hex, 0.66, { emissiveIntensity: 0.12 })),
      );
      chip.position.set((index - 1) * 0.32, 0.56 + (index % 2) * 0.05, 0.02);
      act.group.add(chip);
      return chip;
    });

    const verify = createStation(3, 'EVIDENCE GATE', colors.evidence);
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

    const persist = createStation(4, 'STATE LEDGER', colors.state);
    const stateLayers = [0, 1, 2].map((index) => {
      const material = track(persist, standardMaterial(index === 1 ? colors.orchestrator : colors.state, 0.53, {
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
        track(persist, standardMaterial(colors.state, 0.78, { emissiveIntensity: 0.08 })),
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

    const decide = createStation(5, 'NEXT ACTION', colors.decision);
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
    const packetAuraMaterial = new THREE.MeshBasicMaterial({
      color: colors.work,
      transparent: true,
      opacity: 0.14,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const packetAura = new THREE.Mesh(new THREE.SphereGeometry(0.31, 16, 10), packetAuraMaterial);
    const packetGroup = new THREE.Group();
    packetGroup.add(packetAura, packetBody, packetHeader, packetLine, packetMarker);
    packetGroup.position.copy(mainCurve.getPointAt(0));
    packetGroup.position.z = 0.42;
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

      targetPacketPosition.z = 0.42;
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
        const scale = stationScale * (1 + (selected ? 0.075 : 0) + nearby * 0.025);
        state.group.scale.setScalar(scale);
        state.haloMaterial.opacity = selected ? 0.32 : 0.07 + nearby * 0.12;
        state.baseMaterial.emissiveIntensity = selected ? 0.14 : 0.025 + nearby * 0.05;
        state.materials.forEach((material) => {
          const base = material.userData.baseEmissiveIntensity || 0;
          material.emissiveIntensity = base + (selected ? 0.18 : nearby * 0.08);
        });
        state.title.material.opacity = selected ? 1 : 0.76;
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
      agentPods.forEach((pod, index) => {
        const working = reducedMotion.matches ? 0 : Math.sin(seconds * 1.8 + index * 1.6) * 0.025;
        pod.position.y = -0.04 + (index === 1 ? 0.04 : 0) + working;
      });
      contextChips.forEach((chip, index) => {
        chip.position.y = 0.56 + (index % 2) * 0.05 + (reducedMotion.matches ? 0 : Math.sin(seconds * 1.4 + index) * 0.04);
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
      replaceTubeGeometry(mainTube, mainCurve, 0.026, 180);
      replaceTubeGeometry(mainGlow, mainCurve, 0.072, 160);
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
      const tablet = !compact && width < 900;
      applyLayout(compact);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, compact || lowPower ? 1.3 : 1.65));
      renderer.setSize(width, height, false);

      const aspect = width / height;
      const viewHeight = compact
        ? Math.max(3.45, 5.8 / aspect)
        : tablet
          ? 11.2 / aspect
          : 3.15;
      const viewWidth = viewHeight * aspect;
      camera.left = -viewWidth / 2;
      camera.right = viewWidth / 2;
      camera.top = viewHeight / 2;
      camera.bottom = -viewHeight / 2;
      camera.position.set(0, compact ? 2.05 : 2.6, 10);
      camera.lookAt(0, compact ? -0.05 : 0, 0);
      camera.updateProjectionMatrix();

      stationScale = compact ? 0.93 : tablet ? 0.92 : 1.04;
      packetGroup.scale.setScalar(compact ? 1.08 : 1);
      stationLabels.forEach((label) => { label.visible = width >= 760; });
      numberLabels.forEach((label) => { label.visible = width < 760; });
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
        const distanceFromPaper = Math.abs(red - 247) + Math.abs(green - 249) + Math.abs(blue - 252);
        const luminance = red * 0.2126 + green * 0.7152 + blue * 0.0722;
        sampled += 1;
        if (distanceFromPaper > 24) painted += 1;
        minimumLuminance = Math.min(minimumLuminance, luminance);
        maximumLuminance = Math.max(maximumLuminance, luminance);
      }
      return {
        activeStage,
        agentRoles: roleNames.length,
        compactLayout,
        drawCalls: renderer.info.render.calls,
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
