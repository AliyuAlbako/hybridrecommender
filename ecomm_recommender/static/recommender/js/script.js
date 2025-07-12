
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('searchInput');
    const suggestionsDiv = document.getElementById('suggestions');

    input.addEventListener('keyup', function() {
        const query = input.value;
        if (query.length > 0) {
            fetch(`/suggestions/?term=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsDiv.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach(item => {
                            const suggestionItem = document.createElement('div');
                            suggestionItem.innerHTML = `<a href="/product/${item.id}/">${item.name}</a>`;
                            suggestionItem.style.padding = '8px';
                            suggestionItem.style.borderBottom = '1px solid #eee';
                            suggestionItem.style.cursor = 'pointer';
                            suggestionsDiv.appendChild(suggestionItem);
                        });
                        suggestionsDiv.style.display = 'block';
                    } else {
                        suggestionsDiv.style.display = 'none';
                    }
                });
        } else {
            suggestionsDiv.style.display = 'none';
        }
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!suggestionsDiv.contains(e.target) && e.target !== input) {
            suggestionsDiv.style.display = 'none';
        }
    });
});
