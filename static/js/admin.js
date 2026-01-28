requireLogin();

function headers() {
    return {
        "Content-Type": "application/json",
        "X-User-Id": localStorage.getItem("user_id"),
        "X-User-Role": localStorage.getItem("role")
    }
}

function createCourse() {
    fetch("/api/admin/courses", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({
            name: course_name.value,
            location: course_location.value,
            total_holes: parseInt(course_holes.value || 18)
        })
    })
    .then(r => r.json())
    .then(d => course_msg.innerText = d.message);
}

function addHole() {

    const courseId = document.getElementById("hole_course_id").value;
    const holeNumber = document.getElementById("hole_number").value;
    const par = document.getElementById("hole_par").value;

    fetch(`/api/admin/courses/${courseId}/holes`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-User-Id": localStorage.getItem("user_id"),
            "X-User-Role": localStorage.getItem("role")
        },
        body: JSON.stringify({
            hole_number: parseInt(holeNumber),
            par: parseInt(par)
        })
    })
    .then(r => r.json())
    .then(d => {

        console.log(d);   // debug

        if (d.message) {
            document.getElementById("hole_msg").innerText = d.message;
        } else if (d.error) {
            document.getElementById("hole_msg").innerText = d.error;
        } else {
            document.getElementById("hole_msg").innerText = "Unknown response";
        }
    });
}



function createTournament() {
    fetch("/api/tournaments", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({
            name: t_name.value,
            course_id: parseInt(t_course.value),
            start_date: t_start.value,
            end_date: t_end.value,
            status: t_status.value
        })
    })
    .then(r => r.json())
    .then(d => tournament_msg.innerText = d.message);
}
