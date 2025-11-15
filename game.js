// 获取DOM元素
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const restartBtn = document.getElementById('restart-btn');
const currentScoreElement = document.getElementById('current-score');
const highScoreElement = document.getElementById('high-score');
const gameOverElement = document.getElementById('game-over');

// 游戏配置
const GRID_SIZE = 20;
const TILE_COUNT = canvas.width / GRID_SIZE;

// 游戏状态
let snake = [];
let food = {};
let dx = 0;
let dy = 0;
let score = 0;
let highScore = localStorage.getItem('snakeHighScore') || 0;
let gameLoop = null;
let gameStarted = false;
let gamePaused = false;
let gameSpeed = 120; // 初始速度 (版本2调整)

// 初始化游戏
function initGame() {
    snake = [
        { x: 10, y: 10 },
        { x: 9, y: 10 },
        { x: 8, y: 10 }
    ];
    dx = 1;
    dy = 0;
    score = 0;
    currentScoreElement.textContent = score;
    highScoreElement.textContent = highScore;
    gameOverElement.style.display = 'none';
    generateFood();
}

// 生成食物
function generateFood() {
    food = {
        x: Math.floor(Math.random() * TILE_COUNT),
        y: Math.floor(Math.random() * TILE_COUNT)
    };

    // 确保食物不在蛇身上
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            generateFood();
            return;
        }
    }
}

// 绘制游戏
function draw() {
    // 清空画布
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 绘制网格
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= TILE_COUNT; i++) {
        ctx.beginPath();
        ctx.moveTo(i * GRID_SIZE, 0);
        ctx.lineTo(i * GRID_SIZE, canvas.height);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, i * GRID_SIZE);
        ctx.lineTo(canvas.width, i * GRID_SIZE);
        ctx.stroke();
    }

    // 绘制蛇
    snake.forEach((segment, index) => {
        if (index === 0) {
            // 蛇头 - 版本2改为蓝色
            ctx.fillStyle = '#2196F3';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#2196F3';
        } else {
            // 蛇身 - 版本2改为浅蓝色
            ctx.fillStyle = '#64B5F6';
            ctx.shadowBlur = 5;
            ctx.shadowColor = '#64B5F6';
        }

        ctx.fillRect(
            segment.x * GRID_SIZE + 1,
            segment.y * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        );

        // 添加圆角效果 - 版本2蓝色边框
        ctx.strokeStyle = index === 0 ? '#1976D2' : '#42A5F5';
        ctx.lineWidth = 2;
        ctx.strokeRect(
            segment.x * GRID_SIZE + 1,
            segment.y * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        );
    });

    // 重置阴影
    ctx.shadowBlur = 0;

    // 绘制食物 - 版本2改为金黄色
    ctx.fillStyle = '#FFC107';
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#FFC107';
    ctx.beginPath();
    ctx.arc(
        food.x * GRID_SIZE + GRID_SIZE / 2,
        food.y * GRID_SIZE + GRID_SIZE / 2,
        GRID_SIZE / 2 - 2,
        0,
        Math.PI * 2
    );
    ctx.fill();

    ctx.shadowBlur = 0;
}

// 更新游戏状态
function update() {
    if (gamePaused) return;

    // 计算新的蛇头位置
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };

    // 检查碰撞 - 墙壁
    if (head.x < 0 || head.x >= TILE_COUNT || head.y < 0 || head.y >= TILE_COUNT) {
        endGame();
        return;
    }

    // 检查碰撞 - 自己
    for (let segment of snake) {
        if (head.x === segment.x && head.y === segment.y) {
            endGame();
            return;
        }
    }

    // 添加新头部
    snake.unshift(head);

    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        currentScoreElement.textContent = score;

        // 更新最高分
        if (score > highScore) {
            highScore = score;
            highScoreElement.textContent = highScore;
            localStorage.setItem('snakeHighScore', highScore);
        }

        generateFood();

        // 加速游戏 (版本2调整加速度)
        if (gameSpeed > 70) {
            gameSpeed -= 2; // 每次加速减少2ms
            clearInterval(gameLoop);
            gameLoop = setInterval(gameUpdate, gameSpeed);
        }
    } else {
        // 移除尾部
        snake.pop();
    }

    draw();
}

// 游戏更新循环
function gameUpdate() {
    update();
}

// 开始游戏
function startGame() {
    if (!gameStarted) {
        gameStarted = true;
        gamePaused = false;
        initGame();
        gameLoop = setInterval(gameUpdate, gameSpeed);
        startBtn.textContent = '游戏中...';
        pauseBtn.disabled = false;
    }
}

// 暂停游戏
function togglePause() {
    if (!gameStarted) return;

    gamePaused = !gamePaused;
    pauseBtn.textContent = gamePaused ? '继续' : '暂停';
}

// 重新开始
function restartGame() {
    clearInterval(gameLoop);
    gameStarted = false;
    gamePaused = false;
    gameSpeed = 120; // 重置为初始速度
    startBtn.textContent = '开始游戏';
    pauseBtn.textContent = '暂停';
    pauseBtn.disabled = true;
    initGame();
    draw();
}

// 结束游戏
function endGame() {
    clearInterval(gameLoop);
    gameStarted = false;
    gameOverElement.style.display = 'block';
    startBtn.textContent = '开始游戏';
    pauseBtn.disabled = true;
}

// 键盘控制
document.addEventListener('keydown', (e) => {
    if (!gameStarted) return;

    switch(e.key) {
        case 'ArrowUp':
            if (dy === 0) { dx = 0; dy = -1; }
            e.preventDefault();
            break;
        case 'ArrowDown':
            if (dy === 0) { dx = 0; dy = 1; }
            e.preventDefault();
            break;
        case 'ArrowLeft':
            if (dx === 0) { dx = -1; dy = 0; }
            e.preventDefault();
            break;
        case 'ArrowRight':
            if (dx === 0) { dx = 1; dy = 0; }
            e.preventDefault();
            break;
        case ' ':
            togglePause();
            e.preventDefault();
            break;
    }
});

// 按钮事件
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', togglePause);
restartBtn.addEventListener('click', restartGame);

// 初始化
initGame();
draw();
pauseBtn.disabled = true;
highScoreElement.textContent = highScore;
