var main = document.createElement('div');
main.id = 'mainhack';
main.style.backgroundColor = '#120f13';
main.style.border = '10px solid #e97fff 5px';
main.style.position = 'fixed';
main.style.top = '10px';
main.style.right = '10px';
main.style.padding = '5px';
main.style.width = '200px';
main.style.color = '#df7fff';
main.style.textAlign = 'center';
main.innerText = 'Dino Hack';

var noclip = document.createElement('div');
noclip.id = 'noclip';
noclip.innerText = 'Noclip: Disabled';
noclip.style.color = '#ff8888';
noclip.style.cursor = 'pointer';
noclip.onclick = function() {
    if (noclip.innerText == 'Noclip: Disabled') {
        var original = Runner.prototype.gameOver;
        Runner.prototype.gameOver = function() {};
        noclip.innerText = 'Noclip: Enabled';
        noclip.style.color = '#88ff88';
    } else {
        Runner.prototype.gameOver = original;
        noclip.innerText = 'Noclip: Disabled';
        noclip.style.color = '#ff8888';
    };
};
main.appendChild(noclip);

var auto = document.createElement('div');
auto.id = 'auto';
auto.innerText = 'Auto: Disabled';
auto.style.color = '#ff8888';
auto.style.cursor = 'pointer';
auto.onclick = function() {
    if (auto.innerText == 'Auto: Disabled') {
        auto.innerText = 'Auto: Enabled';
        auto.style.color = '#88ff88';
    } else {
        auto.innerText = 'Auto: Disabled';
        auto.style.color = '#ff8888';
    };
};
setInterval(() => {
    if (auto.innerText == 'Auto: Enabled') {
        autoplay();
    }
}, Runner.instance_.msPerFrame);
main.appendChild(auto);

var xspeed = document.createElement('div');
xspeed.id = 'xspeed';
xspeed.innerText = 'Walk Speed: ';
xspeed.style.color = '#df7fff';
xspeed.style.display = 'inline-block';
xspeed.style.cursor = 'pointer';

var xspeed_textbox = document.createElement('input');
xspeed_textbox.id = 'xspeed_textbox';
xspeed_textbox.type = 'number';
xspeed_textbox.value = '10';
xspeed_textbox.placeholder = '10';
xspeed_textbox.style.width = '50px';
xspeed_textbox.style.backgroundColor = '#362040';
xspeed_textbox.style.border = '1px solid #e97fff';
xspeed_textbox.style.color = '#df7fff';
xspeed_textbox.style.cursor = 'pointer';
xspeed_textbox.onchange = function() {
    Runner.instance_.setSpeed(parseInt(xspeed_textbox.value));
};
xspeed.appendChild(xspeed_textbox);
main.appendChild(xspeed);

var yspeed = document.createElement('div');
yspeed.id = 'yspeed';
yspeed.innerText = 'Jump Speed: ';
yspeed.style.color = '#df7fff';
yspeed.style.display = 'inline-block';
yspeed.style.cursor = 'pointer';

var yspeed_textbox = document.createElement('input');
yspeed_textbox.id = 'yspeed_textbox';
yspeed_textbox.type = 'number';
yspeed_textbox.value = '10';
yspeed_textbox.placeholder = '10';
yspeed_textbox.style.width = '50px';
yspeed_textbox.style.backgroundColor = '#362040';
yspeed_textbox.style.border = '1px solid #e97fff';
yspeed_textbox.style.color = '#df7fff';
yspeed_textbox.style.cursor = 'pointer';
yspeed_textbox.onchange = function() {
    Runner.instance_.tRex.setJumpVelocity(parseInt(yspeed_textbox.value));
};
yspeed.appendChild(yspeed_textbox);
main.appendChild(yspeed);

var ground = document.createElement('div');
ground.id = 'ground';
ground.innerText = 'Ground Y: ';
ground.style.color = '#df7fff';
ground.style.display = 'inline-block';
ground.style.cursor = 'pointer';
ground.onclick = function() {
    Runner.instance_.tRex.groundYPos = parseInt(ground_textbox.value);
};

var ground_textbox = document.createElement('input');
ground_textbox.id = 'ground_textbox';
ground_textbox.type = 'number';
ground_textbox.value = '0';
ground_textbox.placeholder = '0';
ground_textbox.style.width = '50px';
ground_textbox.style.backgroundColor = '#362040';
ground_textbox.style.border = '1px solid #e97fff';
ground_textbox.style.color = '#df7fff';
ground_textbox.style.cursor = 'pointer';
ground.appendChild(ground_textbox);
main.appendChild(ground);

var pos = document.createElement('div');
pos.id = 'pos';
pos.innerText = 'XPosition: ';
pos.style.color = '#df7fff';
pos.style.display = 'inline-block';
pos.style.cursor = 'pointer';
pos.onclick = function() {
    Runner.instance_.tRex.xPos = parseInt(xpos_textbox.value);
};

var xpos_textbox = document.createElement('input');
xpos_textbox.id = 'xpos_textbox';
xpos_textbox.type = 'number';
xpos_textbox.value = '0';
xpos_textbox.placeholder = '0';
xpos_textbox.style.width = '50px';
xpos_textbox.style.backgroundColor = '#362040';
xpos_textbox.style.border = '1px solid #e97fff';
xpos_textbox.style.color = '#df7fff';
xpos_textbox.style.cursor = 'pointer';
pos.appendChild(xpos_textbox);
main.appendChild(pos);

var score = document.createElement('div');
score.id = 'score';
score.innerText = 'Set Score: ';
score.style.color = '#df7fff';
score.style.display = 'inline-block';
score.style.cursor = 'pointer';
score.onclick = function() {
    Runner.instance_.distanceRan = parseInt(score_textbox.value) / Runner.instance_.distanceMeter.config.COEFFICIENT
};

var score_textbox = document.createElement('input');
score_textbox.id = 'score_textbox';
score_textbox.type = 'number';
score_textbox.value = '0';
score_textbox.placeholder = '0';
score_textbox.style.width = '50px';
score_textbox.style.backgroundColor = '#362040';
score_textbox.style.border = '1px solid #e97fff';
score_textbox.style.color = '#df7fff';
score_textbox.style.cursor = 'pointer';
score.appendChild(score_textbox);
main.appendChild(score);

var credits = document.createElement('div');
credits.id = 'credits';
credits.innerText = 'Made by Pisc639';
credits.style.color = '#ffffff';
credits.style.display = 'inline-block';
credits.style.cursor = 'pointer';
main.appendChild(credits);

document.body.appendChild(main);
