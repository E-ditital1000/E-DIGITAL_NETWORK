 // static/js/voter_search.js

 document.addEventListener('DOMContentLoaded', function() {
    const userSelect = document.querySelector('select[name="user"]');
    const searchInput = document.createElement('input');
    searchInput.setAttribute('type', 'text');
    searchInput.setAttribute('placeholder', 'Search by name');
    searchInput.classList.add('form-control', 'mb-2');

    userSelect.parentNode.insertBefore(searchInput, userSelect);

    searchInput.addEventListener('keyup', function() {
        const searchTerm = searchInput.value.toLowerCase();
        for (let i = 0; i < userSelect.options.length; i++) {
            const option = userSelect.options[i];
            const text = option.text.toLowerCase();
            option.style.display = text.includes(searchTerm) ? 'block' : 'none';
        }
    });
});
