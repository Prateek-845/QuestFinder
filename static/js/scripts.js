function renderCard(title, asin, info) {
    return `
        <div class="card-title">${title}</div>
        <div class="card-sub">ASIN: ${asin}</div>
        <div class="card-info">${info}</div>
    `;
}

async function loadPopularGames() {
    const list = document.getElementById('popular_games');
    list.innerHTML = '';
    try {
        const res = await fetch('/popular_games');
        const data = await res.json();
        data.games.forEach(g => {
            const li = document.createElement('li');
            li.className = 'card';
            li.innerHTML = renderCard(
                g.title,
                g.asin,
                `Rating: ${g.average_rating} | ${g.review_count} reviews`
            );
            list.appendChild(li);
        });
    } catch (e) {
        list.innerHTML = '<li class="card">Failed to load trending games.</li>';
    }
}
loadPopularGames();

async function getRecommendations() {
    const userId = document.getElementById('user_id').value.trim();
    const list = document.getElementById('recommendations');
    list.innerHTML = '';
    if (!userId) return alert('Please enter a User ID.');
    try {
        const res = await fetch(`/recommend?user_id=${encodeURIComponent(userId)}`);
        const data = await res.json();
        if (data.error) return alert(data.error);
        if (!data.recommendations.length) {
            list.innerHTML = '<li class="card">No recommendations found for this user.</li>';
            return;
        }
        data.recommendations.forEach(r => {
            const li = document.createElement('li');
            li.className = 'card';
            li.innerHTML = renderCard(r.title, r.asin, `Predicted Rating: ${r.predicted_rating}`);
            list.appendChild(li);
        });
    } catch (e) {
        alert('Error fetching recommendations');
    }
}

async function getRecommendationsByTitle() {
    const title = document.getElementById('game_title').value.trim();
    const list = document.getElementById('title_recommendations');
    list.innerHTML = '';
    if (!title) return alert('Please enter a game title.');
    try {
        const res = await fetch(`/recommend_by_title?title=${encodeURIComponent(title)}`);
        const data = await res.json();
        if (data.error) return alert(data.error);
        if (!data.recommendations.length) {
            list.innerHTML = '<li class="card">No similar games found for that title.</li>';
            return;
        }
        data.recommendations.forEach(r => {
            const li = document.createElement('li');
            li.className = 'card';
            li.innerHTML = renderCard(r.title, r.asin, `Similarity: ${r.similarity}`);
            list.appendChild(li);
        });
    } catch (e) {
        alert('Error fetching recommendations');
    }
}