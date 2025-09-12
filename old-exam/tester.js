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
main.innerText = 'Test';

var rectangle = document.createElement('div');
rectangle.id = 'rectangle';
rectangle.style.backgroundColor = '#000000';
rectangle.style.position = 'fixed';
rectangle.style.top = '0px';
rectangle.style.left = '0px';
rectangle.style.width = '0px';
rectangle.style.height = '0px';

var x = document.createElement('input');
x.type = 'number';
x.value = '0';
x.placeholder = 'X';
x.style.width = '50px';
x.style.backgroundColor = '#362040';
x.style.border = '1px solid #e97fff';
x.style.color = '#df7fff';
x.style.cursor = 'pointer';
main.appendChild(x);

var y = document.createElement('input');
y.type = 'number';
y.value = '0';
y.placeholder = 'Y';
y.style.width = '50px';
y.style.backgroundColor = '#362040';
y.style.border = '1px solid #e97fff';
y.style.color = '#df7fff';
y.style.cursor = 'pointer';
main.appendChild(y);

var width = document.createElement('input');
width.type = 'number';
width.value = '0';
width.placeholder = 'Width';
width.style.width = '50px';
width.style.backgroundColor = '#362040';
width.style.border = '1px solid #e97fff';
width.style.color = '#df7fff';
width.style.cursor = 'pointer';
main.appendChild(width);

var height = document.createElement('input');
height.type = 'number';
height.value = '0';
height.placeholder = 'Height';
height.style.width = '50px';
height.style.backgroundColor = '#362040';
height.style.border = '1px solid #e97fff';
height.style.color = '#df7fff';
height.style.cursor = 'pointer';
main.appendChild(height);

function updateRectangle() {
    rectangle.style.top = y.value + 'px';
    rectangle.style.left = x.value + 'px';
    rectangle.style.width = width.value + 'px';
    rectangle.style.height = height.value + 'px';
}

x.onchange = updateRectangle;
y.onchange = updateRectangle;
width.onchange = updateRectangle;
height.onchange = updateRectangle;

document.body.appendChild(main);
document.body.appendChild(rectangle);
