import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Snake Game", page_icon="🐍", layout="centered")

st.title("🐍 BSnake Game")
st.write("Use the arrow keys to play. This is a simple test app you can run from Streamlit.")

snake_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    margin: 0;
    display: flex;
    justify-content: center;
    background: #111;
    color: white;
    font-family: Arial, sans-serif;
  }
  #wrap {
    text-align: center;
  }
  canvas {
    background: #000;
    border: 3px solid #4CAF50;
    margin-top: 10px;
  }
  button {
    margin: 8px;
    padding: 8px 14px;
    font-size: 16px;
    cursor: pointer;
  }
</style>
</head>
<body>
<div id="wrap">
  <h2>Snake</h2>
  <div>Score: <span id="score">0</span></div>
  <button onclick="restartGame()">Restart</button>
  <br>
  <canvas id="game" width="400" height="400"></canvas>
  <p>Click inside the game area, then use arrow keys.</p>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");

const box = 20;
const rows = canvas.height / box;
const cols = canvas.width / box;

let snake;
let direction;
let nextDirection;
let food;
let score;
let gameOver;
let gameLoop;

function initGame() {
  snake = [{x: 10, y: 10}];
  direction = {x: 1, y: 0};
  nextDirection = direction;
  food = randomFood();
  score = 0;
  gameOver = false;
  scoreEl.textContent = score;
}

function randomFood() {
  let newFood;
  do {
    newFood = {
      x: Math.floor(Math.random() * cols),
      y: Math.floor(Math.random() * rows)
    };
  } while (snake && snake.some(part => part.x === newFood.x && part.y === newFood.y));
  return newFood;
}

function restartGame() {
  clearInterval(gameLoop);
  initGame();
  gameLoop = setInterval(update, 120);
}

document.addEventListener("keydown", function(event) {
  if (event.key === "ArrowUp" && direction.y !== 1) {
    nextDirection = {x: 0, y: -1};
  } else if (event.key === "ArrowDown" && direction.y !== -1) {
    nextDirection = {x: 0, y: 1};
  } else if (event.key === "ArrowLeft" && direction.x !== 1) {
    nextDirection = {x: -1, y: 0};
  } else if (event.key === "ArrowRight" && direction.x !== -1) {
    nextDirection = {x: 1, y: 0};
  }
});

function update() {
  if (gameOver) {
    draw();
    return;
  }

  direction = nextDirection;

  const head = {
    x: snake[0].x + direction.x,
    y: snake[0].y + direction.y
  };

  if (
    head.x < 0 || head.x >= cols ||
    head.y < 0 || head.y >= rows ||
    snake.some(part => part.x === head.x && part.y === head.y)
  ) {
    gameOver = true;
    draw();
    return;
  }

  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 1;
    scoreEl.textContent = score;
    food = randomFood();
  } else {
    snake.pop();
  }

  draw();
}

function draw() {
  ctx.fillStyle = "#000";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#4CAF50";
  snake.forEach(part => {
    ctx.fillRect(part.x * box, part.y * box, box - 1, box - 1);
  });

  ctx.fillStyle = "#FF5252";
  ctx.fillRect(food.x * box, food.y * box, box - 1, box - 1);

  if (gameOver) {
    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "white";
    ctx.font = "32px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Game Over", canvas.width / 2, canvas.height / 2 - 10);
    ctx.font = "18px Arial";
    ctx.fillText("Press Restart", canvas.width / 2, canvas.height / 2 + 25);
  }
}

restartGame();
</script>
</body>
</html>
"""

components.html(snake_html, height=560)
