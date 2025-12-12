function getCheckedList(parent) {
    const checkedBoxes = parent.querySelectorAll('input[type="checkbox"]:checked');

    return Array.from(checkedBoxes).map(checkbox => checkbox.value);
}


const qWord = document.getElementById('key-word');
const orden = document.getElementById('order');
const atributo = document.getElementById('attribute');
const cantidad = document.getElementById('quantity');
const categories = document.getElementById('categories');

function updateUrl() {
    let search_command = `?q=${qWord.value}&qty=${cantidad.value}&ord=${orden.value}&attr=${atributo.value}`;
    const categoriesValues = getCheckedList(categories);

    if (categoriesValues.length > 0) {
        search_command = search_command + '&cat=' + categoriesValues.join('&cat=');
    };

    window.location.href = window.location.origin + window.location.pathname + search_command;
}

const urlParams = new URLSearchParams(window.location.search);
const pageButtons = document.querySelectorAll('#buttonPage')||null;
const nextButton = document.getElementById('nextButton');
const prevButton = document.getElementById('prevButton');

function checkButtons() {
    const currentPage = parseInt(urlParams.get('page')) || 1;
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

function searchOptions() {
    const orderBy = urlParams.get('ord');
    const query = urlParams.get('q');
    const categoriesValues = urlParams.getAll('cat');
    const quantity = urlParams.getAll('qty');
    const attributeValue = urlParams.getAll('attr');
    if (orderBy === '1' ){
        orden.value = '1'
    }
    if (query) {
        qWord.value = query
    }
    categories.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        if (categoriesValues.includes(checkbox.value)){
            checkbox.checked = true;
        };
    });
    if (quantity) {
        cantidad.value = quantity;
    };
    if (attributeValue) {
        atributo.value = attributeValue
    }

};

document.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        updateUrl();
    }
    console.log('ENTER');
});

// When page finish loading then execute checks
document.addEventListener("DOMContentLoaded", ()=> {
    if (pageButtons.length > 0){
        checkButtons();
    };
        searchOptions();
});