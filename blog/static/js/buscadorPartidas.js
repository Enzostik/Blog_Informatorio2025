function getCheckedList(parent) {
    const checkedBoxes = parent.querySelectorAll('input[type="checkbox"]:checked');

    return Array.from(checkedBoxes).map(checkbox => checkbox.value);
}

function updateUrl() {
    const qWord = document.getElementById('key-word').value;
    const orden = document.getElementById('order').value;
    const atributo = document.getElementById('attribute').value;
    const cantidad = document.getElementById('quantity').value;
    const categories = getCheckedList(document.getElementById('categories'));

    let search_command = `?q=${qWord}&qty=${cantidad}&ord=${orden}&attr=${atributo}`;

    if (categories.length > 0) {
        search_command = search_command + '&cat=' + categories.join('&cat=');
    };

    window.location.href = window.location.origin + window.location.pathname + search_command;
}

const urlParams = new URLSearchParams(window.location.search);
const currentPage = parseInt(urlParams.get('page')) || 1;
const pageButtons = document.querySelectorAll('#buttonPage');
const nextButton = document.getElementById('nextButton');
const prevButton = document.getElementById('prevButton');

function checkButtons() {
    let lastValue;
    pageButtons.forEach(button => {
        const buttonValue = Number(button.getAttribute('value')) || null;
        lastValue = buttonValue;
        if (buttonValue === currentPage){
            button.parentNode.classList.add('active');
            button.disabled = true;
            return;
        };
        button.addEventListener('click', function() {
            urlParams.set('page', buttonValue);
            window.location.search = urlParams.toString();
        });
    });
    if (currentPage === 1) {
        prevButton.parentNode.classList.add('disabled');
        prevButton.disabled = true;
    } else {
        prevButton.addEventListener('click', function() {
            urlParams.set('page', currentPage - 1);
            window.location.search = urlParams.toString();
        });
    };
    if (currentPage === lastValue) {
        nextButton.parentNode.classList.add('disabled');
        nextButton.disabled = true;
    } else {
        nextButton.addEventListener('click', function() {
            urlParams.set('page', currentPage + 1);
            window.location.search = urlParams.toString();
        });
    };
};

document.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        updateUrl();
    }
    console.log('ENTER');
});

checkButtons();