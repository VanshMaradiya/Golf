requireLogin();

function headers() {
    return {
        "Content-Type": "application/json",
        "X-User-Id": localStorage.getItem("user_id"),
        "X-User-Role": localStorage.getItem("role")
    }
}

function loadTournaments() {
    fetch("/api/player/tournaments", { headers: headers() })
        .then(r => r.json())
        .then(d => {
            const sel = document.getElementById("tournamentSelect");
            sel.innerHTML = "";
            d.forEach(t => {
                sel.innerHTML += `<option value="${t.id}">${t.name}</option>`;
            });
            loadHoles();
            loadLeaderboard();
        });
}

function loadHoles() {
    const holeSel = document.getElementById("holeSelect");
    holeSel.innerHTML = "";
    for (let i = 1; i <= 18; i++) {
        holeSel.innerHTML += `<option value="${i}">Hole ${i}</option>`;
    }
}

function addScore() {
    const t = tournamentSelect.value;
    const h = holeSelect.value;
    const s = strokes.value;

    fetch(`/api/scores/tournaments/${t}/holes/${h}`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ strokes: parseInt(s) })
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("score_msg").innerText = d.message;
        loadLeaderboard();   // refresh leaderboard after score
    });
}

function loadLeaderboard() {
    const t = tournamentSelect.value;

    fetch(`/api/leaderboard/tournaments/${t}`)
        .then(r => r.json())
        .then(d => {

            const body = document.getElementById("leaderboard");
            body.innerHTML = "";

            d.leaderboard.forEach(p => {

                let style = "";

                // highlight winner
                if (p.rank === 1) {
                    style = "style='background:#d4edda;font-weight:bold'";
                }

                body.innerHTML += `
                    <tr ${style}>
                        <td>${p.rank}</td>
                        <td>${p.player_name}</td>
                        <td>${p.total_strokes}</td>
                    </tr>
                `;
            });
        });
}

loadTournaments();
