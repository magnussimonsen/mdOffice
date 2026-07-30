document.addEventListener('DOMContentLoaded', () => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const minSpeed = 100; // px per second
  const maxSpeed = 800; // px per second
  const maxBallSpeed = 1000; // px per second cap for ball-like emojis
  const defaultMass = 1;
  const gravityConstant = 25000000; // tuned for screen-space inverse-square pull
  const gravityMinDistance = 44; // softening floor to avoid singularity at close range
  const maxGravityAccel = 1400; // cap to keep motion stable near the star
  const lifespan = 60000; // ms an animal wanders before fading out
  const collisionDistance = 54; // px between centers to count as a crash
  const maxBalls = 1; // bump for testing multiple balls at once
  const maxGoals = 1; // bump for testing multiple goals at once
  const goalEntryConeDegrees = 145; // how wide a window, centered on straight up, counts as "from below"

  const EMOJI = {
    ball: '⚽',
    goal: '🥅',
    trophy: '🏆',
    star: '⭐',
    coffee: '☕',
    diamond: '💎',
  };
  const supportSpecials = new Set([EMOJI.star, EMOJI.coffee, EMOJI.diamond]);
  const isSupportPage = window.location.pathname.endsWith('/support.html') || window.location.pathname.endsWith('support.html');

  const active = [];
  let looping = false;
  const goalsKey = 'kittenGlobalGoals';
  const windowNameToken = '__mdofficeGoals=';
  const scoreEls = document.querySelectorAll('#kitten-score');
  const supportButtons = document.querySelectorAll('nav .menu a.cta');
  const logoButtons = document.querySelectorAll('nav a.logo');

  function toSafeGoalCount(value) {
    const parsed = parseInt(String(value ?? ''), 10);
    return Number.isFinite(parsed) && parsed >= 0 ? parsed : 0;
  }

  function readWindowNameGoals() {
    const name = String(window.name || '');
    const parts = name.split(';');
    for (const part of parts) {
      const trimmed = part.trim();
      if (trimmed.startsWith(windowNameToken)) {
        return toSafeGoalCount(trimmed.slice(windowNameToken.length));
      }
    }
    return 0;
  }

  function writeWindowNameGoals(value) {
    const safeValue = String(toSafeGoalCount(value));
    const name = String(window.name || '');
    const parts = name
      .split(';')
      .map((part) => part.trim())
      .filter((part) => part && !part.startsWith(windowNameToken));
    parts.push(`${windowNameToken}${safeValue}`);
    window.name = parts.join('; ');
  }

  function readGoals() {
    const fromWindowName = readWindowNameGoals();
    try {
      const fromLocalStorage = toSafeGoalCount(localStorage.getItem(goalsKey));
      return Math.max(fromLocalStorage, fromWindowName);
    } catch {
      return fromWindowName;
    }
  }

  function persistGoals() {
    writeWindowNameGoals(goals);
    try {
      localStorage.setItem(goalsKey, String(goals));
    } catch {
      // Ignore storage failures (private mode, blocked storage, etc.)
    }
  }

  let goals = readGoals();

  function normalizeEmoji(value) {
    return String(value || '').replace(/[\uFE0E\uFE0F]/g, '');
  }

  function renderScore() {
    const text = `${EMOJI.trophy} ${goals}`;
    scoreEls.forEach((el) => { el.textContent = text; });
  }

  function isAlive(animal) {
    return !animal.dead && !animal.fading;
  }

  function countActiveRole(role) {
    return active.reduce((count, animal) => (isAlive(animal) && animal.role === role ? count + 1 : count), 0);
  }

  function hasActiveEmoji(emoji) {
    return active.some((animal) => isAlive(animal) && normalizeEmoji(animal.emoji) === normalizeEmoji(emoji));
  }

  function isBallLike(animal) {
    return animal.role === 'ball' || (isSupportPage && animal.role === 'special');
  }

  function isCoffee(animal) {
    return normalizeEmoji(animal.emoji) === EMOJI.coffee;
  }

  function explode(x, y, emoji) {
    const boom = document.createElement('span');
    boom.className = 'kitten kitten-boom';
    boom.textContent = emoji;
    boom.style.left = `${x}px`;
    boom.style.top = `${y}px`;
    document.body.appendChild(boom);
    boom.addEventListener('animationend', () => boom.remove());
  }

  function spawnEntity(rect, emoji, role) {
    if (role === 'ball' && countActiveRole('ball') >= maxBalls) return;
    if (role === 'goal' && countActiveRole('goal') >= maxGoals) return;
    if (role === 'special' && hasActiveEmoji(emoji)) return;

    const el = document.createElement('span');
    el.className = 'kitten';
    el.textContent = emoji;
    document.body.appendChild(el);

    const now = performance.now();
    const entity = {
      el,
      emoji,
      role,
      mass: defaultMass,
      x: rect.left + Math.random() * rect.width,
      y: rect.bottom + Math.random() * 10,
      angle: Math.random() * Math.PI * 2,
      speed: minSpeed + Math.random() * (maxSpeed - minSpeed),
      start: now,
      lastFrame: now,
      dead: false,
      fading: false,
    };
    el.style.left = `${entity.x}px`;
    el.style.top = `${entity.y}px`;

    active.push(entity);
    startLoop();
  }

  function removeEntity(entity) {
    entity.dead = true;
    entity.el.remove();
  }

  function fadeOut(entity) {
    entity.fading = true;
    entity.el.style.transition = 'opacity 400ms ease';
    entity.el.style.opacity = '0';
    entity.el.addEventListener('transitionend', () => removeEntity(entity));
  }

  function bounceOff(a, b) {
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const dist = Math.hypot(dx, dy) || 1;
    const nx = dx / dist;
    const ny = dy / dist;
    const away = Math.atan2(ny, nx);
    a.angle = away + Math.PI;
    b.angle = away;

    // nudge apart so they don't immediately re-trigger the same collision
    const overlap = collisionDistance - dist;
    if (overlap > 0) {
      a.x -= (nx * overlap) / 2;
      a.y -= (ny * overlap) / 2;
      b.x += (nx * overlap) / 2;
      b.y += (ny * overlap) / 2;
    }
  }

  function boostBallSpeed(animal) {
    animal.speed = Math.min(animal.speed + 180, maxSpeed, maxBallSpeed);
  }

  function clampEntitySpeed(entity) {
    const speedCap = isBallLike(entity) ? Math.min(maxSpeed, maxBallSpeed) : maxSpeed;
    if (entity.speed > speedCap) entity.speed = speedCap;
  }

  function getCoffeeGravityAccel(entity) {
    let ax = 0;
    let ay = 0;

    for (const source of active) {
      if (!isAlive(source)) continue;
      if (source === entity) continue;
      if (!isCoffee(source)) continue;

      const dx = source.x - entity.x;
      const dy = source.y - entity.y;
      const distance = Math.hypot(dx, dy);
      if (!Number.isFinite(distance) || distance === 0) continue;

      // Inverse-square force where both masses are currently 1.
      const clampedDistance = Math.max(distance, gravityMinDistance);
      const force = (gravityConstant * entity.mass * source.mass) / (clampedDistance * clampedDistance);
      const accel = Math.min(force / entity.mass, maxGravityAccel);

      ax += (dx / distance) * accel;
      ay += (dy / distance) * accel;
    }

    return { ax, ay };
  }

  // A goal only counts if, at contact, the ball is positioned below the net
  // (y grows downward on screen, so larger y = below) and its velocity
  // relative to the net's points up within goalEntryConeDegrees of straight
  // up. At 180 degrees that's any upward angle; narrower values demand a
  // more head-on approach.
  function isGoalFromBelow(ball, goal) {
    if (ball.y <= goal.y) return false;

    const relVx = Math.cos(ball.angle) * ball.speed - Math.cos(goal.angle) * goal.speed;
    const relVy = Math.sin(ball.angle) * ball.speed - Math.sin(goal.angle) * goal.speed;
    if (relVx === 0 && relVy === 0) return false;

    const approachAngle = Math.atan2(relVy, relVx);
    const straightUp = -Math.PI / 2;
    let angleFromUp = Math.abs(approachAngle - straightUp);
    if (angleFromUp > Math.PI) angleFromUp = 2 * Math.PI - angleFromUp;

    const halfCone = (goalEntryConeDegrees * Math.PI) / 360;
    return angleFromUp <= halfCone;
  }

  function updateEntity(entity, now) {
    const dt = Math.min(now - entity.lastFrame, 50) / 1000;
    entity.lastFrame = now;

    let vx = Math.cos(entity.angle) * entity.speed;
    let vy = Math.sin(entity.angle) * entity.speed;

    // Only coffee creates gravity; non-coffee entities are pulled toward it.
    if (!isCoffee(entity)) {
      const { ax, ay } = getCoffeeGravityAccel(entity);
      vx += ax * dt;
      vy += ay * dt;
      entity.angle = Math.atan2(vy, vx);
      entity.speed = Math.hypot(vx, vy);
    }

    clampEntitySpeed(entity);

    entity.x += Math.cos(entity.angle) * entity.speed * dt;
    entity.y += Math.sin(entity.angle) * entity.speed * dt;

    const maxX = window.innerWidth - entity.el.offsetWidth;
    const maxY = window.innerHeight - entity.el.offsetHeight;
    if (entity.x < 0) { entity.x = 0; entity.angle = Math.PI - entity.angle; }
    if (entity.x > maxX) { entity.x = maxX; entity.angle = Math.PI - entity.angle; }
    if (entity.y < 0) { entity.y = 0; entity.angle = -entity.angle; }
    if (entity.y > maxY) { entity.y = maxY; entity.angle = -entity.angle; }

    entity.el.style.left = `${entity.x}px`;
    entity.el.style.top = `${entity.y}px`;
  }

  function checkCollisions() {
    for (let i = 0; i < active.length; i++) {
      const a = active[i];
      if (!isAlive(a)) continue;
      for (let j = i + 1; j < active.length; j++) {
        const b = active[j];
        if (!isAlive(b)) continue;

        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const distance = Math.hypot(dx, dy);
        if (distance >= collisionDistance) continue;

        const ball = a.role === 'ball' ? a : b.role === 'ball' ? b : null;
        const goal = a.role === 'goal' ? a : b.role === 'goal' ? b : null;

        if (ball && goal) {
          if (isGoalFromBelow(ball, goal)) {
            goals += 1;
            persistGoals();
            renderScore();
            explode((a.x + b.x) / 2, (a.y + b.y) / 2, EMOJI.trophy);
            removeEntity(a);
            removeEntity(b);
          } else {
            bounceOff(a, b);
            clampEntitySpeed(a);
            clampEntitySpeed(b);
          }
          continue;
        }

        const aBallLike = isBallLike(a);
        const bBallLike = isBallLike(b);
        const aIsSpecial = a.role === 'special';
        const bIsSpecial = b.role === 'special';
        if (isSupportPage && ((aBallLike && bIsSpecial) || (bBallLike && aIsSpecial))) {
          if (aBallLike) boostBallSpeed(a);
          if (bBallLike) boostBallSpeed(b);
        }

        bounceOff(a, b);
        clampEntitySpeed(a);
        clampEntitySpeed(b);
      }
    }
  }

  function frame(now) {
    for (const entity of active) {
      if (!isAlive(entity)) continue;
      updateEntity(entity, now);
      if (now - entity.start > lifespan) {
        fadeOut(entity);
      }
    }

    checkCollisions();

    for (let i = active.length - 1; i >= 0; i--) {
      if (active[i].dead) active.splice(i, 1);
    }

    if (active.length > 0) {
      requestAnimationFrame(frame);
    } else {
      looping = false;
    }
  }

  function startLoop() {
    if (!looping) {
      looping = true;
      requestAnimationFrame(frame);
    }
  }

  renderScore();

  window.addEventListener('storage', (event) => {
    if (event.key === goalsKey || event.key === null) {
      goals = readGoals();
      renderScore();
    }
  });

  supportButtons.forEach((btn) => {
    btn.addEventListener('mouseenter', () => {
      spawnEntity(btn.getBoundingClientRect(), EMOJI.ball, 'ball');
    });
  });

  logoButtons.forEach((btn) => {
    btn.addEventListener('mouseenter', () => {
      spawnEntity(btn.getBoundingClientRect(), EMOJI.goal, 'goal');
    });
  });

  document.querySelectorAll('[data-kitten-emoji]').forEach((btn) => {
    btn.addEventListener('mouseenter', () => {
      if (!isSupportPage) return;
      const emoji = normalizeEmoji(btn.dataset.kittenEmoji);
      if (!supportSpecials.has(emoji)) return;
      spawnEntity(btn.getBoundingClientRect(), emoji, 'special');
    });
  });
});
